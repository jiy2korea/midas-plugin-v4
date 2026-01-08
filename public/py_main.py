### do not delete this import scripts ###
import json
import copy
import math
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
    NominalMomentStrength_6,
    NominalShearStrength,
    StudAnchorStrength,
    AngleAnchorStrength,
    DesignMomentStrength,
    DesignShearStrength,
    StrengthCheck,
    ServiceabilityCheck,
    CompositeSectionMomentStrength_positive,
    CompositeSectionMomentStrength_Negative,
    EffectiveInertia,
    MinimumRebarSpacingCheck,
    CostCalculation,
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


# =============================================================================
# 설계 계산 메인 함수
# =============================================================================

def calculate_design_strength(input_data):
    """
    설계강도 계산 메인 함수 (BestoDesign.py 로직 이식)
    
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
    
    try:
        result = _run_design_calculation(config)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)


def _run_design_calculation(config):
    """설계 계산 실행 (내부 함수)"""
    
    # ==========================================================================
    # 1. 입력 데이터 파싱
    # ==========================================================================
    
    # H형강 정보
    h_section_name = config.get('selectedMember')
    if not h_section_name:
        raise ValueError('selectedMember is required but not provided')
    h_data = HBeamData.get(h_section_name)
    if not h_data:
        raise ValueError(f'H-section {h_section_name} not found')
    
    H_height = h_data['H']
    H_width = h_data['B']
    H_web_thickness = h_data['t1']
    H_flange_thickness = h_data['t2']
    H_length = float(config.get('h_bracket_length', 1700))  # H브라켓 길이
    
    # U형강 정보 (매칭)
    u_match = HBeamToUSectionMatch.get(h_section_name)
    if not u_match:
        raise ValueError(f'No matching U-section for {h_section_name}')
    
    U_height = u_match['U_height']
    U_width = u_match['U_width']
    U_wing_width = u_match.get('U_wing_width', 80)  # 날개폭 기본값
    U_thickness = u_match['U_thickness']
    
    # 재료 물성
    steel_E = float(config.get('steelElasticModulus', STEEL_ELASTIC_MODULUS))  # 탄성계수 (config에서 받거나 기본값 사용)
    
    # 강종 정보 (두께에 따라 항복강도 계산)
    steel_H_type = config.get('steelH')  # H형강 강종 (예: 'SM355', 'SM420' 등)
    steel_U_type = config.get('steelU')  # U형강 강종 (예: 'SM355', 'SM420' 등)
    
    # 항복강도 계산: 강종이 제공되면 두께에 따라 계산, 없으면 기존 방식 사용
    if steel_H_type and steel_H_type in ['SM355', 'SM420', 'SM460', 'SN355', 'SHN355']:
        steel_Fy_H = StructuralSteelYieldStress(steel=steel_H_type, thickness=H_flange_thickness)
    else:
        steel_Fy_H = float(config.get('fYH', 355))
    
    if steel_U_type and steel_U_type in ['SM355', 'SM420', 'SM460', 'SN355', 'SHN355']:
        steel_Fy_U = StructuralSteelYieldStress(steel=steel_U_type, thickness=U_thickness)
    else:
        steel_Fy_U = float(config.get('fYU', 355))
    
    f_yr = float(config.get('fYr', 400))  # 철근 항복강도
    
    # 콘크리트 강도
    concrete_grade = config.get('concrete', 'C30')
    f_ck = CONCRETE_STRENGTH.get(concrete_grade, 30)
    E_c = ConcreteElasticModulus(f_ck)
    
    # 기하 조건
    beam_length = float(config.get('span_length', DEFAULT_SPAN_LENGTH))
    spacing1 = float(config.get('bay_spacing1', 3000))  # 좌측 간격
    spacing2 = float(config.get('bay_spacing2', 3000))  # 우측 간격
    slab_depth = float(config.get('slabDs', 150))
    
    # 철근 정보
    top_rebar_qty = int(config.get('rebarTopCount', 0) or 0)
    top_rebar_dia_str = str(config.get('rebarTopDia', 'D16'))
    top_rebar_dia = int(top_rebar_dia_str.replace('D', '') if 'D' in top_rebar_dia_str else top_rebar_dia_str)
    top_rebar_area = reBarArea.get(top_rebar_dia, 199)
    
    bot_rebar_qty = int(config.get('rebarBotCount', 0) or 0)
    bot_rebar_dia_str = str(config.get('rebarBotDia', 'D16'))
    bot_rebar_dia = int(bot_rebar_dia_str.replace('D', '') if 'D' in bot_rebar_dia_str else bot_rebar_dia_str)
    bot_rebar_area = reBarArea.get(bot_rebar_dia, 199)
    
    # 전단연결재
    stud_spacing = float(config.get('studSpacing', 200) or 200)
    angle_spacing = float(config.get('angleSpacing', 0) or 0)
    shear_connector_height = 50  # 전단연결재 높이
    
    # 설계 조건
    end_condition = config.get('endCondition', 'Fix-Fix')
    beam_support = int(config.get('beamSupport', 0))  # 0: 무지보, 1: 서포트
    usage_for_vibration = config.get('usageForVibration', '사무실')  # '사무실', '쇼핑몰', '육교(실내)', '육교(실외)'
    
    # 하중
    live_load_construction = float(config.get('liveLoadConstruction', 2.5))  # 시공하중 [kN/m²]
    dead_load_finish = float(config.get('deadLoadFinish', 1.5))  # 마감하중 [kN/m²]
    live_load_permanent = float(config.get('liveLoadPermanent', 2.5))  # 활하중 [kN/m²]
    
    # 부재력 (수동 입력)
    manual_positive_moment = float(config.get('manualPositiveMoment', 0) or 0) * 1e6  # kN·m -> N·mm
    manual_negative_moment = float(config.get('manualNegativeMoment', 0) or 0) * 1e6
    manual_negative_moment_U = float(config.get('manualNegativeMomentU', 0) or 0) * 1e6
    manual_shear_force = float(config.get('manualShearForce', 0) or 0) * 1e3  # kN -> N
    
    # ==========================================================================
    # 2. 단면 생성
    # ==========================================================================
    
    # U단면
    U_wing1 = SquareSection(
        height=U_thickness, 
        width=U_wing_width + U_thickness, 
        x=(U_wing_width + U_thickness) / 2, 
        y=U_height - U_thickness / 2
    )
    U_wing2 = SquareSection(
        height=U_thickness, 
        width=U_wing_width + U_thickness, 
        x=U_width - (U_wing_width + U_thickness) / 2, 
        y=U_height - U_thickness / 2
    )
    U_web1 = SquareSection(
        height=U_height - U_thickness * 2, 
        width=U_thickness, 
        x=U_thickness / 2, 
        y=U_height / 2
    )
    U_web2 = SquareSection(
        height=U_height - U_thickness * 2, 
        width=U_thickness, 
        x=U_width - U_thickness / 2, 
        y=U_height / 2
    )
    U_bottom_flange = SquareSection(
        height=U_thickness, 
        width=U_width, 
        x=U_width / 2, 
        y=U_thickness / 2
    )
    U_section = CombinedSection(U_wing1, U_wing2, U_web1, U_web2, U_bottom_flange)
    weight_U_section = U_section.area / 1e6 * 78.5  # kN/m (강재 단위중량 78.5 kN/m³)
    
    # H단면
    H_top_flange = SquareSection(
        height=H_flange_thickness, 
        width=H_width, 
        x=H_width / 2, 
        y=H_height - H_flange_thickness / 2
    )
    H_bottom_flange = SquareSection(
        height=H_flange_thickness, 
        width=H_width, 
        x=H_width / 2, 
        y=H_flange_thickness / 2
    )
    H_web = SquareSection(
        height=H_height - H_flange_thickness * 2, 
        width=H_web_thickness, 
        x=H_width / 2, 
        y=H_height / 2
    )
    H_section = CombinedSection(H_top_flange, H_bottom_flange, H_web)
    if h_section_name in HBeamData:
        H_section.area = HBeamData[h_section_name]['A'] * 100  # cm² -> mm²
    weight_H_section = H_section.area / 1e6 * 78.5  # kN/m
    
    # 콘크리트 단면
    effective_width = EffectiveWidth(span=beam_length, bay=spacing1) + EffectiveWidth(span=beam_length, bay=spacing2)
    conc_in_U = SquareSection(
        height=U_height - U_thickness, 
        width=U_width - 2 * U_thickness, 
        x=U_wing_width + U_width / 2, 
        y=(U_height - U_thickness) / 2 + U_thickness
    )
    conc_slab = SquareSection(
        height=slab_depth, 
        width=effective_width, 
        x=U_wing_width + U_width / 2, 
        y=U_height + slab_depth / 2
    )
    C_section = CombinedSection(conc_in_U, conc_slab)
    weight_C_section = (conc_in_U.area + slab_depth * (spacing1 + spacing2) / 2) / 1e6 * 24  # kN/m (RC 24 kN/m³)
    
    # 합성단면
    elastic_modulus_ratio = steel_E / E_c
    tran_conc_section = copy.deepcopy(C_section)
    tran_conc_section.area = C_section.area / elastic_modulus_ratio
    tran_conc_section.inertiaX = C_section.inertiaX / elastic_modulus_ratio
    composite_section = CombinedSection(U_section, tran_conc_section)
    
    # ==========================================================================
    # 3. 하중 계산
    # ==========================================================================
    
    weight_live_load = (spacing1 + spacing2) / 2 / 1000 * live_load_permanent
    weight_dead_load1 = weight_C_section + weight_U_section
    weight_dead_load2 = (spacing1 + spacing2) / 2 / 1000 * dead_load_finish
    weight_construction_load = (spacing1 + spacing2) / 2 / 1000 * live_load_construction
    
    # 시공중 하중
    beam_force_calc = BeamForceCalculator(beam_length)
    factored_construction_load = 1.2 * weight_dead_load1 + 1.6 * weight_construction_load
    
    if beam_support == 0:  # 무지보
        end_moment_construction = abs(beam_force_calc.calculate_forces(
            "Uniform", end_condition, beam_length, lineLoad=factored_construction_load
        )["Moment"])
        end_moment_U_construction = abs(beam_force_calc.calculate_forces(
            "Uniform", end_condition, H_length, lineLoad=factored_construction_load
        )["Moment"])
        center_moment_construction = abs(beam_force_calc.calculate_forces(
            "Uniform", end_condition, beam_length / 2, lineLoad=factored_construction_load
        )["Moment"])
        shear_construction = abs(beam_force_calc.calculate_forces(
            "Uniform", end_condition, 0, lineLoad=factored_construction_load
        )["ShearForce"])
    else:  # 서포트 사용
        end_moment_construction = 0
        end_moment_U_construction = 0
        center_moment_construction = 0
        shear_construction = 0
    
    # 시공후 하중 (수동 입력 또는 계산)
    if manual_positive_moment > 0:
        center_moment_permanent = manual_positive_moment
        end_moment_permanent = manual_negative_moment
        end_moment_U_permanent = manual_negative_moment_U
        shear_permanent = manual_shear_force
    else:
        # 자동 계산
        factored_permanent_load = 1.2 * (weight_dead_load1 + weight_dead_load2) + 1.6 * weight_live_load
        center_moment_permanent = abs(beam_force_calc.calculate_forces(
            "Uniform", end_condition, beam_length / 2, lineLoad=factored_permanent_load
        )["Moment"])
        end_moment_permanent = abs(beam_force_calc.calculate_forces(
            "Uniform", end_condition, beam_length, lineLoad=factored_permanent_load
        )["Moment"])
        end_moment_U_permanent = abs(beam_force_calc.calculate_forces(
            "Uniform", end_condition, H_length, lineLoad=factored_permanent_load
        )["Moment"])
        shear_permanent = abs(beam_force_calc.calculate_forces(
            "Uniform", end_condition, 0, lineLoad=factored_permanent_load
        )["ShearForce"])
    
    # ==========================================================================
    # 4. 시공중 검토
    # ==========================================================================
    
    # --- U단면 정모멘트 검토 ---
    U_required_M_positive = center_moment_construction
    U_nominal_M_positive = NominalMomentStrength_6(
        section=U_section, 
        flange=U_wing1, 
        Steel_elasticModulus=steel_E, 
        Steel_yieldStress=steel_Fy_U, 
        direction="P", 
        typeNumber=3
    )
    U_design_M_positive = DesignMomentStrength(U_nominal_M_positive.elasticMomentStrength)
    U_moment_check_positive = StrengthCheck(U_design_M_positive, U_required_M_positive)
    
    # --- U단면 부모멘트 검토 ---
    U_required_M_negative = end_moment_U_construction
    U_nominal_M_negative = NominalMomentStrength_6(
        section=U_section, 
        flange=U_bottom_flange, 
        Steel_elasticModulus=steel_E, 
        Steel_yieldStress=steel_Fy_U, 
        direction="N", 
        typeNumber=8
    )
    U_design_M_negative = DesignMomentStrength(U_nominal_M_negative.elasticMomentStrength)
    U_moment_check_negative = StrengthCheck(U_design_M_negative, U_required_M_negative)
    
    # --- U단면 전단 검토 ---
    U_required_V = shear_construction
    U_shear_area = U_height * U_thickness * 2
    U_nominal_V = NominalShearStrength(
        square=U_web1, 
        shearArea=U_shear_area, 
        yieldStress=steel_Fy_U, 
        elasticModulus=steel_E
    )
    U_design_V = DesignShearStrength(U_nominal_V.nominalShearStrength)
    U_shear_check = StrengthCheck(U_design_V, U_required_V)
    
    # --- H단면 부모멘트 검토 ---
    H_required_M_negative = end_moment_construction
    H_nominal_M = NominalMomentStrength_2(
        section=H_section, 
        Steel_elasticModulus=steel_E, 
        Steel_yieldStress=steel_Fy_H, 
        unbracedLength=H_length * 2
    )
    H_design_M_negative = DesignMomentStrength(H_nominal_M.elasticMomentStrength)
    H_moment_check_negative = StrengthCheck(H_design_M_negative, H_required_M_negative)
    
    # --- H단면 전단 검토 ---
    H_required_V = shear_construction
    H_nominal_V = NominalShearStrength(
        square=H_web, 
        shearArea=H_height * H_web_thickness, 
        yieldStress=steel_Fy_H, 
        elasticModulus=steel_E
    )
    H_design_V = DesignShearStrength(H_nominal_V.nominalShearStrength) / 0.9  # 압연형강 phi=1.0
    H_shear_check = StrengthCheck(H_design_V, H_required_V)
    
    # --- 시공중 처짐 검토 ---
    required_deflection_construction = 40  # mm
    if beam_support == 0:
        deflection_D1, _ = Deflection(
            'Fix-Fix', weight_dead_load1, beam_length, steel_E, U_section.inertiaX
        )
        deflection_C, _ = Deflection(
            'Fix-Fix', weight_construction_load, beam_length, steel_E, U_section.inertiaX
        )
    else:
        deflection_D1 = 0
        deflection_C = 0
    deflection_check_construction = ServiceabilityCheck(
        deflection_D1 + deflection_C, required_deflection_construction
    )
    
    # ==========================================================================
    # 5. 시공후 검토 (합성단면)
    # ==========================================================================
    
    # --- 전단연결재 강도 ---
    stud_anchor_strength = StudAnchorStrength(
        studAnchorArea=math.pi * (19 / 2) ** 2,  # 19mm 스터드
        f_ck=f_ck,
        concreteElasticModulus=E_c,
        studAnchorStrength=400
    )
    
    angle_anchor_strength = AngleAnchorStrength(
        height=shear_connector_height,
        U_width=U_width - U_wing_width * 2,
        f_ck=f_ck
    )
    
    # 스터드 개수 및 강도
    if stud_spacing > 0:
        stud_count = math.floor((beam_length - H_length) / 2 / stud_spacing)
        stud_strength_total = stud_anchor_strength * stud_count
    else:
        stud_count = 0
        stud_strength_total = 0
    
    # 앵글 개수 및 강도
    if angle_spacing > 0:
        angle_count = math.floor((beam_length - H_length) / 2 / angle_spacing)
        angle_strength_total = angle_anchor_strength * angle_count
    else:
        angle_count = 0
        angle_strength_total = 0
    
    shear_connector_strength = stud_strength_total + angle_strength_total
    
    # --- 합성단면 정모멘트 검토 ---
    Comp_required_M_positive = center_moment_permanent
    Comp_web_WT = WidthThicknessRatio(
        width=U_web1.height, 
        thickness=U_web1.width, 
        elasticModulus=steel_E, 
        yieldStress=steel_Fy_U, 
        typeNumber=6
    )
    
    Comp_nominal_M_positive = CompositeSectionMomentStrength_positive(
        P_y=steel_Fy_U * U_section.area,
        P_rb=f_yr * bot_rebar_qty * bot_rebar_area,
        f_ck=f_ck,
        A_s=conc_slab.area,
        Q_n=shear_connector_strength,
        b_eff=effective_width,
        d_s=slab_depth,
        F_y=steel_Fy_U,
        steelSection=U_section,
        compressiveFlanges=(U_wing1, U_wing2),
        webs=(U_web1, U_web2),
        tensionRebarStrength=bot_rebar_qty * bot_rebar_area * f_yr,
        widthThicknessRatio=[Comp_web_WT.check(), Comp_web_WT.check()]
    )
    Comp_design_M_positive = DesignMomentStrength(Comp_nominal_M_positive)
    Comp_moment_check_positive = StrengthCheck(Comp_design_M_positive, Comp_required_M_positive)
    
    # --- 합성단면 부모멘트 검토 (U단면부) ---
    Comp_required_M_negative_U = end_moment_U_permanent
    Comp_bottom_flange_WT = WidthThicknessRatio(
        width=U_bottom_flange.width, 
        thickness=U_bottom_flange.height, 
        elasticModulus=steel_E, 
        yieldStress=steel_Fy_U, 
        typeNumber=8
    )
    
    Comp_nominal_M_negative_U = CompositeSectionMomentStrength_Negative(
        topRebarStrength=f_yr * top_rebar_qty * top_rebar_area,
        Qn=shear_connector_strength,
        Pyc=steel_Fy_U * U_section.area,
        ds=slab_depth,
        slabCoverConcreteDepth=20,
        Fy=steel_Fy_U,
        tensileFlanges=(U_wing1, U_wing2),
        webs=(U_web1, U_web2),
        steelSection=U_section,
        widthThicknessRatio=[Comp_web_WT.check(), Comp_web_WT.check(), Comp_bottom_flange_WT.check()]
    )
    Comp_design_M_negative_U = DesignMomentStrength(Comp_nominal_M_negative_U)
    Comp_moment_check_negative_U = StrengthCheck(Comp_design_M_negative_U, Comp_required_M_negative_U)
    
    # --- 합성단면 부모멘트 검토 (H단면부) ---
    Comp_required_M_negative_H = end_moment_permanent
    H_bottom_flange_WT = WidthThicknessRatio(
        width=H_bottom_flange.width / 2, 
        thickness=H_bottom_flange.height, 
        elasticModulus=steel_E, 
        yieldStress=steel_Fy_H, 
        typeNumber=1
    )
    H_web_WT = WidthThicknessRatio(
        width=H_web.height, 
        thickness=H_web.width, 
        elasticModulus=steel_E, 
        yieldStress=steel_Fy_H, 
        typeNumber=6
    )
    
    Comp_nominal_M_negative_H = CompositeSectionMomentStrength_Negative(
        topRebarStrength=f_yr * top_rebar_qty * top_rebar_area,
        Qn=shear_connector_strength,
        Pyc=steel_Fy_H * H_section.area,
        ds=slab_depth,
        slabCoverConcreteDepth=40,
        Fy=steel_Fy_H,
        tensileFlanges=[H_top_flange],
        webs=[H_web],
        steelSection=H_section,
        widthThicknessRatio=[H_web_WT.check(), H_bottom_flange_WT.check()]
    )
    Comp_design_M_negative_H = DesignMomentStrength(Comp_nominal_M_negative_H)
    Comp_moment_check_negative_H = StrengthCheck(Comp_design_M_negative_H, Comp_required_M_negative_H)
    
    # --- 합성단면 전단 검토 ---
    Comp_required_V = shear_permanent
    Comp_shear_check = StrengthCheck(U_design_V, Comp_required_V)
    
    # --- 시공후 처짐 검토 ---
    composite_ratio = min(
        shear_connector_strength / min(
            steel_Fy_U * U_section.area + f_yr * bot_rebar_qty * bot_rebar_area,
            0.85 * f_ck * conc_slab.area
        ), 
        1.0
    )
    effective_inertia = EffectiveInertia(
        steelSectionInertia=U_section.inertiaX,
        compositeRatio=composite_ratio,
        compositeSectionInertia=composite_section.inertiaX
    )
    
    deflection_live, _ = Deflection(
        'Fix-Fix', weight_live_load, beam_length, steel_E, effective_inertia
    )
    deflection_dead_live_support, _ = Deflection(
        'Fix-Fix', weight_live_load + weight_dead_load1 + weight_dead_load2, 
        beam_length, steel_E, effective_inertia
    )
    deflection_dead_live_no_support_1, _ = Deflection(
        'Fix-Fix', weight_live_load + weight_dead_load2, beam_length, steel_E, effective_inertia
    )
    deflection_dead_live_no_support_2, _ = Deflection(
        'Fix-Fix', weight_dead_load1, beam_length, steel_E, U_section.inertiaX
    )
    deflection_dead_live_no_support = deflection_dead_live_no_support_1 + deflection_dead_live_no_support_2
    
    deflection_check_live = ServiceabilityCheck(deflection_live, beam_length / 360)
    deflection_check_dead_live = ServiceabilityCheck(
        deflection_dead_live_support if beam_support == 1 else deflection_dead_live_no_support,
        beam_length / 240
    )
    
    # --- 진동 검토 ---
    vibration = Vibration(
        useage=usage_for_vibration, 
        deflection_L=deflection_live, 
        weight=200
    )
    
    # ==========================================================================
    # 6. 비용 계산
    # ==========================================================================
    
    section1_length = beam_length - H_length * 2  # U단면 길이
    section2_length = H_length * 2  # H단면 길이
    volumn_conc_in_U = conc_in_U.area * (beam_length - 3800)
    
    cost_calc = CostCalculation(
        section1_length=section1_length,
        section2_length=section2_length,
        unitWeight_Section1=weight_U_section,
        unitWeight_Section2=weight_H_section,
        volumn_concInU=volumn_conc_in_U,
        angleShearConnector_spacing=angle_spacing,
        studShearConnector_spacing=stud_spacing,
        topRebarDiameter=top_rebar_dia,
        topRebarQuantity=top_rebar_qty,
        bottomRebarDiameter=bot_rebar_dia,
        bottomRebarQuantity=bot_rebar_qty,
        H_Section_List=h_section_name,
        overlappedLength=500
    )
    
    # ==========================================================================
    # 7. 결과 반환
    # ==========================================================================
    
    result = {
        'sectionInfo': {
            'hSection': h_section_name,
            'uSection': f"U-{int(U_height)}x{int(U_width)}x{U_thickness}",
            'hArea': round(H_section.area, 2),
            'uArea': round(U_section.area, 2),
            'hInertia': round(H_section.inertiaX, 0),
            'uInertia': round(U_section.inertiaX, 0),
            'hModulusX1': round(H_section.sectionModulusX1, 2),
            'compositeInertia': round(composite_section.inertiaX, 0),
            'effectiveWidth': round(effective_width, 2),
        },
        'materialInfo': {
            'steelFyH': steel_Fy_H,
            'steelFyU': steel_Fy_U,
            'steelE': steel_E,
            'concrete': concrete_grade,
            'fck': f_ck,
            'Ec': round(E_c, 0),
            'fyr': f_yr,
        },
        'loads': {
            'weightDeadLoad1': round(weight_dead_load1, 3),
            'weightDeadLoad2': round(weight_dead_load2, 3),
            'weightLiveLoad': round(weight_live_load, 3),
            'weightConstructionLoad': round(weight_construction_load, 3),
        },
        'constructionStage': {
            'U_positive': {
                'requiredStrength': round(U_required_M_positive / 1e6, 2),
                'nominalStrength': round(U_nominal_M_positive.elasticMomentStrength / 1e6, 2),
                'designStrength': round(U_design_M_positive / 1e6, 2),
                'ratio': round(U_required_M_positive / U_design_M_positive, 3) if U_design_M_positive > 0 else 0,
                'check': 'OK' if U_moment_check_positive else 'NG',
            },
            'U_negative': {
                'requiredStrength': round(U_required_M_negative / 1e6, 2),
                'nominalStrength': round(U_nominal_M_negative.elasticMomentStrength / 1e6, 2),
                'designStrength': round(U_design_M_negative / 1e6, 2),
                'ratio': round(U_required_M_negative / U_design_M_negative, 3) if U_design_M_negative > 0 else 0,
                'check': 'OK' if U_moment_check_negative else 'NG',
            },
            'U_shear': {
                'requiredStrength': round(U_required_V / 1e3, 2),
                'nominalStrength': round(U_nominal_V.nominalShearStrength / 1e3, 2),
                'designStrength': round(U_design_V / 1e3, 2),
                'ratio': round(U_required_V / U_design_V, 3) if U_design_V > 0 else 0,
                'check': 'OK' if U_shear_check else 'NG',
            },
            'H_negative': {
                'requiredStrength': round(H_required_M_negative / 1e6, 2),
                'nominalStrength': round(H_nominal_M.elasticMomentStrength / 1e6, 2),
                'designStrength': round(H_design_M_negative / 1e6, 2),
                'ratio': round(H_required_M_negative / H_design_M_negative, 3) if H_design_M_negative > 0 else 0,
                'check': 'OK' if H_moment_check_negative else 'NG',
            },
            'H_shear': {
                'requiredStrength': round(H_required_V / 1e3, 2),
                'nominalStrength': round(H_nominal_V.nominalShearStrength / 1e3, 2),
                'designStrength': round(H_design_V / 1e3, 2),
                'ratio': round(H_required_V / H_design_V, 3) if H_design_V > 0 else 0,
                'check': 'OK' if H_shear_check else 'NG',
            },
            'deflection': {
                'deflectionD1': round(deflection_D1, 2),
                'deflectionC': round(deflection_C, 2),
                'totalDeflection': round(deflection_D1 + deflection_C, 2),
                'limit': required_deflection_construction,
                'check': 'OK' if deflection_check_construction else 'NG',
            },
        },
        'compositeStage': {
            'shearConnector': {
                'studCount': stud_count,
                'studUnitStrength': round(stud_anchor_strength / 1e3, 2),
                'studTotalStrength': round(stud_strength_total / 1e3, 2),
                'angleCount': angle_count,
                'angleUnitStrength': round(angle_anchor_strength / 1e3, 2),
                'angleTotalStrength': round(angle_strength_total / 1e3, 2),
                'totalStrength': round(shear_connector_strength / 1e3, 2),
            },
            'U_positive': {
                'requiredStrength': round(Comp_required_M_positive / 1e6, 2),
                'nominalStrength': round(Comp_nominal_M_positive / 1e6, 2),
                'designStrength': round(Comp_design_M_positive / 1e6, 2),
                'ratio': round(Comp_required_M_positive / Comp_design_M_positive, 3) if Comp_design_M_positive > 0 else 0,
                'check': 'OK' if Comp_moment_check_positive else 'NG',
            },
            'U_negative': {
                'requiredStrength': round(Comp_required_M_negative_U / 1e6, 2),
                'nominalStrength': round(Comp_nominal_M_negative_U / 1e6, 2),
                'designStrength': round(Comp_design_M_negative_U / 1e6, 2),
                'ratio': round(Comp_required_M_negative_U / Comp_design_M_negative_U, 3) if Comp_design_M_negative_U > 0 else 0,
                'check': 'OK' if Comp_moment_check_negative_U else 'NG',
            },
            'H_negative': {
                'requiredStrength': round(Comp_required_M_negative_H / 1e6, 2),
                'nominalStrength': round(Comp_nominal_M_negative_H / 1e6, 2),
                'designStrength': round(Comp_design_M_negative_H / 1e6, 2),
                'ratio': round(Comp_required_M_negative_H / Comp_design_M_negative_H, 3) if Comp_design_M_negative_H > 0 else 0,
                'check': 'OK' if Comp_moment_check_negative_H else 'NG',
            },
            'shear': {
                'requiredStrength': round(Comp_required_V / 1e3, 2),
                'designStrength': round(U_design_V / 1e3, 2),
                'ratio': round(Comp_required_V / U_design_V, 3) if U_design_V > 0 else 0,
                'check': 'OK' if Comp_shear_check else 'NG',
            },
            'deflection': {
                'compositeRatio': round(composite_ratio * 100, 1),
                'effectiveInertia': round(effective_inertia, 0),
                'deflectionLive': round(deflection_live, 2),
                'deflectionLiveLimit': round(beam_length / 360, 2),
                'deflectionLiveCheck': 'OK' if deflection_check_live else 'NG',
                'deflectionDeadLive': round(
                    deflection_dead_live_support if beam_support == 1 else deflection_dead_live_no_support, 2
                ),
                'deflectionDeadLiveLimit': round(beam_length / 240, 2),
                'deflectionDeadLiveCheck': 'OK' if deflection_check_dead_live else 'NG',
            },
            'vibration': {
                'naturalFrequency': round(vibration.naturalFrequency, 2),
                'maxAccelerationRatio': round(vibration.maxAccelerationRatio * 100, 2),
                'accelerationLimit': round(vibration.accRatioLimit.get(usage_for_vibration, 0.5) * 100, 1),
                'check': 'OK' if vibration.check else 'NG',
            },
        },
        'cost': {
            'weightSection1': round(cost_calc.weight_Section1 / 9800, 2),  # kgf -> kg
            'weightSection2': round(cost_calc.weight_Section2 / 9800, 2),
            'spliceWeight': round(cost_calc.bestoGirderSplice_weight / 9800, 2),
            'topRebarWeight': round(cost_calc.topRebar_weight / 9800, 2),
            'bottomRebarWeight': round(cost_calc.bottomRebar_weight / 9800, 2),
            'angleWeight': round(cost_calc.angle_weight / 9800, 2),
            'studCount': round(cost_calc.stud_number + cost_calc.section2_stud_Number, 0),
            'concreteVolume': round(volumn_conc_in_U / 1e9, 2),
            'totalCost': round(cost_calc.totalCost, 0),
        },
        'overallCheck': _get_overall_check([
            U_moment_check_positive, U_moment_check_negative, U_shear_check,
            H_moment_check_negative, H_shear_check, deflection_check_construction,
            Comp_moment_check_positive, Comp_moment_check_negative_U, 
            Comp_moment_check_negative_H, Comp_shear_check,
            deflection_check_live, deflection_check_dead_live, vibration.check
        ]),
    }
    
    return result


def _get_overall_check(checks):
    """전체 검토 결과 판정"""
    return 'OK' if all(checks) else 'NG'
