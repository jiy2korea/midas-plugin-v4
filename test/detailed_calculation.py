# -*- coding: utf-8 -*-
"""
H-600X200X11X17 단면 상세 계산 과정
모든 중간 계산 과정을 출력합니다.
"""
import sys
sys.path.insert(0, '../public')

import math
from py_library import (
    HBeamData,
    HBeamToUSectionMatch,
    SquareSection,
    CombinedSection,
)

print("=" * 70)
print("H-600X200X11X17 단면 상세 계산 과정")
print("=" * 70)

# ============================================================
# 1. 입력 데이터
# ============================================================
print("\n" + "=" * 70)
print("1. 입력 데이터")
print("=" * 70)

h_section_name = "H-600X200X11X17"
h_data = HBeamData[h_section_name]
u_match = HBeamToUSectionMatch[h_section_name]

# 재료 물성
steel_E = 205000  # MPa
steel_Fy = 355    # MPa

print(f"\n[재료 물성]")
print(f"  강재 탄성계수 E = {steel_E} MPa")
print(f"  강재 항복강도 Fy = {steel_Fy} MPa")

print(f"\n[H형강 정보: {h_section_name}]")
print(f"  H (높이) = {h_data['H']} mm")
print(f"  B (폭) = {h_data['B']} mm")
print(f"  t1 (웹두께) = {h_data['t1']} mm")
print(f"  t2 (플랜지두께) = {h_data['t2']} mm")
print(f"  A (단면적, 표준값) = {h_data['A']} cm² = {h_data['A'] * 100} mm²")
print(f"  Ix (단면2차모멘트, 표준값) = {h_data['Ix']} cm⁴ = {h_data['Ix'] * 10000} mm⁴")
print(f"  Zx (소성단면계수, 표준값) = {h_data['Zx']} cm³ = {h_data['Zx'] * 1000} mm³")

print(f"\n[U형강 정보]")
print(f"  U_height (높이) = {u_match['U_height']} mm")
print(f"  U_width (폭) = {u_match['U_width']} mm")
print(f"  U_thickness (두께) = {u_match['U_thickness']} mm")

U_wing_width = 80  # 날개폭
print(f"  U_wing_width (날개폭) = {U_wing_width} mm")

# ============================================================
# 2. H형강 단면 특성 계산
# ============================================================
print("\n" + "=" * 70)
print("2. H형강 단면 특성 계산")
print("=" * 70)

H = h_data['H']      # 600
B = h_data['B']      # 200
t1 = h_data['t1']    # 11 (웹두께)
t2 = h_data['t2']    # 17 (플랜지두께)

print(f"\n[단면 구성 요소]")
print(f"  - 상부 플랜지: 폭 B = {B} mm, 두께 t2 = {t2} mm")
print(f"  - 하부 플랜지: 폭 B = {B} mm, 두께 t2 = {t2} mm")
print(f"  - 웨브: 높이 hw = H - 2*t2 = {H} - 2×{t2} = {H - 2*t2} mm, 두께 t1 = {t1} mm")

# 각 요소 생성
H_top_flange = SquareSection(height=t2, width=B, x=B/2, y=H - t2/2)
H_bottom_flange = SquareSection(height=t2, width=B, x=B/2, y=t2/2)
H_web = SquareSection(height=H - 2*t2, width=t1, x=B/2, y=H/2)

print(f"\n[상부 플랜지]")
print(f"  height = {H_top_flange.height} mm")
print(f"  width = {H_top_flange.width} mm")
print(f"  centerX = {H_top_flange.centerX} mm")
print(f"  centerY = {H_top_flange.centerY} mm")
print(f"  area = height × width = {H_top_flange.height} × {H_top_flange.width} = {H_top_flange.area} mm²")
print(f"  inertiaX = width × height³ / 12 = {H_top_flange.width} × {H_top_flange.height}³ / 12 = {H_top_flange.inertiaX:.2f} mm⁴")

print(f"\n[하부 플랜지]")
print(f"  height = {H_bottom_flange.height} mm")
print(f"  width = {H_bottom_flange.width} mm")
print(f"  centerX = {H_bottom_flange.centerX} mm")
print(f"  centerY = {H_bottom_flange.centerY} mm")
print(f"  area = {H_bottom_flange.area} mm²")
print(f"  inertiaX = {H_bottom_flange.inertiaX:.2f} mm⁴")

print(f"\n[웨브]")
print(f"  height = {H_web.height} mm")
print(f"  width = {H_web.width} mm")
print(f"  centerX = {H_web.centerX} mm")
print(f"  centerY = {H_web.centerY} mm")
print(f"  area = {H_web.area} mm²")
print(f"  inertiaX = {H_web.inertiaX:.2f} mm⁴")

# 조합 단면
H_section = CombinedSection(H_top_flange, H_bottom_flange, H_web)

# 계산된 area 저장 (CombinedSection 생성 시 이미 계산됨)
A_calc = H_top_flange.area + H_bottom_flange.area + H_web.area

print(f"\n[H형강 조합단면 계산]")
print(f"  계산된 단면적 A_calc = {H_top_flange.area} + {H_bottom_flange.area} + {H_web.area}")
print(f"                       = {A_calc} mm²")
print(f"  ※ CombinedSection 생성 시 이 값으로 centerY와 inertiaX가 계산됨")

# py_main.py와 BestoDesign.py 방식을 따름: 단면적만 표준값으로 덮어쓰기
H_section.area = HBeamData[h_section_name]['A'] * 100  # cm² -> mm²
print(f"  표준 단면적 A (표준값) = {H_section.area} mm² (덮어씀)")
print(f"  ※ centerY와 inertiaX는 계산값 기준으로 유지됨")

# 도심 계산 (CombinedSection에서 이미 계산됨)
sum_Ay = (H_top_flange.area * H_top_flange.centerY + 
          H_bottom_flange.area * H_bottom_flange.centerY + 
          H_web.area * H_web.centerY)
print(f"\n  도심 계산:")
print(f"  ΣAy = {H_top_flange.area}×{H_top_flange.centerY} + {H_bottom_flange.area}×{H_bottom_flange.centerY} + {H_web.area}×{H_web.centerY}")
print(f"      = {sum_Ay:.2f} mm³")
print(f"  도심 y_c = ΣAy / A_calc = {sum_Ay:.2f} / {A_calc} = {H_section.centerY:.2f} mm")
print(f"  ※ 도심은 계산된 area 기준으로 계산되며, 이후 area를 표준값으로 덮어써도 변경되지 않음")

# 단면2차모멘트 계산 (평행축 정리)
print(f"\n  단면2차모멘트 Ix (평행축 정리):")
I_tf = H_top_flange.inertiaX + H_top_flange.area * (H_top_flange.centerY - H_section.centerY)**2
I_bf = H_bottom_flange.inertiaX + H_bottom_flange.area * (H_bottom_flange.centerY - H_section.centerY)**2
I_web = H_web.inertiaX + H_web.area * (H_web.centerY - H_section.centerY)**2

print(f"  상부플랜지: I_tf + A_tf × d² = {H_top_flange.inertiaX:.2f} + {H_top_flange.area} × ({H_top_flange.centerY:.2f} - {H_section.centerY:.2f})²")
print(f"            = {H_top_flange.inertiaX:.2f} + {H_top_flange.area} × {(H_top_flange.centerY - H_section.centerY)**2:.2f}")
print(f"            = {I_tf:.2f} mm⁴")

print(f"  하부플랜지: I_bf + A_bf × d² = {H_bottom_flange.inertiaX:.2f} + {H_bottom_flange.area} × ({H_bottom_flange.centerY:.2f} - {H_section.centerY:.2f})²")
print(f"            = {I_bf:.2f} mm⁴")

print(f"  웨브: I_web + A_web × d² = {H_web.inertiaX:.2f} + {H_web.area} × ({H_web.centerY:.2f} - {H_section.centerY:.2f})²")
print(f"      = {I_web:.2f} mm⁴")

print(f"\n  Ix_total (계산값) = {I_tf:.2f} + {I_bf:.2f} + {I_web:.2f}")
print(f"                  = {H_section.inertiaX:.2f} mm⁴")
print(f"                  = {H_section.inertiaX/10000:.2f} cm⁴")
print(f"  표준값 Ix = {h_data['Ix']} cm⁴")
print(f"  ※ CombinedSection 생성 시 계산된 area 기준으로 Ix가 계산됨")
print(f"  ※ py_main.py와 BestoDesign.py는 Ix는 계산값을 그대로 사용하고, 단면적만 표준값으로 덮어씁니다")

# 단면계수
c_top = H_section.topCoordinate - H_section.centerY
c_bot = H_section.centerY - H_section.bottomCoordinate
print(f"\n  c_top (도심에서 상단까지) = {H_section.topCoordinate} - {H_section.centerY:.2f} = {c_top:.2f} mm")
print(f"  c_bot (도심에서 하단까지) = {H_section.centerY:.2f} - {H_section.bottomCoordinate} = {c_bot:.2f} mm")
print(f"  Sx_top = Ix / c_top = {H_section.inertiaX:.2f} / {c_top:.2f} = {H_section.sectionModulusX1:.2f} mm³")
print(f"  Sx_bot = Ix / c_bot = {H_section.inertiaX:.2f} / {c_bot:.2f} = {H_section.sectionModulusX2:.2f} mm³")

# 소성단면계수
print(f"\n  소성단면계수 Zx = {H_section.plasticSectionCoefficient:.2f} mm³")
print(f"                 = {H_section.plasticSectionCoefficient/1000:.2f} cm³")
print(f"  (표준값: {h_data['Zx']} cm³)")

# ============================================================
# 3. U형강 단면 특성 계산
# ============================================================
print("\n" + "=" * 70)
print("3. U형강 단면 특성 계산")
print("=" * 70)

U_height = u_match['U_height']      # 400
U_width = u_match['U_width']        # 250
U_thickness = u_match['U_thickness'] # 6

print(f"\n[단면 구성 요소]")
print(f"  - 좌측 날개 (wing1): 폭 = {U_wing_width + U_thickness} mm, 두께 = {U_thickness} mm")
print(f"  - 우측 날개 (wing2): 폭 = {U_wing_width + U_thickness} mm, 두께 = {U_thickness} mm")
print(f"  - 좌측 웨브 (web1): 높이 = {U_height - 2*U_thickness} mm, 두께 = {U_thickness} mm")
print(f"  - 우측 웨브 (web2): 높이 = {U_height - 2*U_thickness} mm, 두께 = {U_thickness} mm")
print(f"  - 하부 플랜지: 폭 = {U_width} mm, 두께 = {U_thickness} mm")

# 각 요소 생성
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

print(f"\n[좌측 날개 (wing1)]")
print(f"  height = {U_wing1.height} mm (두께)")
print(f"  width = {U_wing1.width} mm (폭)")
print(f"  centerX = {U_wing1.centerX} mm")
print(f"  centerY = {U_wing1.centerY} mm")
print(f"  area = {U_wing1.height} × {U_wing1.width} = {U_wing1.area} mm²")
print(f"  inertiaX = {U_wing1.width} × {U_wing1.height}³ / 12 = {U_wing1.inertiaX:.2f} mm⁴")

print(f"\n[우측 날개 (wing2)]")
print(f"  height = {U_wing2.height} mm")
print(f"  width = {U_wing2.width} mm")
print(f"  centerX = {U_wing2.centerX} mm")
print(f"  centerY = {U_wing2.centerY} mm")
print(f"  area = {U_wing2.area} mm²")
print(f"  inertiaX = {U_wing2.inertiaX:.2f} mm⁴")

print(f"\n[좌측 웨브 (web1)]")
print(f"  height = {U_web1.height} mm")
print(f"  width = {U_web1.width} mm")
print(f"  centerX = {U_web1.centerX} mm")
print(f"  centerY = {U_web1.centerY} mm")
print(f"  area = {U_web1.area} mm²")
print(f"  inertiaX = {U_web1.width} × {U_web1.height}³ / 12 = {U_web1.inertiaX:.2f} mm⁴")

print(f"\n[우측 웨브 (web2)]")
print(f"  height = {U_web2.height} mm")
print(f"  width = {U_web2.width} mm")
print(f"  centerX = {U_web2.centerX} mm")
print(f"  centerY = {U_web2.centerY} mm")
print(f"  area = {U_web2.area} mm²")
print(f"  inertiaX = {U_web2.inertiaX:.2f} mm⁴")

print(f"\n[하부 플랜지 (bottom_flange)]")
print(f"  height = {U_bottom_flange.height} mm")
print(f"  width = {U_bottom_flange.width} mm")
print(f"  centerX = {U_bottom_flange.centerX} mm")
print(f"  centerY = {U_bottom_flange.centerY} mm")
print(f"  area = {U_bottom_flange.area} mm²")
print(f"  inertiaX = {U_bottom_flange.inertiaX:.2f} mm⁴")

# 조합 단면
U_section = CombinedSection(U_wing1, U_wing2, U_web1, U_web2, U_bottom_flange)

print(f"\n[U형강 조합단면 계산]")
print(f"  총 단면적 A = {U_wing1.area} + {U_wing2.area} + {U_web1.area} + {U_web2.area} + {U_bottom_flange.area}")
print(f"             = {U_section.area} mm²")

# 도심 계산
sum_Ay_U = (U_wing1.area * U_wing1.centerY + 
            U_wing2.area * U_wing2.centerY +
            U_web1.area * U_web1.centerY + 
            U_web2.area * U_web2.centerY +
            U_bottom_flange.area * U_bottom_flange.centerY)
print(f"\n  ΣAy = {U_wing1.area}×{U_wing1.centerY} + {U_wing2.area}×{U_wing2.centerY} + {U_web1.area}×{U_web1.centerY} + {U_web2.area}×{U_web2.centerY} + {U_bottom_flange.area}×{U_bottom_flange.centerY}")
print(f"      = {sum_Ay_U:.2f} mm³")
print(f"  도심 y_c = ΣAy / A = {sum_Ay_U:.2f} / {U_section.area} = {U_section.centerY:.2f} mm")

# 단면2차모멘트 계산 (평행축 정리)
print(f"\n  단면2차모멘트 Ix (평행축 정리):")
elements = [
    ("wing1", U_wing1),
    ("wing2", U_wing2),
    ("web1", U_web1),
    ("web2", U_web2),
    ("bottom_flange", U_bottom_flange)
]

total_Ix = 0
for name, elem in elements:
    I_elem = elem.inertiaX + elem.area * (elem.centerY - U_section.centerY)**2
    d = elem.centerY - U_section.centerY
    print(f"  {name}: I + A × d² = {elem.inertiaX:.2f} + {elem.area} × ({d:.2f})² = {I_elem:.2f} mm⁴")
    total_Ix += I_elem

print(f"\n  Ix_total = {U_section.inertiaX:.2f} mm⁴")

# 단면계수
c_top_U = U_section.topCoordinate - U_section.centerY
c_bot_U = U_section.centerY - U_section.bottomCoordinate
print(f"\n  c_top (도심에서 상단까지) = {U_section.topCoordinate} - {U_section.centerY:.2f} = {c_top_U:.2f} mm")
print(f"  c_bot (도심에서 하단까지) = {U_section.centerY:.2f} - {U_section.bottomCoordinate} = {c_bot_U:.2f} mm")
print(f"  Sx_top = Ix / c_top = {U_section.inertiaX:.2f} / {c_top_U:.2f} = {U_section.sectionModulusX1:.2f} mm³")
print(f"  Sx_bot = Ix / c_bot = {U_section.inertiaX:.2f} / {c_bot_U:.2f} = {U_section.sectionModulusX2:.2f} mm³")

# 소성단면계수
print(f"\n  소성중립축 위치 = {U_section.plasticNeutralAxis:.2f} mm (하단 기준)")
print(f"  소성단면계수 Zx = {U_section.plasticSectionCoefficient:.2f} mm³")

# ============================================================
# 4. H형강 부모멘트 강도 계산
# ============================================================
print("\n" + "=" * 70)
print("4. H형강 부모멘트 강도 계산 [KDS 14 31 10, 4.3.2.1.1.2]")
print("=" * 70)

# 탄성모멘트강도
My_H = H_section.sectionModulusX1 * steel_Fy
print(f"\n[탄성모멘트강도 My]")
print(f"  My = Sx × Fy")
print(f"     = {H_section.sectionModulusX1:.2f} mm³ × {steel_Fy} MPa")
print(f"     = {My_H:.2f} N·mm")
print(f"     = {My_H/1e6:.2f} kN·m")

# 소성모멘트강도
Mp_H = H_section.plasticSectionCoefficient * steel_Fy
print(f"\n[소성모멘트강도 Mp]")
print(f"  Mp = Zx × Fy")
print(f"     = {H_section.plasticSectionCoefficient:.2f} mm³ × {steel_Fy} MPa")
print(f"     = {Mp_H:.2f} N·mm")
print(f"     = {Mp_H/1e6:.2f} kN·m")

# 횡좌굴 검토
H_length = 1500  # 브라켓 길이
Lb = H_length * 2  # 비지지 길이

# 회전반경
ry = (H_section.inertiaY / H_section.area) ** 0.5
print(f"\n[횡좌굴 검토]")
print(f"  비지지 길이 Lb = {Lb} mm")
print(f"  약축 회전반경 ry = √(Iy/A) = √({H_section.inertiaY:.2f}/{H_section.area}) = {ry:.2f} mm")

# 소성비지지길이 Lp
Lp = 1.76 * ry * (steel_E / steel_Fy) ** 0.5
print(f"\n  소성비지지길이 Lp = 1.76 × ry × √(E/Fy)")
print(f"                   = 1.76 × {ry:.2f} × √({steel_E}/{steel_Fy})")
print(f"                   = 1.76 × {ry:.2f} × {(steel_E/steel_Fy)**0.5:.2f}")
print(f"                   = {Lp:.2f} mm")

# 뒤틀림상수
Cw = H_section.height ** 2 * H_section.inertiaY / 4
J = H_section.torsionalConstant
ho = H_section.height
rts = ((H_section.inertiaY * Cw) ** 0.5 / H_section.sectionModulusX1) ** 0.5

print(f"\n  뒤틀림상수 Cw = h² × Iy / 4 = {H_section.height}² × {H_section.inertiaY:.2f} / 4 = {Cw:.2f} mm⁶")
print(f"  비틀림상수 J = Σ(b×t³/3) = {J:.2f} mm⁴")
print(f"  rts = √(√(Iy×Cw) / Sx) = {rts:.2f} mm")

# 탄성비지지길이 Lr
c = 1  # 이축대칭 단면
Lr = (1.95 * rts * (steel_E / (0.7 * steel_Fy)) 
      * (J / (H_section.sectionModulusX1 * ho)) ** 0.5
      * (1 + (1 + 6.76 * ((0.7 * steel_Fy / steel_E) 
      * (H_section.sectionModulusX1 * ho / J)) ** 2) ** 0.5) ** 0.5)

print(f"\n  탄성비지지길이 Lr = {Lr:.2f} mm")

# 횡좌굴강도 결정
if Lb <= Lp:
    Mn_LTB = Mp_H
    print(f"\n  Lb ({Lb}) ≤ Lp ({Lp:.2f}) → 소성영역")
    print(f"  횡좌굴강도 Mn = Mp = {Mn_LTB/1e6:.2f} kN·m")
elif Lb <= Lr:
    Mn_LTB = Mp_H - (Mp_H - 0.7 * steel_Fy * H_section.sectionModulusX1) * ((Lb - Lp) / (Lr - Lp))
    print(f"\n  Lp ({Lp:.2f}) < Lb ({Lb}) ≤ Lr ({Lr:.2f}) → 비탄성영역")
    print(f"  횡좌굴강도 Mn = Mp - (Mp - 0.7×Fy×Sx) × (Lb - Lp) / (Lr - Lp)")
    print(f"                = {Mp_H/1e6:.2f} - ({Mp_H/1e6:.2f} - 0.7×{steel_Fy}×{H_section.sectionModulusX1/1e6:.4f}) × ({Lb} - {Lp:.2f}) / ({Lr:.2f} - {Lp:.2f})")
    print(f"                = {Mn_LTB/1e6:.2f} kN·m")
else:
    Fcr = (math.pi**2 * steel_E / (Lb / rts)**2) * (1 + 0.078 * J / (H_section.sectionModulusX1 * ho) * (Lb / rts)**2) ** 0.5
    Mn_LTB = Fcr * H_section.sectionModulusX1
    print(f"\n  Lb ({Lb}) > Lr ({Lr:.2f}) → 탄성좌굴영역")
    print(f"  횡좌굴강도 Mn = {Mn_LTB/1e6:.2f} kN·m")

# 공칭휨강도
Mn_H = min(Mp_H, Mn_LTB)
print(f"\n[공칭휨강도 Mn]")
print(f"  Mn = min(Mp, Mn_LTB) = min({Mp_H/1e6:.2f}, {Mn_LTB/1e6:.2f}) = {Mn_H/1e6:.2f} kN·m")

# 설계휨강도
phi_b = 0.9
phi_Mn_H = phi_b * Mn_H
print(f"\n[설계휨강도 φMn]")
print(f"  φMn = φ × Mn = {phi_b} × {Mn_H/1e6:.2f} = {phi_Mn_H/1e6:.2f} kN·m")

# ============================================================
# 5. U형강 정모멘트 강도 계산
# ============================================================
print("\n" + "=" * 70)
print("5. U형강 정모멘트 강도 계산 [KDS 14 31 10, 4.3.2.1.1.6]")
print("=" * 70)

# 정모멘트: 상부가 압축 → 하단 단면계수 사용
Sx_U = U_section.sectionModulusX2  # 하단 기준 단면계수

# 탄성모멘트강도
My_U = Sx_U * steel_Fy
print(f"\n[탄성모멘트강도 My]")
print(f"  정모멘트: 상부 압축, 하부 인장")
print(f"  Sx (하단 기준) = {Sx_U:.2f} mm³")
print(f"  My = Sx × Fy")
print(f"     = {Sx_U:.2f} mm³ × {steel_Fy} MPa")
print(f"     = {My_U:.2f} N·mm")
print(f"     = {My_U/1e6:.2f} kN·m")

# 소성모멘트강도
Mp_U = U_section.plasticSectionCoefficient * steel_Fy
print(f"\n[소성모멘트강도 Mp]")
print(f"  Mp = Zx × Fy")
print(f"     = {U_section.plasticSectionCoefficient:.2f} mm³ × {steel_Fy} MPa")
print(f"     = {Mp_U:.2f} N·mm")
print(f"     = {Mp_U/1e6:.2f} kN·m")

# 항복모멘트강도 제한 (Mp ≤ 1.6My)
My_limit = 1.6 * My_U
print(f"\n[항복모멘트강도 제한]")
print(f"  1.6 × My = 1.6 × {My_U/1e6:.2f} = {My_limit/1e6:.2f} kN·m")
if Mp_U <= My_limit:
    My_yield = Mp_U
    print(f"  Mp ({Mp_U/1e6:.2f}) ≤ 1.6My ({My_limit/1e6:.2f}) → My_yield = Mp = {My_yield/1e6:.2f} kN·m")
else:
    My_yield = My_U
    print(f"  Mp ({Mp_U/1e6:.2f}) > 1.6My ({My_limit/1e6:.2f}) → My_yield = My = {My_yield/1e6:.2f} kN·m")

# 국부좌굴 검토 (플랜지 판폭두께비)
# 날개의 판폭두께비
b_f = U_wing1.width
t_f = U_wing1.height
lambda_f = b_f / t_f

# 조밀/비조밀 한계
lambda_p_f = 0.54 * (steel_E / steel_Fy) ** 0.5  # 표 4.3-2의 타입 3
lambda_r_f = 0.91 * (steel_E / steel_Fy) ** 0.5

print(f"\n[국부좌굴 검토 - 날개 (플랜지)]")
print(f"  b = {b_f} mm, t = {t_f} mm")
print(f"  λ = b/t = {b_f}/{t_f} = {lambda_f:.2f}")
print(f"  λp = 0.54 × √(E/Fy) = 0.54 × √({steel_E}/{steel_Fy}) = {lambda_p_f:.2f}")
print(f"  λr = 0.91 × √(E/Fy) = 0.91 × √({steel_E}/{steel_Fy}) = {lambda_r_f:.2f}")

if lambda_f <= lambda_p_f:
    classification = "Compact"
    Mn_local = My_U  # 탄성강도 사용
    print(f"  λ ({lambda_f:.2f}) ≤ λp ({lambda_p_f:.2f}) → {classification}")
    print(f"  국부좌굴강도 Mn = My = {Mn_local/1e6:.2f} kN·m")
elif lambda_f <= lambda_r_f:
    classification = "NonCompact"
    # 탄성강도(My) 기준으로 계산
    Mn_local = My_U - (My_U - 0.7 * steel_Fy * Sx_U) * (lambda_f - lambda_p_f) / (lambda_r_f - lambda_p_f)
    print(f"  λp ({lambda_p_f:.2f}) < λ ({lambda_f:.2f}) ≤ λr ({lambda_r_f:.2f}) → {classification}")
    print(f"  국부좌굴강도 Mn = My - (My - 0.7×Fy×Sx) × (λ - λp) / (λr - λp)")
    print(f"                 = {My_U/1e6:.2f} - ({My_U/1e6:.2f} - 0.7×{steel_Fy}×{Sx_U/1e6:.4f}) × ({lambda_f:.2f} - {lambda_p_f:.2f}) / ({lambda_r_f:.2f} - {lambda_p_f:.2f})")
    print(f"                 = {Mn_local/1e6:.2f} kN·m")
else:
    classification = "Slender"
    Mn_local = (0.69 * steel_E) / ((b_f / (2 * t_f)) ** 2) * Sx_U
    print(f"  λ ({lambda_f:.2f}) > λr ({lambda_r_f:.2f}) → {classification}")
    print(f"  국부좌굴강도 Mn = {Mn_local/1e6:.2f} kN·m")

# 공칭휨강도 (탄성강도 기준)
Mn_U = min(My_U, Mn_local)
print(f"\n[공칭휨강도 Mn (탄성강도 기준)]")
print(f"  Mn = min(My, Mn_local) = min({My_U/1e6:.2f}, {Mn_local/1e6:.2f}) = {Mn_U/1e6:.2f} kN·m")

# 설계휨강도
phi_Mn_U = phi_b * Mn_U
print(f"\n[설계휨강도 φMn]")
print(f"  φMn = φ × Mn = {phi_b} × {Mn_U/1e6:.2f} = {phi_Mn_U/1e6:.2f} kN·m")

# ============================================================
# 6. U형강 전단강도 계산
# ============================================================
print("\n" + "=" * 70)
print("6. U형강 전단강도 계산 [KDS 14 31 10, 4.3.2.1.2.2]")
print("=" * 70)

# 전단면적 (양측 웨브)
Aw = U_height * U_thickness * 2
print(f"\n[전단면적]")
print(f"  Aw = h × tw × 2 = {U_height} × {U_thickness} × 2 = {Aw} mm²")

# 웨브 세장비
h_web = U_web1.height
tw = U_web1.width
lambda_w = h_web / tw

print(f"\n[웨브 세장비]")
print(f"  h = {h_web} mm, tw = {tw} mm")
print(f"  h/tw = {h_web}/{tw} = {lambda_w:.2f}")

# 전단좌굴계수
kv = 5  # 비보강 웨브
print(f"\n[전단좌굴계수]")
print(f"  kv = {kv} (비보강 웨브)")

# 한계 세장비
lambda_1 = 1.10 * (kv * steel_E / steel_Fy) ** 0.5
lambda_2 = 1.37 * (kv * steel_E / steel_Fy) ** 0.5

print(f"\n[한계 세장비]")
print(f"  1.10 × √(kv×E/Fy) = 1.10 × √({kv}×{steel_E}/{steel_Fy}) = {lambda_1:.2f}")
print(f"  1.37 × √(kv×E/Fy) = 1.37 × √({kv}×{steel_E}/{steel_Fy}) = {lambda_2:.2f}")

# 전단계수 Cv
if lambda_w <= lambda_1:
    Cv = 1.0
    print(f"\n  h/tw ({lambda_w:.2f}) ≤ 1.10√(kv×E/Fy) ({lambda_1:.2f})")
    print(f"  → Cv = 1.0")
elif lambda_w <= lambda_2:
    Cv = 1.10 * (kv * steel_E / steel_Fy) ** 0.5 / lambda_w
    print(f"\n  1.10√(kv×E/Fy) ({lambda_1:.2f}) < h/tw ({lambda_w:.2f}) ≤ 1.37√(kv×E/Fy) ({lambda_2:.2f})")
    print(f"  → Cv = 1.10 × √(kv×E/Fy) / (h/tw)")
    print(f"       = 1.10 × √({kv}×{steel_E}/{steel_Fy}) / {lambda_w:.2f}")
    print(f"       = {Cv:.4f}")
else:
    Cv = 1.51 * kv * steel_E / (steel_Fy * lambda_w ** 2)
    print(f"\n  h/tw ({lambda_w:.2f}) > 1.37√(kv×E/Fy) ({lambda_2:.2f})")
    print(f"  → Cv = 1.51 × kv × E / (Fy × (h/tw)²)")
    print(f"       = 1.51 × {kv} × {steel_E} / ({steel_Fy} × {lambda_w:.2f}²)")
    print(f"       = {Cv:.4f}")

# 공칭전단강도
Vn = 0.6 * steel_Fy * Aw * Cv
print(f"\n[공칭전단강도 Vn]")
print(f"  Vn = 0.6 × Fy × Aw × Cv")
print(f"     = 0.6 × {steel_Fy} × {Aw} × {Cv:.4f}")
print(f"     = {Vn:.2f} N")
print(f"     = {Vn/1e3:.2f} kN")

# 설계전단강도
phi_v = 0.9
phi_Vn = phi_v * Vn
print(f"\n[설계전단강도 φVn]")
print(f"  φVn = φ × Vn = {phi_v} × {Vn/1e3:.2f} = {phi_Vn/1e3:.2f} kN")

# ============================================================
# 7. 시공중 검토용 설계강도 (탄성강도 기준)
# ============================================================
print("\n" + "=" * 70)
print("7. 시공중 검토용 설계강도 (탄성강도 기준)")
print("=" * 70)

# 시공중에는 탄성강도 사용
phi_My_H = phi_b * My_H  # H형강 탄성 설계휨강도
phi_My_U = phi_b * My_U  # U형강 탄성 설계휨강도

print(f"\n[H형강 부모멘트 (시공중 - 탄성강도)]")
print(f"  탄성모멘트강도 My = {My_H/1e6:.2f} kN·m")
print(f"  설계휨강도 φMy = φ × My = {phi_b} × {My_H/1e6:.2f} = {phi_My_H/1e6:.2f} kN·m")

print(f"\n[U형강 정모멘트 (시공중 - 탄성강도)]")
print(f"  탄성모멘트강도 My = {My_U/1e6:.2f} kN·m")
print(f"  설계휨강도 φMy = φ × My = {phi_b} × {My_U/1e6:.2f} = {phi_My_U/1e6:.2f} kN·m")

print(f"\n[U형강 전단강도]")
print(f"  설계전단강도 φVn = {phi_Vn/1e3:.2f} kN")

# ============================================================
# 8. 결과 요약
# ============================================================
print("\n" + "=" * 70)
print("8. 결과 요약")
print("=" * 70)

print(f"\n┌{'─'*68}┐")
print(f"│{'★ 시공중 검토 (탄성강도 기준)':^60}│")
print(f"├{'─'*68}┤")
print(f"│  H형강 탄성모멘트강도 My  = {My_H/1e6:>10.2f} kN·m{' '*22}│")
print(f"│  H형강 설계휨강도 φMy     = {phi_My_H/1e6:>10.2f} kN·m  ← 부모멘트 강도{' '*6}│")
print(f"├{'─'*68}┤")
print(f"│  U형강 탄성모멘트강도 My  = {My_U/1e6:>10.2f} kN·m{' '*22}│")
print(f"│  U형강 설계휨강도 φMy     = {phi_My_U/1e6:>10.2f} kN·m  ← 정모멘트 강도{' '*6}│")
print(f"├{'─'*68}┤")
print(f"│  U형강 설계전단강도 φVn   = {phi_Vn/1e3:>10.2f} kN   ← 전단 강도{' '*10}│")
print(f"└{'─'*68}┘")

print("\n" + "=" * 70)
print("계산 완료")
print("=" * 70)

