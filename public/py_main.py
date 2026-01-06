### do not delete this import scripts ###
import json
from py_base import set_g_values, get_g_values, requests_json, MidasAPI, Product
from py_base_sub import HelloWorld, ApiGet
### do not delete this import scripts ###

# BESTO Design Library import
from py_library import (
    HBeamData,
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
    StructuralSteelYieldStress
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
