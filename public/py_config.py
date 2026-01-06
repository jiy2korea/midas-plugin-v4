"""
BESTO Design - 기본 설정값 및 상수
설계강도 계산에 필요하지만 UI에서 입력받지 않는 값들
"""

# ============================================================
# 재료 상수
# ============================================================

# 강재 탄성계수 (MPa)
STEEL_ELASTIC_MODULUS = 205000

# 콘크리트 강도 등급별 설계기준강도 (MPa)
CONCRETE_STRENGTH = {
    "C24": 24,
    "C27": 27,
    "C30": 30,
    "C35": 35,
    "C40": 40,
    "C50": 50,
}

# 철근 탄성계수 (MPa)
REBAR_ELASTIC_MODULUS = 200000


# ============================================================
# 기하 조건 (더미 기본값)
# ============================================================

# 보 길이 (mm) - 실제로는 MIDAS에서 가져오거나 UI에서 입력
DEFAULT_SPAN_LENGTH = 10000  # 10m

# Bay 간격 (mm) - 유효폭 계산용
DEFAULT_BAY_SPACING = 9000  # 9m

# 비지지 길이 (mm) - 횡좌굴 검토용 (슬래브로 구속되어 있다고 가정)
DEFAULT_UNBRACED_LENGTH = 0  # 완전 구속


# ============================================================
# 하중 조건 (더미 기본값)
# ============================================================

# 등분포 하중 (N/mm = kN/m)
DEFAULT_UNIFORM_LOAD = 30  # 30 kN/m

# 시공단계 하중 (N/mm²) - 상부플랜지 시공하중 검토용
DEFAULT_CONSTRUCTION_LOAD = 0.005  # 5 kN/m² = 0.005 N/mm²


# ============================================================
# 전단연결재 규격 (더미 기본값)
# ============================================================

# 스터드 앵커 규격
STUD_ANCHOR = {
    "diameter": 19,       # 직경 (mm)
    "height": 100,        # 높이 (mm)  
    "area": 283.5,        # 단면적 (mm²) - π*19²/4
    "strength": 450,      # 인장강도 (MPa)
}

# 앵글 전단연결재 규격
ANGLE_CONNECTOR = {
    "height": 75,         # 앵글 높이 (mm)
    "U_width": 200,       # U형강 폭 (mm) - 단면에 따라 달라짐
}


# ============================================================
# 슬래브 조건 (더미 기본값)
# ============================================================

# 슬래브 피복두께 (mm)
DEFAULT_SLAB_COVER = 40

# 철근 피복두께 (mm)
DEFAULT_REBAR_COVER = 33


# ============================================================
# 안전계수 및 설계 상수
# ============================================================

# 강도감소계수
PHI_FLEXURE = 0.9    # 휨
PHI_SHEAR = 0.9      # 전단
PHI_COMPRESSION = 0.75  # 압축

# 횡좌굴 모멘트 수정계수
CB_DEFAULT = 1.0


# ============================================================
# 사용성 기준
# ============================================================

# 처짐 제한 (span/ratio)
DEFLECTION_LIMIT_RATIO = 360  # L/360

# 진동 검토 용도
DEFAULT_USAGE = "사무실"


# ============================================================
# U형강 단면 생성 헬퍼 함수
# ============================================================

def create_u_section_squares(u_height, u_width, u_thickness):
    """
    U형강 단면을 SquareSection 객체들로 생성
    
    Args:
        u_height: U형강 높이 (mm)
        u_width: U형강 전체 폭 (mm)
        u_thickness: 판 두께 (mm)
    
    Returns:
        tuple: (wing1, wing2, web1, web2, bottom_flange) SquareSection 객체들
    """
    from py_library import SquareSection
    
    # 날개 (상부 돌출부)
    wing_width = 50  # 날개 폭 (고정값)
    wing1 = SquareSection(
        height=u_thickness,
        width=wing_width,
        x=wing_width / 2,
        y=u_height - u_thickness / 2
    )
    wing2 = SquareSection(
        height=u_thickness,
        width=wing_width,
        x=u_width - wing_width / 2,
        y=u_height - u_thickness / 2
    )
    
    # 웨브 (좌우 수직판)
    web_height = u_height - 2 * u_thickness
    web1 = SquareSection(
        height=web_height,
        width=u_thickness,
        x=u_thickness / 2,
        y=u_height / 2
    )
    web2 = SquareSection(
        height=web_height,
        width=u_thickness,
        x=u_width - u_thickness / 2,
        y=u_height / 2
    )
    
    # 하부 플랜지
    bottom_flange = SquareSection(
        height=u_thickness,
        width=u_width,
        x=u_width / 2,
        y=u_thickness / 2
    )
    
    return (wing1, wing2, web1, web2, bottom_flange)


def create_h_section_squares(h_data):
    """
    H형강 단면을 SquareSection 객체들로 생성
    
    Args:
        h_data: HBeamData 딕셔너리 항목
    
    Returns:
        tuple: (top_flange, web, bottom_flange) SquareSection 객체들
    """
    from py_library import SquareSection
    
    H = h_data["H"]
    B = h_data["B"]
    t1 = h_data["t1"]  # 웨브 두께
    t2 = h_data["t2"]  # 플랜지 두께
    
    # 상부 플랜지
    top_flange = SquareSection(
        height=t2,
        width=B,
        x=B / 2,
        y=H - t2 / 2
    )
    
    # 웨브
    web_height = H - 2 * t2
    web = SquareSection(
        height=web_height,
        width=t1,
        x=B / 2,
        y=H / 2
    )
    
    # 하부 플랜지
    bottom_flange = SquareSection(
        height=t2,
        width=B,
        x=B / 2,
        y=t2 / 2
    )
    
    return (top_flange, web, bottom_flange)


# ============================================================
# 설계강도 계산용 기본 입력값 딕셔너리
# ============================================================

def get_default_design_inputs():
    """
    설계강도 계산에 필요한 기본 입력값 반환
    UI에서 입력받지 않는 값들의 기본값
    """
    return {
        # 재료
        "steel_elastic_modulus": STEEL_ELASTIC_MODULUS,
        "rebar_elastic_modulus": REBAR_ELASTIC_MODULUS,
        
        # 기하
        "span_length": DEFAULT_SPAN_LENGTH,
        "bay_spacing": DEFAULT_BAY_SPACING,
        "unbraced_length": DEFAULT_UNBRACED_LENGTH,
        
        # 하중
        "uniform_load": DEFAULT_UNIFORM_LOAD,
        "construction_load": DEFAULT_CONSTRUCTION_LOAD,
        
        # 전단연결재
        "stud_diameter": STUD_ANCHOR["diameter"],
        "stud_area": STUD_ANCHOR["area"],
        "stud_strength": STUD_ANCHOR["strength"],
        "angle_height": ANGLE_CONNECTOR["height"],
        
        # 슬래브
        "slab_cover": DEFAULT_SLAB_COVER,
        "rebar_cover": DEFAULT_REBAR_COVER,
        
        # 안전계수
        "phi_flexure": PHI_FLEXURE,
        "phi_shear": PHI_SHEAR,
        
        # 사용성
        "deflection_limit_ratio": DEFLECTION_LIMIT_RATIO,
        "usage": DEFAULT_USAGE,
    }

