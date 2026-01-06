### do not delete this import scripts ###
import json
from py_base import set_g_values, get_g_values, requests_json, MidasAPI, Product
from py_base_sub import HelloWorld, ApiGet
### do not delete this import scripts ###

# BESTO Design Library import
from py_library import (
    HBeamData,
    HBeamToUSectionMatch,
    reBarArea,
    reBarUnitWeight,
    SquareSection,
    CombinedSection,
    ConcreteElasticModulus,
    EffectiveWidth,
    Deflection,
    Vibration,
    get_h_beam_data,
    calculate_section_properties,
    StructuralSteelYieldStress,
    WidthThicknessRatio,
    BeamForceCalculator,
    NominalMomentStrength_2,
    NominalShearStrength,
    StudAnchorStrength,
    AngleAnchorStrength,
    DesignMomentStrength,
    DesignShearStrength,
    StrengthCheck,
)

# 설계 기본값 import
from py_config import (
    STEEL_ELASTIC_MODULUS,
    CONCRETE_STRENGTH,
    DEFAULT_SPAN_LENGTH,
    DEFAULT_UNIFORM_LOAD,
    STUD_ANCHOR,
    get_default_design_inputs,
    create_u_section_squares,
    create_h_section_squares,
)


def main():
    """메인 함수 - Pyscript 엔트리 포인트"""
    print('BESTO Design Plugin initialized')


def get_beam_info(section_name):
    """H형강 정보 조회"""
    data = get_h_beam_data(section_name)
    if data:
        return json.dumps(data)
    return json.dumps({'error': 'Section not found'})


def get_matched_u_section(h_section_name):
    """H형강에 매칭되는 U형강 정보 조회"""
    if h_section_name in HBeamToUSectionMatch:
        return json.dumps(HBeamToUSectionMatch[h_section_name])
    return json.dumps({'error': 'No matching U-section found'})


def calculate_simple_section(height, width, thickness):
    """간단한 단면 계산"""
    result = calculate_section_properties(height, width, thickness)
    return json.dumps(result)


def test_section_calculation():
    """단면 계산 테스트"""
    # U단면 생성 예시
    wing1 = SquareSection(height=6, width=50, x=25, y=147)
    wing2 = SquareSection(height=6, width=50, x=125, y=147)
    web1 = SquareSection(height=138, width=6, x=3, y=75)
    web2 = SquareSection(height=138, width=6, x=147, y=75)
    bottomFlange = SquareSection(height=6, width=150, x=75, y=3)
    
    u_section = CombinedSection(wing1, wing2, web1, web2, bottomFlange)
    
    return json.dumps({
        'area': u_section.area,
        'centerY': u_section.centerY,
        'inertiaX': u_section.inertiaX,
        'plasticNeutralAxis': u_section.plasticNeutralAxis
    })


def calculate_design_strength(input_data):
    """
    설계강도 계산 메인 함수
    
    Args:
        input_data: UI에서 전달받은 입력 데이터 (JSON string 또는 dict)
    
    Returns:
        JSON string: 계산 결과
    """
    # 입력 데이터 파싱
    if isinstance(input_data, str):
        inputs = json.loads(input_data)
    else:
        inputs = input_data
    
    # 기본값 로드 및 UI 입력값으로 덮어쓰기
    config = get_default_design_inputs()
    config.update(inputs)
    
    # H형강 정보 가져오기
    h_section_name = config.get('selectedMember', 'H-400X200X8X13')
    h_data = HBeamData.get(h_section_name)
    
    if not h_data:
        return json.dumps({'error': f'H-section {h_section_name} not found'})
    
    # 매칭되는 U형강 정보
    u_match = HBeamToUSectionMatch.get(h_section_name)
    if not u_match:
        return json.dumps({'error': f'No matching U-section for {h_section_name}'})
    
    # 재료 물성
    steel_E = STEEL_ELASTIC_MODULUS
    steel_Fy_H = float(config.get('fYH', 355))
    steel_Fy_U = float(config.get('fYU', 355))
    
    # 콘크리트 강도
    concrete_grade = config.get('concrete', 'C30')
    f_ck = CONCRETE_STRENGTH.get(concrete_grade, 30)
    E_c = ConcreteElasticModulus(f_ck)
    
    # 기하 조건
    span = float(config.get('span_length', DEFAULT_SPAN_LENGTH))
    d_s = float(config.get('slabDs', 150))
    b_eff = float(config.get('slabBeff', 2000))
    
    # 철근 정보
    rebar_top_count = int(config.get('rebarTopCount', 0) or 0)
    rebar_top_dia = int(config.get('rebarTopDia', '16').replace('D', '') or 16)
    rebar_bot_count = int(config.get('rebarBotCount', 0) or 0)
    rebar_bot_dia = int(config.get('rebarBotDia', '16').replace('D', '') or 16)
    f_yr = float(config.get('fYr', 400) or 400)
    
    # H형강 단면 생성
    h_squares = create_h_section_squares(h_data)
    top_flange, web, bottom_flange = h_squares
    h_section = CombinedSection(top_flange, web, bottom_flange)
    
    # U형강 단면 생성
    u_squares = create_u_section_squares(
        u_match['U_height'],
        u_match['U_width'],
        u_match['U_thickness']
    )
    u_section = CombinedSection(*u_squares)
    
    # 부재력 계산
    uniform_load = float(config.get('uniform_load', DEFAULT_UNIFORM_LOAD))
    beam_calc = BeamForceCalculator(span)
    support_type = config.get('support', 'SimpleBeam')
    if support_type == 'Simple':
        support_type = 'SimpleBeam'
    elif support_type == 'Continuous':
        support_type = 'FixedEnd'
    
    # 중앙부 모멘트와 단부 전단력
    mid_forces = beam_calc.calculate_forces('Uniform', support_type, span/2, lineLoad=uniform_load)
    end_forces = beam_calc.calculate_forces('Uniform', support_type, 0, lineLoad=uniform_load)
    
    M_max = abs(mid_forces['Moment'])  # kN·m -> N·mm 변환은 나중에
    V_max = abs(end_forces['ShearForce'])
    
    # 공칭휨강도 계산 (H형강 단독 - 시공 전)
    unbraced_length = float(config.get('unbraced_length', 0))
    nominal_moment = NominalMomentStrength_2(
        h_section,
        steel_E,
        steel_Fy_H,
        unbraced_length
    )
    
    # 공칭전단강도 계산
    shear_area = h_data['H'] * h_data['t1']  # 웨브 전단면적
    nominal_shear = NominalShearStrength(
        web,
        shear_area,
        steel_Fy_H,
        steel_E
    )
    
    # 설계강도
    design_M = DesignMomentStrength(nominal_moment.nominalMomentStrength_Positive)
    design_V = DesignShearStrength(nominal_shear.nominalShearStrength)
    
    # 강도비 (소요강도/설계강도)
    M_ratio = (M_max * 1e6) / design_M if design_M > 0 else float('inf')  # kN·m -> N·mm
    V_ratio = (V_max * 1e3) / design_V if design_V > 0 else float('inf')  # kN -> N
    
    # 전단연결재 강도 (스터드)
    stud_spacing = float(config.get('studSpacing', 200) or 200)
    stud_strength = StudAnchorStrength(
        STUD_ANCHOR['area'],
        f_ck,
        E_c,
        STUD_ANCHOR['strength']
    )
    num_studs = span / stud_spacing
    total_stud_strength = stud_strength * num_studs
    
    # 처짐 계산
    I_steel = h_data['Ix'] * 1e4  # cm⁴ -> mm⁴
    deflection, _ = Deflection(
        'Pin-Pin' if support_type == 'SimpleBeam' else 'Fix-Fix',
        uniform_load,  # N/mm
        span,
        steel_E,
        I_steel
    )
    deflection_limit = span / config.get('deflection_limit_ratio', 360)
    deflection_ratio = deflection / deflection_limit if deflection_limit > 0 else 0
    
    # 결과 반환
    result = {
        'sectionInfo': {
            'hSection': h_section_name,
            'uSection': f"U-{int(u_match['U_height'])}x{int(u_match['U_width'])}x{u_match['U_thickness']}",
            'hArea': h_data['A'],
            'uArea': round(u_section.area, 2),
        },
        'materialInfo': {
            'steelFyH': steel_Fy_H,
            'steelFyU': steel_Fy_U,
            'concrete': concrete_grade,
            'fck': f_ck,
            'Ec': round(E_c, 0),
        },
        'forces': {
            'maxMoment': round(M_max, 2),
            'maxShear': round(V_max, 2),
        },
        'beforeComposite': {
            'nominalMomentStrength': round(nominal_moment.nominalMomentStrength_Positive / 1e6, 2),  # N·mm -> kN·m
            'nominalShearStrength': round(nominal_shear.nominalShearStrength / 1e3, 2),  # N -> kN
            'designMomentStrength': round(design_M / 1e6, 2),
            'designShearStrength': round(design_V / 1e3, 2),
            'momentRatio': round(M_ratio, 3),
            'shearRatio': round(V_ratio, 3),
            'momentCheck': 'OK' if M_ratio <= 1.0 else 'NG',
            'shearCheck': 'OK' if V_ratio <= 1.0 else 'NG',
        },
        'shearConnector': {
            'studSpacing': stud_spacing,
            'studUnitStrength': round(stud_strength / 1e3, 2),  # N -> kN
            'numStuds': round(num_studs, 0),
            'totalStudStrength': round(total_stud_strength / 1e3, 2),
        },
        'serviceability': {
            'deflection': round(deflection, 2),
            'deflectionLimit': round(deflection_limit, 2),
            'deflectionRatio': round(deflection_ratio, 3),
            'deflectionCheck': 'OK' if deflection_ratio <= 1.0 else 'NG',
        },
        'overallCheck': 'OK' if (M_ratio <= 1.0 and V_ratio <= 1.0 and deflection_ratio <= 1.0) else 'NG',
    }
    
    return json.dumps(result, ensure_ascii=False)


def test_design_strength():
    """설계강도 계산 테스트 (더미 데이터 사용)"""
    test_input = {
        'selectedMember': 'H-400X200X8X13',
        'rebarTopCount': '4',
        'rebarTopDia': 'D16',
        'rebarBotCount': '2',
        'rebarBotDia': 'D16',
        'fYr': '400',
        'studSpacing': '200',
        'angleSpacing': '',
        'fYU': '355',
        'fYH': '355',
        'concrete': 'C30',
        'slabDs': '150',
        'slabBeff': '2000',
        'support': 'Simple',
    }
    
    return calculate_design_strength(test_input)
