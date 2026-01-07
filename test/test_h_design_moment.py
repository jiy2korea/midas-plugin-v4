"""
H단면 부모멘트 설계강도 계산 테스트
plugin()과 legacy() 함수를 비교하기 위한 테스트 파일
"""
import sys
import os

# 프로젝트 루트 경로를 sys.path에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
public_path = os.path.join(project_root, 'public')
legacy_path = os.path.join(project_root, 'test', 'legacy')

if public_path not in sys.path:
    sys.path.insert(0, public_path)
if legacy_path not in sys.path:
    sys.path.insert(0, legacy_path)

# plugin() 함수에 필요한 import (출처: public/py_main.py)
from py_library import (
    HBeamData,
    SquareSection,
    CombinedSection,
    NominalMomentStrength_2,
    DesignMomentStrength,
    StrengthCheck,
    StructuralSteelYieldStress,
)

# legacy() 함수에 필요한 import (출처: test/legacy/BestoDesign.py)
import library


def plugin(input_data):
    """
    H단면 부모멘트 설계강도 계산 (plugin 버전)
    출처: public/py_main.py의 H_design_M_negative 계산 코드 (386-395 라인)
    
    Args:
        input_data (dict): 입력 데이터 딕셔너리
            - h_section_name: H형강 이름 (예: 'H-400X200X8X13')
            - H_height: H형강 높이 [mm]
            - H_width: H형강 폭 [mm]
            - H_web_thickness: H형강 웹 두께 [mm]
            - H_flange_thickness: H형강 플랜지 두께 [mm]
            - H_length: H브라켓 길이 [mm]
            - steel_E: 강재 탄성계수 [MPa]
            - steel_Fy_H: H형강 항복강도 [MPa] 또는 steel_H_type (강종)
            - end_moment_construction: 시공중 부단부 모멘트 [N·mm]
    
    Returns:
        dict: 계산 결과
            - H_required_M_negative: 요구강도 [N·mm]
            - H_nominal_M: 공칭강도 객체
            - H_design_M_negative: 설계강도 [N·mm]
            - H_moment_check_negative: 강도 검토 결과 (True/False)
    """
    # 입력 데이터 추출
    h_section_name = input_data.get('h_section_name', 'H-400X200X8X13')
    H_height = input_data.get('H_height', 400)
    H_width = input_data.get('H_width', 200)
    H_web_thickness = input_data.get('H_web_thickness', 8)
    H_flange_thickness = input_data.get('H_flange_thickness', 13)
    H_length = input_data.get('H_length', 1700)
    steel_E = input_data.get('steel_E', 200000)
    steel_Fy_H_input = input_data.get('steel_Fy_H', 355)
    end_moment_construction = input_data.get('end_moment_construction', 0)
    
    # 강종이 제공되면 두께에 따라 항복강도 계산 (출처: py_main.py 149-152 라인)
    if isinstance(steel_Fy_H_input, str) and steel_Fy_H_input in ['SM355', 'SM420', 'SM460', 'SN355', 'SHN355']:
        steel_Fy_H = StructuralSteelYieldStress(steel=steel_Fy_H_input, thickness=H_flange_thickness)
    else:
        steel_Fy_H = float(steel_Fy_H_input)
    
    # H단면 생성 (출처: py_main.py 242-264 라인)
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
    
    # H단면 부모멘트 검토 (출처: py_main.py 386-395 라인)
    H_required_M_negative = end_moment_construction
    H_nominal_M = NominalMomentStrength_2(
        section=H_section, 
        Steel_elasticModulus=steel_E, 
        Steel_yieldStress=steel_Fy_H, 
        unbracedLength=H_length * 2
    )
    H_design_M_negative = DesignMomentStrength(H_nominal_M.elasticMomentStrength)
    H_moment_check_negative = StrengthCheck(H_design_M_negative, H_required_M_negative)
    
    return {
        'H_required_M_negative': H_required_M_negative,
        'H_nominal_M': H_nominal_M,
        'H_design_M_negative': H_design_M_negative,
        'H_moment_check_negative': H_moment_check_negative,
    }


def legacy(input_data):
    """
    H단면 부모멘트 설계강도 계산 (legacy 버전)
    출처: test/legacy/BestoDesign.py의 H_designMomentStrength_Construction_Negative 계산 코드 (175-182 라인)
    
    Args:
        input_data (dict): 입력 데이터 딕셔너리
            - H_Section_List: H형강 이름 (예: 'H-400X200X8X13') 또는 'Built Up', 'None'
            - H_height: H형강 높이 [mm]
            - H_width: H형강 폭 [mm]
            - H_Web_thickness: H형강 웹 두께 [mm]
            - H_Flange_thickness: H형강 플랜지 두께 [mm]
            - H_length: H브라켓 길이 [mm]
            - Steel_elasticModulus: 강재 탄성계수 [MPa]
            - H_steel: H형강 강종 (예: 'SM355', 'SM420' 등)
            - endMoment_Construction: 시공중 부단부 모멘트 [N·mm]
    
    Returns:
        dict: 계산 결과
            - H_requiredMomentStrength_Construction_Negative: 요구강도 [N·mm]
            - H_nominalMomentStrength: 공칭강도 객체
            - H_designMomentStrength_Construction_Negative: 설계강도 [N·mm]
            - H_momentStrenthCheck_Negative: 강도 검토 결과 (True/False)
    """
    # 입력 데이터 추출
    H_Section_List = input_data.get('H_Section_List', 'H-400X200X8X13')
    H_height = input_data.get('H_height', 400)
    H_width = input_data.get('H_width', 200)
    H_Web_thickness = input_data.get('H_Web_thickness', 8)
    H_Flange_thickness = input_data.get('H_Flange_thickness', 13)
    H_length = input_data.get('H_length', 1700)
    Steel_elasticModulus = input_data.get('Steel_elasticModulus', 200000)
    H_steel = input_data.get('H_steel', 'SM355')
    endMoment_Construction = input_data.get('endMoment_Construction', 0)
    
    # H형강 강종에 따른 항복강도 계산 (출처: BestoDesign.py 68-69 라인)
    H_steelYieldStress = library.StructuralSteelYieldStress(steel=H_steel, thickness=H_Flange_thickness)
    
    # H단면 생성 (출처: BestoDesign.py 108-115 라인)
    H_topFlange = library.SquareSection(
        height=H_Flange_thickness, 
        width=H_width, 
        x=H_width/2, 
        y=(H_height-H_Flange_thickness/2)
    )
    H_bottomFlange = library.SquareSection(
        height=H_Flange_thickness, 
        width=H_width, 
        x=H_width/2, 
        y=(H_Flange_thickness/2)
    )
    H_web = library.SquareSection(
        height=(H_height-H_Flange_thickness*2), 
        width=H_Web_thickness, 
        x=H_width/2, 
        y=H_height/2
    )
    H_section = library.CombinedSection(H_topFlange, H_bottomFlange, H_web)
    if (H_Section_List != 'Built Up' and H_Section_List != 'None'):
        H_section.area = library.HBeamData[H_Section_List]['A'] * 100
    
    # H단면 모멘트 검토 (출처: BestoDesign.py 175-182 라인)
    H_requiredMomentStrength_Construction_Positive = 0
    H_requiredMomentStrength_Construction_Negative = endMoment_Construction
    H_nominalMomentStrength = library.NominalMomentStrength_2(
        section=H_section, 
        Steel_elasticModulus=Steel_elasticModulus, 
        Steel_yieldStress=H_steelYieldStress, 
        unbracedLength=H_length * 2
    )
    H_designMomentStrength_Construction_Positive = library.DesignMomentStrength(H_nominalMomentStrength.elasticMomentStrength)  # 시공시 탄성강도로 검토
    H_designMomentStrength_Construction_Negative = library.DesignMomentStrength(H_nominalMomentStrength.elasticMomentStrength)  # 시공시 탄성강도로 검토
    H_momentStrenthCheck_Positive = library.StrengthCheck(
        designStrength=H_designMomentStrength_Construction_Positive, 
        requiredStrength=H_requiredMomentStrength_Construction_Positive
    )
    H_momentStrenthCheck_Negative = library.StrengthCheck(
        designStrength=H_designMomentStrength_Construction_Negative, 
        requiredStrength=H_requiredMomentStrength_Construction_Negative
    )
    
    return {
        'H_requiredMomentStrength_Construction_Negative': H_requiredMomentStrength_Construction_Negative,
        'H_nominalMomentStrength': H_nominalMomentStrength,
        'H_designMomentStrength_Construction_Negative': H_designMomentStrength_Construction_Negative,
        'H_momentStrenthCheck_Negative': H_momentStrenthCheck_Negative,
    }


# 테스트용 입력 데이터 (임의의 값)
plugin_input_data = {
    'h_section_name': 'H-600X200X11X17',
    'H_height': 600,
    'H_width': 200,
    'H_web_thickness': 11,
    'H_flange_thickness': 17,
    'H_length': 1700,
    'steel_E': 205000,
    'steel_Fy_H': 'SM355',  # 또는 숫자값 355
    'end_moment_construction': 50000000,  # 50 kN·m = 50,000,000 N·mm
}

legacy_input_data = {
    'H_Section_List': 'H-600X200X11X17',
    'H_height': 600,
    'H_width': 200,
    'H_Web_thickness': 11,
    'H_Flange_thickness': 17,
    'H_length': 1700,
    'Steel_elasticModulus': 205000,
    'H_steel': 'SM355',
    'endMoment_Construction': 50000000,  # 50 kN·m = 50,000,000 N·mm
}


if __name__ == '__main__':
    # 테스트 실행
    print("=== Plugin 버전 테스트 ===")
    plugin_result = plugin(plugin_input_data)
    print(f"요구강도: {plugin_result['H_required_M_negative'] / 1e6:.2f} kN·m")
    print(f"설계강도: {plugin_result['H_design_M_negative'] / 1e6:.2f} kN·m")
    print(f"검토결과: {'OK' if plugin_result['H_moment_check_negative'] else 'NG'}")
    
    print("\n=== Legacy 버전 테스트 ===")
    legacy_result = legacy(legacy_input_data)
    print(f"요구강도: {legacy_result['H_requiredMomentStrength_Construction_Negative'] / 1e6:.2f} kN·m")
    print(f"설계강도: {legacy_result['H_designMomentStrength_Construction_Negative'] / 1e6:.2f} kN·m")
    print(f"검토결과: {'OK' if legacy_result['H_momentStrenthCheck_Negative'] else 'NG'}")

