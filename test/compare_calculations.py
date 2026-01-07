"""
레거시 파일(BestoDesign.py)과 현재 프로젝트(py_main.py)의 계산값 비교 테스트

엑셀 파일에서 입력값을 읽어서 두 방법으로 계산하고 비교합니다.
"""
import os
import sys
import json
import xlwings

# 경로 설정
current_path = os.path.dirname(os.path.abspath(__file__))
legacy_path = os.path.join(current_path, 'legacy')
public_path = os.path.join(current_path, '..', 'public')

# 레거시 모듈 import
sys.path.insert(0, legacy_path)
import library as legacy_library

# 현재 프로젝트 모듈 import
sys.path.insert(0, public_path)
from py_library import (
    HBeamData,
    HBeamToUSectionMatch,
    SquareSection,
    CombinedSection,
    NominalMomentStrength_6,
    DesignMomentStrength,
    StructuralSteelYieldStress,
    ConcreteElasticModulus,
    EffectiveWidth,
    BeamForceCalculator,
    NominalMomentStrength_2,
    NominalShearStrength,
    DesignShearStrength,
    StrengthCheck,
    ServiceabilityCheck,
    Deflection,
    StudAnchorStrength,
    AngleAnchorStrength,
    CompositeSectionMomentStrength_positive,
    CompositeSectionMomentStrength_Negative,
    EffectiveInertia,
    Vibration,
    WidthThicknessRatio,
    CostCalculation,
    MinimumRebarSpacingCheck,
)
from py_config import (
    STEEL_ELASTIC_MODULUS,
    CONCRETE_STRENGTH,
    DEFAULT_SPAN_LENGTH,
)
import copy
import math


def read_excel_inputs(excel_path):
    """엑셀 파일에서 입력값 읽기"""
    wb = xlwings.Book(excel_path)
    inputSheet = wb.sheets['design']
    
    inputs = {}
    
    # 1. Section
    inputs['U_height'] = inputSheet.range('I7').value
    inputs['U_width'] = inputSheet.range('I8').value
    inputs['U_Wing_width'] = inputSheet.range('I9').value
    inputs['U_thickness'] = inputSheet.range('I10').value
    
    # H Bracket
    inputs['H_Section_List'] = inputSheet.range('Q6').value
    inputs['H_length'] = 0 if inputs['H_Section_List'] == 'none' else inputSheet.range('R11').value
    
    if inputs['H_Section_List'] == 'Built Up' or inputs['H_Section_List'] == 'None':
        inputs['H_height'] = inputSheet.range('R7').value
        inputs['H_width'] = inputSheet.range('R8').value
        inputs['H_Web_thickness'] = inputSheet.range('R9').value
        inputs['H_Flange_thickness'] = inputSheet.range('R10').value
    else:
        h_data = legacy_library.HBeamData[inputs['H_Section_List']]
        inputs['H_height'] = h_data['H']
        inputs['H_width'] = h_data['B']
        inputs['H_Web_thickness'] = h_data['t1']
        inputs['H_Flange_thickness'] = h_data['t2']
    
    # Slab
    inputs['Slab_depth'] = inputSheet.range('AA7').value
    
    # Rebar
    inputs['topRebarQuantity'] = inputSheet.range('Z9').value
    inputs['topRebarDiameter'] = inputSheet.range('AB9').value
    inputs['bottomRebarQuantity'] = inputSheet.range('Z10').value
    inputs['bottomRebarDiameter'] = inputSheet.range('AB10').value
    
    # Shear Connector
    inputs['studShearConnector_spacing'] = inputSheet.range('AA12').value
    inputs['angleShearConnector_spacing'] = inputSheet.range('AA13').value
    
    # Material
    inputs['U_steel'] = inputSheet.range('I16').value
    inputs['H_steel'] = inputSheet.range('I17').value
    inputs['Steel_elasticModulus'] = inputSheet.range('I18').value
    inputs['Concrete_compressiveStress'] = inputSheet.range('I19').value
    inputs['ReBar_yieldStress'] = inputSheet.range('I20').value
    
    # Design Condition
    inputs['endCondition'] = inputSheet.range('S16').value
    inputs['beamSupport'] = inputSheet.range('S17').value
    inputs['useageForVibration'] = inputSheet.range('S18').value
    
    # Design Load
    inputs['liveLoad_construction'] = inputSheet.range('Z16').value
    inputs['deadLoad_finish'] = inputSheet.range('Z17').value
    inputs['liveLoad_permanant'] = inputSheet.range('Z18').value
    
    # Member Forces
    inputs['manual_positiveMoment_Permanant'] = inputSheet.range('H26').value * 1000000
    inputs['manual_negativeMoment_Permanant'] = inputSheet.range('H27').value * 1000000
    inputs['manual_negativeMoment_Permanant_U'] = inputSheet.range('H28').value * 1000000
    inputs['manual_shearForce_Permanant'] = inputSheet.range('H29').value * 1000
    
    # Length and Spacing
    inputs['beamLength'] = inputSheet.range('R26').value
    inputs['spacing1'] = inputSheet.range('R27').value
    inputs['spacing2'] = inputSheet.range('R28').value
    
    wb.close()
    
    return inputs


def calculate_legacy_way(inputs):
    """레거시 방식으로 계산 (BestoDesign.py 로직)"""
    
    # 재료 물성 계산
    Steel_yieldStress = legacy_library.StructuralSteelYieldStress(
        steel=inputs['U_steel'], 
        thickness=inputs['U_thickness']
    )
    H_steelYieldStress = legacy_library.StructuralSteelYieldStress(
        steel=inputs['H_steel'], 
        thickness=inputs['H_Flange_thickness']
    )
    Steel_elasticModulus = inputs['Steel_elasticModulus']
    Concrete_compressiveStress = inputs['Concrete_compressiveStress']
    ReBar_yieldStress = inputs['ReBar_yieldStress']
    Concrete_elasticModulus = legacy_library.ConcreteElasticModulus(
        fck=Concrete_compressiveStress
    )
    
    # 단면 생성
    U_wing1 = legacy_library.SquareSection(
        height=inputs['U_thickness'], 
        width=inputs['U_Wing_width'] + inputs['U_thickness'], 
        x=(inputs['U_Wing_width'] + inputs['U_thickness'])/2, 
        y=inputs['U_height'] - inputs['U_thickness']/2
    )
    U_wing2 = legacy_library.SquareSection(
        height=inputs['U_thickness'], 
        width=inputs['U_Wing_width'] + inputs['U_thickness'], 
        x=inputs['U_width'] - (inputs['U_Wing_width'] + inputs['U_thickness'])/2, 
        y=inputs['U_height'] - inputs['U_thickness']/2
    )
    U_web1 = legacy_library.SquareSection(
        height=inputs['U_height'] - inputs['U_thickness'] * 2, 
        width=inputs['U_thickness'], 
        x=inputs['U_thickness']/2, 
        y=inputs['U_height']/2
    )
    U_web2 = legacy_library.SquareSection(
        height=inputs['U_height'] - inputs['U_thickness'] * 2, 
        width=inputs['U_thickness'], 
        x=inputs['U_width'] - inputs['U_thickness']/2, 
        y=inputs['U_height']/2
    )
    U_bottomFlange = legacy_library.SquareSection(
        height=inputs['U_thickness'], 
        width=inputs['U_width'], 
        x=inputs['U_width']/2, 
        y=inputs['U_thickness']/2
    )
    U_section = legacy_library.CombinedSection(U_wing1, U_wing2, U_web1, U_web2, U_bottomFlange)
    
    # 콘크리트 단면 생성 (레거시와 동일하게)
    effectiveWidth = legacy_library.EffectiveWidth(
        span=inputs['beamLength'], 
        bay=inputs['spacing1']
    ) + legacy_library.EffectiveWidth(
        span=inputs['beamLength'], 
        bay=inputs['spacing2']
    )
    concInU = legacy_library.SquareSection(
        height=inputs['U_height'] - inputs['U_thickness'], 
        width=inputs['U_width'] - 2*inputs['U_thickness'], 
        x=inputs['U_Wing_width'] + inputs['U_width']/2, 
        y=(inputs['U_height'] - inputs['U_thickness'])/2 + inputs['U_thickness']
    )
    concSlab = legacy_library.SquareSection(
        height=inputs['Slab_depth'], 
        width=effectiveWidth, 
        x=inputs['U_Wing_width'] + inputs['U_width']/2, 
        y=inputs['U_height'] + inputs['Slab_depth']/2
    )
    C_section = legacy_library.CombinedSection(concInU, concSlab)
    
    # 하중 계산 (레거시와 동일하게)
    weight_U_Section = U_section.area/10**6 * 78.5
    weight_C_section = (concInU.area + inputs['Slab_depth'] * (inputs['spacing1'] + inputs['spacing2']) / 2)/10**6 * 24
    weightDeadLoad1 = weight_C_section + weight_U_Section
    weightConstructionLoad = (inputs['spacing1'] + inputs['spacing2']) / 2 / 1000 * inputs['liveLoad_construction']
    
    # 시공중 하중
    beamForce_Construction = legacy_library.BeamForceCalculator(inputs['beamLength'])
    if inputs['beamSupport'] == 0:
        centerMoment_Construction = abs(beamForce_Construction.calculate_forces(
            load_type="Uniform", 
            support_type=inputs['endCondition'], 
            position=inputs['beamLength']/2, 
            lineLoad=1.2 * weightDeadLoad1 + 1.6 * weightConstructionLoad
        )["Moment"])
    else:
        centerMoment_Construction = 0
    
    # U단면 정모멘트 검토
    U_nominalMomentStrength_Positive = legacy_library.NominalMomentStrength_6(
        section=U_section, 
        flange=U_wing1, 
        Steel_elasticModulus=Steel_elasticModulus, 
        Steel_yieldStress=Steel_yieldStress, 
        direction="P", 
        typeNumber=3
    )
    U_designMomentStrength_Positive = legacy_library.DesignMomentStrength(
        U_nominalMomentStrength_Positive.elasticMomentStrength
    )
    
    # AS12 값 (kN·m)
    AS12_value = round(U_designMomentStrength_Positive/1000000, 2)
    
    return {
        'AS12': AS12_value,
        'U_designMomentStrength_Positive': U_designMomentStrength_Positive,
        'U_nominalMomentStrength_Positive': U_nominalMomentStrength_Positive.elasticMomentStrength,
        'Steel_yieldStress': Steel_yieldStress,
        'Steel_elasticModulus': Steel_elasticModulus,
        'centerMoment_Construction': centerMoment_Construction,
        'U_section': U_section,
    }


def calculate_current_way(inputs):
    """현재 프로젝트 방식으로 계산 (py_main.py 로직 직접 구현)"""
    
    # 재료 물성 (레거시와 동일하게 계산)
    Steel_yieldStress_U = StructuralSteelYieldStress(
        steel=inputs['U_steel'], 
        thickness=inputs['U_thickness']
    )
    Steel_yieldStress_H = StructuralSteelYieldStress(
        steel=inputs['H_steel'], 
        thickness=inputs['H_Flange_thickness']
    )
    Steel_elasticModulus = inputs['Steel_elasticModulus']
    Concrete_compressiveStress = inputs['Concrete_compressiveStress']
    E_c = ConcreteElasticModulus(Concrete_compressiveStress)
    
    # H형강 정보
    if inputs['H_Section_List'] != 'Built Up' and inputs['H_Section_List'] != 'None':
        h_section_name = inputs['H_Section_List']
        h_data = HBeamData.get(h_section_name)
        if not h_data:
            raise ValueError(f'H-section {h_section_name} not found')
        H_height = h_data['H']
        H_width = h_data['B']
        H_web_thickness = h_data['t1']
        H_flange_thickness = h_data['t2']
    else:
        H_height = inputs['H_height']
        H_width = inputs['H_width']
        H_web_thickness = inputs['H_Web_thickness']
        H_flange_thickness = inputs['H_Flange_thickness']
        h_section_name = 'Built Up'
    
    # U형강 정보 (레거시와 동일하게 엑셀에서 읽은 값 사용)
    U_height = inputs['U_height']
    U_width = inputs['U_width']
    U_wing_width = inputs['U_Wing_width']
    U_thickness = inputs['U_thickness']
    
    # 단면 생성 (현재 프로젝트 방식)
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
    weight_U_section = U_section.area / 1e6 * 78.5
    
    # 콘크리트 단면
    effective_width = EffectiveWidth(span=inputs['beamLength'], bay=inputs['spacing1']) + EffectiveWidth(span=inputs['beamLength'], bay=inputs['spacing2'])
    conc_in_U = SquareSection(
        height=U_height - U_thickness, 
        width=U_width - 2 * U_thickness, 
        x=U_wing_width + U_width / 2, 
        y=(U_height - U_thickness) / 2 + U_thickness
    )
    weight_C_section = (conc_in_U.area + inputs['Slab_depth'] * (inputs['spacing1'] + inputs['spacing2']) / 2) / 1e6 * 24
    
    # 하중 계산
    weight_dead_load1 = weight_C_section + weight_U_section
    weight_construction_load = (inputs['spacing1'] + inputs['spacing2']) / 2 / 1000 * inputs['liveLoad_construction']
    
    # 시공중 하중
    beam_force_calc = BeamForceCalculator(inputs['beamLength'])
    factored_construction_load = 1.2 * weight_dead_load1 + 1.6 * weight_construction_load
    
    if inputs['beamSupport'] == 0:
        center_moment_construction = abs(beam_force_calc.calculate_forces(
            "Uniform", inputs['endCondition'], inputs['beamLength'] / 2, lineLoad=factored_construction_load
        )["Moment"])
    else:
        center_moment_construction = 0
    
    # U단면 정모멘트 검토
    U_nominal_M_positive = NominalMomentStrength_6(
        section=U_section, 
        flange=U_wing1, 
        Steel_elasticModulus=Steel_elasticModulus, 
        Steel_yieldStress=Steel_yieldStress_U, 
        direction="P", 
        typeNumber=3
    )
    U_design_M_positive = DesignMomentStrength(U_nominal_M_positive.elasticMomentStrength)
    
    # AS12 값 (kN·m)
    AS12_value = round(U_design_M_positive / 1e6, 2)
    
    return {
        'AS12': AS12_value,
        'U_designMomentStrength_Positive': U_design_M_positive,
        'U_nominalMomentStrength_Positive': U_nominal_M_positive.elasticMomentStrength,
        'Steel_yieldStress': Steel_yieldStress_U,
        'Steel_elasticModulus': Steel_elasticModulus,
        'centerMoment_Construction': center_moment_construction,
        'U_section': U_section,
    }


def compare_results(legacy_result, current_result):
    """두 계산 결과 비교"""
    print("=" * 80)
    print("계산 결과 비교")
    print("=" * 80)
    
    print(f"\n[AS12 값 비교]")
    print(f"  레거시 방식: {legacy_result['AS12']:.2f} kN·m")
    print(f"  현재 방식:   {current_result['AS12']:.2f} kN·m")
    diff = abs(legacy_result['AS12'] - current_result['AS12'])
    diff_percent = (diff / legacy_result['AS12'] * 100) if legacy_result['AS12'] != 0 else 0
    print(f"  차이:        {diff:.2f} kN·m ({diff_percent:.2f}%)")
    
    print(f"\n[설계 모멘트 강도 비교]")
    print(f"  레거시 방식: {legacy_result['U_designMomentStrength_Positive']/1e6:.2f} kN·m")
    print(f"  현재 방식:   {current_result['U_designMomentStrength_Positive']/1e6:.2f} kN·m")
    diff = abs(legacy_result['U_designMomentStrength_Positive'] - current_result['U_designMomentStrength_Positive']) / 1e6
    print(f"  차이:        {diff:.2f} kN·m")
    
    print(f"\n[공칭 모멘트 강도 비교]")
    print(f"  레거시 방식: {legacy_result['U_nominalMomentStrength_Positive']/1e6:.2f} kN·m")
    print(f"  현재 방식:   {current_result['U_nominalMomentStrength_Positive']/1e6:.2f} kN·m")
    diff = abs(legacy_result['U_nominalMomentStrength_Positive'] - current_result['U_nominalMomentStrength_Positive']) / 1e6
    print(f"  차이:        {diff:.2f} kN·m")
    
    print(f"\n[항복강도 비교]")
    print(f"  레거시 방식: {legacy_result['Steel_yieldStress']:.2f} MPa")
    print(f"  현재 방식:   {current_result['Steel_yieldStress']:.2f} MPa")
    print(f"  차이:        {abs(legacy_result['Steel_yieldStress'] - current_result['Steel_yieldStress']):.2f} MPa")
    
    print(f"\n[탄성계수 비교]")
    print(f"  레거시 방식: {legacy_result['Steel_elasticModulus']:.2f} MPa")
    print(f"  현재 방식:   {current_result['Steel_elasticModulus']:.2f} MPa")
    print(f"  차이:        {abs(legacy_result['Steel_elasticModulus'] - current_result['Steel_elasticModulus']):.2f} MPa")
    
    print(f"\n[소요 모멘트 비교]")
    print(f"  레거시 방식: {legacy_result['centerMoment_Construction']/1e6:.2f} kN·m")
    print(f"  현재 방식:   {current_result['centerMoment_Construction']/1e6:.2f} kN·m")
    diff = abs(legacy_result['centerMoment_Construction'] - current_result['centerMoment_Construction']) / 1e6
    print(f"  차이:        {diff:.2f} kN·m")
    
    print("\n" + "=" * 80)

    print("=== 단면 특성 비교 ===")
    print(f"레거시 U_section.area: {legacy_result['U_section'].area}")
    print(f"현재 U_section.area: {current_result['U_section'].area}")
    print(f"레거시 sectionModulusX2: {legacy_result['U_section'].sectionModulusX2}")
    print(f"현재 sectionModulusX2: {current_result['U_section'].sectionModulusX2}")
    print(f"레거시 plasticSectionCoefficient: {legacy_result['U_section'].plasticSectionCoefficient}")
    print(f"현재 plasticSectionCoefficient: {current_result['U_section'].plasticSectionCoefficient}")
    print(f"레거시 plasticNeutralAxis: {legacy_result['U_section'].plasticNeutralAxis}")
    print(f"현재 plasticNeutralAxis: {current_result['U_section'].plasticNeutralAxis}")
    
    # 일치 여부 판정
    tolerance = 0.01  # 0.01 kN·m = 10 N·m
    is_match = abs(legacy_result['AS12'] - current_result['AS12']) < tolerance
    
    if is_match:
        print("[OK] AS12 값이 일치합니다!")
    else:
        print("[NG] AS12 값이 일치하지 않습니다.")
        print(f"  차이: {abs(legacy_result['AS12'] - current_result['AS12']):.4f} kN·m")


    return is_match



def main():
    """메인 함수"""
    excel_path = os.path.join(legacy_path, 'BestoDesign.xlsm')
    
    if not os.path.exists(excel_path):
        print(f"엑셀 파일을 찾을 수 없습니다: {excel_path}")
        return
    
    print("엑셀 파일에서 입력값 읽는 중...")
    inputs = read_excel_inputs(excel_path)
    
    print("\n레거시 방식으로 계산 중...")
    legacy_result = calculate_legacy_way(inputs)
    
    print("현재 프로젝트 방식으로 계산 중...")
    current_result = calculate_current_way(inputs)
    
    print("\n")
    is_match = compare_results(legacy_result, current_result)
    
    return is_match


if __name__ == "__main__":
    main()

