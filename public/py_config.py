"""
BESTO Design - 기본 설정값 및 상수
설계강도 계산에 필요하지만 UI에서 입력받지 않는 값들
API연결 전 임시 사용을 위해 작성된 파일
"""

# ============================================================
# 설계강도 계산용 기본 입력값 딕셔너리
# ============================================================

def get_default_design_inputs():

    return {

        # H형강
        "selectedMember": "H-600X200X11X17",
        "h_bracket_length": 1700,
        
        # U형강
        "u_wing_width": 80,
        
        # 슬래브
        "slabDs": 150,
        
        # 철근
        "rebar_top_count": 0,
        "rebar_top_dia": 'D25',
        "rebar_bot_count": 0,
        "rebar_bot_dia": 'D25',
        
        # 전단연결재
        "stud_spacing": 200,
        "angle_spacing": 200,
        "angle_height": 50,
        "stud_diameter": 19,
        "stud_strength": 450,

        # 재료(강재)
        "steel_elastic_modulus": 205000,        
        "steelH": 'SM355',
        "steelU": 'SM355',
        
        #재료(콘크리트)        
        "concrete": 'C30',

        # 재료(철근)
        "rebar_yield_stress": 600,
        
        # 설계 조건
        "endCondition": 'Fix-Fix',
        "beamSupport": 0,
        "usageForVibration": '사무실',
        
        # 하중
        "liveLoadConstruction": 2.5,
        "deadLoadFinish": 1.5,
        "liveLoadPermanent": 2.5,
        "manualPositiveMoment": 0,
        "manualNegativeMoment": 0,
        "manualNegativeMomentU": 0,
        "manualShearForce": 0,

        # 기하
        "span_length": 10000,
        "bay_spacing1": 5000,
        "bay_spacing2": 5000,
    }


