import os, copy
import xlwings
import library
import math

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def  main():
    # -------------- 데이터 가져오기 --------------
    
    wb = xlwings.Book.caller()
    inputSheet = wb.sheets['design']
    shape_effctiveWidth = inputSheet.shapes['직사각형 25']

    # 1. Section

    # 1.1 BESTO
    U_height = inputSheet.range('I7').value
    U_width = inputSheet.range('I8').value
    U_Wing_width = inputSheet.range('I9').value
    U_thickness = inputSheet.range('I10').value    
    
    # 1.2 H Bracket
    H_Section_List = inputSheet.range('Q6').value
    H_length = 0 if H_Section_List == 'None' else inputSheet.range('R11').value
    if (H_Section_List == 'Built Up' or H_Section_List == 'None'):    
        H_height = inputSheet.range('R7').value
        H_width = inputSheet.range('R8').value
        H_Web_thickness = inputSheet.range('R9').value
        H_Flange_thickness = inputSheet.range('R10').value

    else:
        H_height = library.HBeamData[H_Section_List]['H']
        H_width = library.HBeamData[H_Section_List]['B']
        H_Web_thickness = library.HBeamData[H_Section_List]['t1']
        H_Flange_thickness = library.HBeamData[H_Section_List]['t2']
        inputSheet['R7'].value = round(H_height)
        inputSheet['R8'].value = round(H_width)
        inputSheet['R9'].value = round(H_Web_thickness)
        inputSheet['R10'].value = round(H_Flange_thickness)
        
    # 1.3 Slab
    Slab_depth = inputSheet.range('AA7').value
    
    # 1.4 Rebar
    topRebarQuantity = inputSheet.range('Z9').value
    topRebarDiameter = inputSheet.range('AB9').value
    topRebarArea = library.reBarArea[topRebarDiameter]
    bottomRebarQuantity = inputSheet.range('Z10').value
    bottomRebarDiameter = inputSheet.range('AB10').value
    bottomRebarArea = library.reBarArea[bottomRebarDiameter]
    rebarSpacingCheck = library.MinimumRebarSpacingCheck(
        beamwidth = U_width - U_thickness * 2,
        rebarDiameter = bottomRebarDiameter,
        rebarQuantity = bottomRebarQuantity
    )
    
    # 1.5 Shear Connector
    ShearConnector_height = 50
    studShearConnector_spacing = inputSheet.range('AA12').value
    angleShearConnector_spacing = inputSheet.range('AA13').value
    studAnchorYieldStress = 450

    # 2. Material
    U_steel = inputSheet.range('I16').value
    Steel_yieldStress = library.StructuralSteelYieldStress(steel=U_steel, thickness=U_thickness)
    H_steel = inputSheet.range('I17').value
    H_steelYieldStress = library.StructuralSteelYieldStress(steel=H_steel, thickness=H_Flange_thickness)
    Steel_elasticModulus = inputSheet.range('I18').value
    Concrete_compressiveStress = inputSheet.range('I19').value
    ReBar_yieldStress = inputSheet.range('I20').value
    Concrete_elasticModulus = library.ConcreteElasticModulus(fck = Concrete_compressiveStress)

    # 3. Design Condition
    endCondition = inputSheet.range('S16').value
    beamSupport = inputSheet.range('S17').value
    useageForVibration = inputSheet.range('S18').value

    # 4. Design Load
    liveLoad_construction = inputSheet.range('Z16').value     # 시공하중 [kN/m^2]
    deadLoad_finish = inputSheet.range('Z17').value           # 마감하중 [kN/m^2]    
    liveLoad_permanant = inputSheet.range('Z18').value        # 활하중   [kN/m^2]

    # 5. Member Forces
    manual_positiveMoment_Permanant = inputSheet.range('H26').value * 1000000
    manual_negativeMoment_Permanant = inputSheet.range('H27').value * 1000000
    manual_negativeMoment_Permanant_U = inputSheet.range('H28').value * 1000000
    manual_shearForce_Permanant = inputSheet.range('H29').value * 1000

    # 6. Length and Spacing
    beamLength = inputSheet.range('R26').value
    spacing1 = inputSheet.range('R27').value
    spacing2 = inputSheet.range('R28').value


    # -------------- 단면 생성 --------------

    # U단면    
    U_wing1 = library.SquareSection(height=U_thickness, width=U_Wing_width + U_thickness, x=(U_Wing_width + U_thickness)/2 , y=U_height - U_thickness/2)
    U_wing2 = library.SquareSection(height=U_thickness, width=U_Wing_width + U_thickness, x=U_width - (U_Wing_width + U_thickness)/2 , y=U_height - U_thickness/2)
    U_web1 = library.SquareSection(height=U_height - U_thickness * 2, width=U_thickness, x=U_thickness/2, y=U_height/2)
    U_web2 = library.SquareSection(height=U_height - U_thickness * 2, width=U_thickness, x=U_width - U_thickness/2, y=U_height/2)
    U_bottomFlange = library.SquareSection(height=U_thickness, width=U_width, x=U_width/2, y=U_thickness/2)
    U_section = library.CombinedSection(U_wing1, U_wing2, U_web1, U_web2, U_bottomFlange)
    weight_U_Section = U_section.area/10**6 * 78.5   # 단위길이당 하중 [kN/m]   강재의 단위중량 78.5 kN/m3

    # H단면
    H_topFlange = library.SquareSection(height=H_Flange_thickness, width=H_width, x=H_width/2, y=(H_height-H_Flange_thickness/2))
    H_bottomFlange = library.SquareSection(height=H_Flange_thickness, width=H_width, x=H_width/2, y=(H_Flange_thickness/2))
    H_web = library.SquareSection(height=(H_height-H_Flange_thickness*2), width=H_Web_thickness, x=H_width/2, y=H_height/2)
    H_section = library.CombinedSection(H_topFlange, H_bottomFlange, H_web)
    if (H_Section_List != 'Built Up' and H_Section_List != 'None'):
        H_section.area = library.HBeamData[H_Section_List]['A'] * 100
    weight_H_Section = H_section.area/10**6 * 78.5   # 단위길이당 하중 [kN/m]   강재의 단위중량 78.5 kN/m3
    inputSheet['Q3'].value = H_Section_List

    # 콘크리트 단면
    effectiveWidth = library.EffectiveWidth(span=beamLength, bay=spacing1) + library.EffectiveWidth(span=beamLength, bay=spacing2)         #유효폭
    concInU = library.SquareSection(height=U_height-U_thickness, width=U_width-2*U_thickness, x=U_Wing_width+U_width/2, y=(U_height-U_thickness)/2+U_thickness)
    concSlab = library.SquareSection(height=Slab_depth, width=effectiveWidth, x=U_Wing_width+U_width/2, y=U_height+Slab_depth/2)
    C_section = library.CombinedSection(concInU, concSlab)
    volumn_concInU = concInU.area * (beamLength - 3800)
    weight_C_section = (concInU.area + Slab_depth * (spacing1 + spacing2) / 2)/10**6 * 24   # 단위길이당 하중 [kN/m]    철근콘크리트 단위중량 24kN/m3
    
    # 합성 단면
    elasticModulusRatio = Steel_elasticModulus / Concrete_elasticModulus    # 강재/콘크리트 탄성계수비
    tranConcSection = copy.deepcopy(C_section)
    tranConcSection.area = C_section.area / elasticModulusRatio
    tranConcSection.inertiaX = C_section.inertiaX / elasticModulusRatio
    compositeSection = library.CombinedSection(U_section, tranConcSection)


    # -------------- 하중 계산 --------------
    
    # 단위길이당 하중
    weightLiveLoad = (spacing1 + spacing2) / 2 / 1000 * liveLoad_permanant              # 활하중 [kN/m] = [N/mm]
    weightDeadLoad1 = weight_C_section + weight_U_Section                               # 고정하중(데크플레이트, 토핑콘크리트, 강재보) [kN/m] = [N/mm]
    weightDeadLoad2 = (spacing1 + spacing2) / 2 / 1000 * deadLoad_finish                # 고정하중(콘크리트 양생 후 마감에 의한 고정하중) [kN/m] = [N/mm]
    weightConstructionLoad = (spacing1 + spacing2) / 2 / 1000 * liveLoad_construction   # 시공시 하중 [kN/m] = [N/mm]

    # 시공중 하중
    beamForce_Construction = library.BeamForceCalculator(beamLength)
    endMoment_Construction = abs(beamForce_Construction.calculate_forces(load_type="Uniform", support_type=endCondition, position=beamLength, lineLoad = 1.2 * weightDeadLoad1 + 1.6 * weightConstructionLoad)["Moment"]) if beamSupport == 0 else 0
    endMoment_U_Construction = abs(beamForce_Construction.calculate_forces(load_type="Uniform", support_type=endCondition, position=H_length, lineLoad = 1.2 * weightDeadLoad1 + 1.6 * weightConstructionLoad)["Moment"]) if beamSupport == 0 else 0
    centerMoment_Construction = abs(beamForce_Construction.calculate_forces(load_type="Uniform", support_type=endCondition, position=beamLength/2, lineLoad = 1.2 * weightDeadLoad1 + 1.6 * weightConstructionLoad)["Moment"]) if beamSupport == 0 else 0
    shear_Construction = abs(beamForce_Construction.calculate_forces(load_type="Uniform", support_type=endCondition, position=0, lineLoad = 1.2 * weightDeadLoad1 + 1.6 * weightConstructionLoad)["ShearForce"]) if beamSupport == 0 else 0
    
    # 시공후 하중
    endMoment_Permanant = manual_negativeMoment_Permanant
    endMoment_U_Permanant = manual_negativeMoment_Permanant_U
    centerMoment_Permanant = manual_positiveMoment_Permanant
    shear_Permanant = manual_shearForce_Permanant


    # -------------- 시공중 검토 -------------- 

    # U단면 모멘트 검토
    U_requiredMomentStrength_Construction_Positive = centerMoment_Construction
    U_nominalMomentStrength_Positive = library.NominalMomentStrength_6(section=U_section, flange=U_wing1, Steel_elasticModulus=Steel_elasticModulus, Steel_yieldStress=Steel_yieldStress, direction="P", typeNumber=3)
    U_designMomentStrength_Positive = library.DesignMomentStrength(U_nominalMomentStrength_Positive.elasticMomentStrength) # 시공시 탄성강도로 검토
    U_momentStrengthCheck_Positive = library.StrengthCheck(designStrength=U_designMomentStrength_Positive, requiredStrength=U_requiredMomentStrength_Construction_Positive)
        
    U_requiredMomentStrength_Construction_Negative = endMoment_U_Construction
    U_nominalMomentStrength_Negative = library.NominalMomentStrength_6(section=U_section, flange=U_bottomFlange, Steel_elasticModulus=Steel_elasticModulus, Steel_yieldStress=Steel_yieldStress, direction="N",typeNumber=8)
    U_designMomentStrength_Negative = library.DesignMomentStrength(U_nominalMomentStrength_Negative.elasticMomentStrength) # 시공시 탄성강도로 검토
    U_momentStrengthCheck_Negative = library.StrengthCheck(designStrength=U_designMomentStrength_Negative, requiredStrength=U_requiredMomentStrength_Construction_Negative)
                    
    # U단면 전단 검토
    U_requiredShearStrength_construction = shear_Construction
    U_nominalShearStrength = library.NominalShearStrength(square=U_web1,shearArea=U_height*U_thickness*2, yieldStress=Steel_yieldStress, elasticModulus=Steel_elasticModulus)
    U_designShearStrength = library.DesignShearStrength(U_nominalShearStrength.nominalShearStrength)
    U_shearCheck = library.StrengthCheck(designStrength=U_designShearStrength, requiredStrength=U_requiredShearStrength_construction)
            
    # H단면 모멘트 검토
    H_requiredMomentStrength_Construction_Positive = 0
    H_requiredMomentStrength_Construction_Negative = endMoment_Construction
    H_nominalMomentStrength = library.NominalMomentStrength_2(section=H_section, Steel_elasticModulus=Steel_elasticModulus, Steel_yieldStress=H_steelYieldStress, unbracedLength=H_length * 2)
    H_designMomentStrength_Construction_Positive = library.DesignMomentStrength(H_nominalMomentStrength.elasticMomentStrength)  # 시공시 탄성강도로 검토
    H_designMomentStrength_Construction_Negative = library.DesignMomentStrength(H_nominalMomentStrength.elasticMomentStrength)  # 시공시 탄성강도로 검토
    H_momentStrenthCheck_Positive = library.StrengthCheck(designStrength=H_designMomentStrength_Construction_Positive, requiredStrength=H_requiredMomentStrength_Construction_Positive)
    H_momentStrenthCheck_Negative = library.StrengthCheck(designStrength=H_designMomentStrength_Construction_Negative, requiredStrength=H_requiredMomentStrength_Construction_Negative)
    
    # H단면 전단 검토
    H_requiredShearStrength_construction = shear_Construction
    H_nominalShearStrength = library.NominalShearStrength(square=H_web, shearArea=H_height*H_Web_thickness ,yieldStress=H_steelYieldStress, elasticModulus=Steel_elasticModulus)
    H_designShearStrength = library.DesignShearStrength(H_nominalShearStrength.nominalShearStrength) / 0.9 # 2.24(E/Fy)^0.5 이상인 압연형강의 웨브 phi=1.0
    H_shearStrengthCheck = library.StrengthCheck(designStrength=H_designShearStrength, requiredStrength=H_requiredShearStrength_construction)
    
    # 처짐 검토
    requiredDeflection_construction = 40
    deflection_D1, error_D1 = library.Deflection(endCondition='Fix-Fix', load=(weightDeadLoad1), length=beamLength, elasticModulus=Steel_elasticModulus, inertia=U_section.inertiaX) if beamSupport == 0 else (0, None)
    deflection_C, error_C = library.Deflection(endCondition='Fix-Fix', load=(weightConstructionLoad), length=beamLength, elasticModulus=Steel_elasticModulus, inertia=U_section.inertiaX) if beamSupport == 0 else (0, None)
    deflectionCheck = library.ServiceabilityCheck(capacity=deflection_D1 + deflection_C, demand=requiredDeflection_construction)
    

    # -------------- 시공후 검토 --------------      

    # 전단연결재 강도
    studAnchorStrength = library.StudAnchorStrength(
        studAnchorArea = math.pi * (19/2)**2, # 스터드 지름 19mm
        f_ck = Concrete_compressiveStress,
        concreteElasticModulus = Concrete_elasticModulus,
        studAnchorStrength = studAnchorYieldStress, # 스터드 항복강도 MPa
    )
    
    angleAnchorStrength = library.AngleAnchorStrength(
        height=ShearConnector_height,
        U_width=U_width - U_Wing_width * 2,
        f_ck=Concrete_compressiveStress,
    )
        
    # U단면 전단연결재 강도
    if studShearConnector_spacing != 0:
        stud_count = math.floor((beamLength - H_length) / 2 / studShearConnector_spacing)
        stud_strength = studAnchorStrength * stud_count
    else:
        stud_strength = 0

    if angleShearConnector_spacing != 0:
        angle_count = math.floor((beamLength - H_length) / 2 / angleShearConnector_spacing)
        angle_strength = angleAnchorStrength * angle_count
    else:
        angle_strength = 0
    shearConnectorStrength = stud_strength + angle_strength
        
    # H단면 전단연결재 간격
    H_studAnchorRow = 2 if H_width > 210 else 1
    if topRebarQuantity == 0:
        H_studAnchorSpacing = None
    else:
        H_studAnchorSpacing = (H_length - 700) / math.ceil(topRebarArea * topRebarQuantity * ReBar_yieldStress / studAnchorStrength / H_studAnchorRow)

    #합성단면 정모멘트 검토
    Comp_requiredMomentStrength_Positive = centerMoment_Permanant
    Comp_web1WTRatio = library.WidthThicknessRatio(
            width=U_web1.height, 
            thickness=U_web1.width, 
            elasticModulus=Steel_elasticModulus, 
            yieldStress=Steel_yieldStress,
            typeNumber=6)
    Comp_web2WTRatio = library.WidthThicknessRatio(
            width=U_web2.height, 
            thickness=U_web2.width, 
            elasticModulus=Steel_elasticModulus, 
            yieldStress=Steel_yieldStress,
            typeNumber=6)
    Comp_nominalMomentStrength_Positive = library.CompositeSectionMomentStrength_positive(
        P_y = Steel_yieldStress * U_section.area, 
        P_rb = ReBar_yieldStress * bottomRebarQuantity * bottomRebarArea, 
        f_ck = Concrete_compressiveStress,
        A_s = concSlab.area, 
        Q_n = shearConnectorStrength, 
        b_eff = effectiveWidth, 
        d_s = Slab_depth, 
        F_y = Steel_yieldStress,
        steelSection = U_section,
        compressiveFlanges = (U_wing1, U_wing2),
        webs = (U_web1, U_web2),
        tensionRebarStrength = bottomRebarQuantity * bottomRebarArea * ReBar_yieldStress,
        widthThicknessRatio = [Comp_web1WTRatio.check(), Comp_web2WTRatio.check()]
        )
    Comp_designMomentStrength_Positive = library.DesignMomentStrength(Comp_nominalMomentStrength_Positive)
    Comp_momentStrengthCheck_Positive = library.StrengthCheck(designStrength=Comp_designMomentStrength_Positive, requiredStrength=Comp_requiredMomentStrength_Positive)
    
    # 합성단면 부모멘트 검토
    Comp_requiredMomentStrength_Negative = endMoment_U_Permanant
    Comp_bottomFlangeWTRatio = library.WidthThicknessRatio(
            width=U_bottomFlange.width, 
            thickness=U_bottomFlange.height, 
            elasticModulus=Steel_elasticModulus, 
            yieldStress=Steel_yieldStress,
            typeNumber=8)
    Comp_nominalMomentStrength_Negative = library.CompositeSectionMomentStrength_Negative(
        topRebarStrength = ReBar_yieldStress * topRebarQuantity * topRebarArea,
        Qn = shearConnectorStrength,
        Pyc = Steel_yieldStress * U_section.area,
        ds = Slab_depth,
        slabCoverConcreteDepth = 20,
        Fy = Steel_yieldStress,
        tensileFlanges = (U_wing1, U_wing2),
        webs = (U_web1, U_web2),
        steelSection = U_section,
        widthThicknessRatio = [Comp_web1WTRatio.check(), Comp_web2WTRatio.check(), Comp_bottomFlangeWTRatio.check()]
    )
    Comp_designMomentStrength_Negative = library.DesignMomentStrength(Comp_nominalMomentStrength_Negative)
    Comp_momentStrengthCheck_Negative = library.StrengthCheck(designStrength=Comp_designMomentStrength_Negative, requiredStrength=Comp_requiredMomentStrength_Negative)

    # 합성단면 전단 검토
    U_requiredShearStrength_permanent = shear_Permanant
    U_shearCheckPermanet = library.StrengthCheck(designStrength=U_designShearStrength, requiredStrength=U_requiredShearStrength_permanent)

    # H단면 부모멘트 검토
    H_requiredMomentStrength_Permanent_Negative = endMoment_Permanant
    H_bottomFlangeWTRatio = library.WidthThicknessRatio(
            width=H_bottomFlange.width/2, 
            thickness=H_bottomFlange.height, 
            elasticModulus=Steel_elasticModulus, 
            yieldStress=H_steelYieldStress,
            typeNumber=1)
    H_webWTRatio = library.WidthThicknessRatio(
            width=H_web.height, 
            thickness=H_web.width, 
            elasticModulus=Steel_elasticModulus, 
            yieldStress=H_steelYieldStress,
            typeNumber=6)
    H_nominalMomentStrength_Permanent_Negative = library.CompositeSectionMomentStrength_Negative(
        topRebarStrength = ReBar_yieldStress * topRebarQuantity * topRebarArea,
        Qn = shearConnectorStrength,
        Pyc = H_steelYieldStress * H_section.area,
        ds = Slab_depth,
        slabCoverConcreteDepth = 40,
        Fy = H_steelYieldStress,
        tensileFlanges = [H_topFlange],
        webs = [H_web],
        steelSection = H_section,
        widthThicknessRatio = [H_webWTRatio.check(), H_bottomFlangeWTRatio.check()]
    )
    H_designMomentStrength_Permanent_Negative = library.DesignMomentStrength(H_nominalMomentStrength_Permanent_Negative)
    H_momentStrengthCheck_Permanent_Negative = library.StrengthCheck(designStrength=H_designMomentStrength_Permanent_Negative, requiredStrength=H_requiredMomentStrength_Permanent_Negative)

    # H단면 전단 검토
    H_requiredShearStrength_permanent = shear_Permanant
    H_shearCheckPermanent = library.StrengthCheck(designStrength=H_designShearStrength, requiredStrength=H_requiredShearStrength_permanent)

    # 처짐 검토
    compositeRatio = min(shearConnectorStrength / min(Steel_yieldStress * U_section.area + ReBar_yieldStress * bottomRebarQuantity * bottomRebarArea, 0.85 * Concrete_compressiveStress * concSlab.area), 1)
    Comp_effctiveInertia = library.EffectiveInertia(steelSectionInertia = U_section.inertiaX, compositeRatio = compositeRatio, compositeSectionInertia = compositeSection.inertiaX)
    deflection_LiveLoad, error_LiveLoad = library.Deflection(endCondition='Fix-Fix', load=weightLiveLoad, length=beamLength, elasticModulus=Steel_elasticModulus, inertia=Comp_effctiveInertia)     #Es/Ec를 바탕으로 합성단면을 계산 했으므로, 탄성계수는 모두 steel 값 사용
    deflection_DeadNLive_Support, error_DeadNLive_Support = library.Deflection(endCondition='Fix-Fix', load=(weightLiveLoad + weightDeadLoad1 + weightDeadLoad2), length=beamLength, elasticModulus=Steel_elasticModulus, inertia=Comp_effctiveInertia)
    deflection_DeadNLive_NoSupport_temp1, error_DeadNLive_NoSupport_temp1 = library.Deflection(endCondition='Fix-Fix', load=(weightLiveLoad + weightDeadLoad2), length=beamLength, elasticModulus=Steel_elasticModulus, inertia=Comp_effctiveInertia)
    deflection_DeadNLive_NoSupport_temp2, error_DeadNLive_NoSupport_temp2 = library.Deflection(endCondition='Fix-Fix', load=weightDeadLoad1, length=beamLength, elasticModulus=Steel_elasticModulus, inertia=U_section.inertiaX)
    deflection_DeadNLive_NoSupport = deflection_DeadNLive_NoSupport_temp1 + deflection_DeadNLive_NoSupport_temp2
    deflectionCheck_LiveLoad = library.ServiceabilityCheck(capacity=deflection_LiveLoad,  demand=beamLength/360)
    deflectionCheck_DeadNLive_Support = library.ServiceabilityCheck(capacity=deflection_DeadNLive_Support, demand=beamLength/240)
    deflectionCheck_DeadNLive_NoSupport = library.ServiceabilityCheck(capacity=deflection_DeadNLive_NoSupport, demand=beamLength/240)

    # 진동 검토
    vibration = library.Vibration(useage=useageForVibration, deflection_L=deflection_LiveLoad, weight=200)

    # 비용 계산
    section1_length = beamLength - H_length * 2  # U단면 길이
    section2_length = H_length * 2  # H단면 길이
    cost_calc = library.CostCalculation(
        section1_length=section1_length,
        section2_length=section2_length,
        unitWeight_Section1=weight_U_Section,
        unitWeight_Section2=weight_H_Section,
        volumn_concInU=volumn_concInU,
        angleShearConnector_spacing=angleShearConnector_spacing,
        studShearConnector_spacing=studShearConnector_spacing,
        topRebarDiameter=topRebarDiameter,
        topRebarQuantity=topRebarQuantity,
        bottomRebarDiameter=bottomRebarDiameter,
        bottomRebarQuantity=bottomRebarQuantity,
        H_Section_List=H_Section_List,
        overlappedLength=500
    )
    
    print('end of the check')

    # ========================================================================
    # [임시 기능] 텍스트 파일 생성 - 입력값과 결과값 확인용 (줄바꿈으로 구분)
    # TODO: 나중에 삭제 예정
    # ========================================================================
    
    # 객체를 평탄화하는 함수
    def flatten_dict(obj, prefix='', sep='_'):
        flattened = {}
        for key, value in obj.items():
            new_key = f'{prefix}{sep}{key}' if prefix else key
            if isinstance(value, dict) and not isinstance(value, (list, tuple)):
                flattened.update(flatten_dict(value, new_key, sep))
            else:
                flattened[new_key] = value
        return flattened
    
    # 1. 파싱된 입력 데이터 딕셔너리 생성 (py_main.py와 동일한 구조)
    parsed_inputs = {
        'hSection': {
            'sectionName': H_Section_List if H_Section_List else 'None',
            'height': H_height,
            'width': H_width,
            'webThickness': H_Web_thickness,
            'flangeThickness': H_Flange_thickness,
            'bracketLength': H_length,
        },
        'uSection': {
            'height': U_height,
            'width': U_width,
            'wingWidth': U_Wing_width,
            'thickness': U_thickness,
        },
        'slab': {
            'depth': Slab_depth,
        },
        'rebar': {
            'top': {
                'quantity': topRebarQuantity,
                'diameter': topRebarDiameter,
                'diameterStr': f'D{int(topRebarDiameter)}' if topRebarDiameter else '',
                'area': topRebarArea if topRebarArea else 0,
            },
            'bottom': {
                'quantity': bottomRebarQuantity,
                'diameter': bottomRebarDiameter,
                'diameterStr': f'D{int(bottomRebarDiameter)}' if bottomRebarDiameter else '',
                'area': bottomRebarArea if bottomRebarArea else 0,
            },
            'yieldStress': ReBar_yieldStress,
        },
        'shearConnector': {
            'studSpacing': studShearConnector_spacing if studShearConnector_spacing else 0,
            'angleSpacing': angleShearConnector_spacing if angleShearConnector_spacing else 0,
            'angleHeight': ShearConnector_height,
            'studDiameter': 19,  # 하드코딩된 값
            'studStrength': studAnchorYieldStress,
        },
        'steel': {
            'elasticModulus': Steel_elasticModulus,
            'hType': H_steel if H_steel else None,
            'uType': U_steel if U_steel else None,
            'fyH': H_steelYieldStress,
            'fyU': Steel_yieldStress,
        },
        'concrete': {
            'grade': Concrete_compressiveStress,  # 변수명은 다르지만 값
            'fck': Concrete_compressiveStress,
            'elasticModulus': Concrete_elasticModulus,
        },
        'designCondition': {
            'endCondition': endCondition,
            'beamSupport': beamSupport,
            'usageForVibration': useageForVibration,
        },
        'loads': {
            'liveLoadConstruction': liveLoad_construction,
            'deadLoadFinish': deadLoad_finish,
            'liveLoadPermanent': liveLoad_permanant,
        },
        'manualForces': {
            'positiveMoment': manual_positiveMoment_Permanant,
            'negativeMoment': manual_negativeMoment_Permanant,
            'negativeMomentU': manual_negativeMoment_Permanant_U,
            'shearForce': manual_shearForce_Permanant,
        },
        'geometry': {
            'beamLength': beamLength,
            'spacing1': spacing1,
            'spacing2': spacing2,
        },
    }
    
    # 2. 결과 데이터 딕셔너리 생성 (py_main.py와 동일한 구조)
    result = {
        'sectionInfo': {
            'hSection': H_Section_List if H_Section_List else 'None',
            'uSection': f"U-{int(U_height)}x{int(U_width)}x{U_thickness}",
            'hArea': round(H_section.area, 2),
            'uArea': round(U_section.area, 2),
            'hInertia': round(H_section.inertiaX, 0),
            'uInertia': round(U_section.inertiaX, 0),
            'hModulusX1': round(H_section.sectionModulusX1, 2),
            'compositeInertia': round(compositeSection.inertiaX, 0),
            'effectiveWidth': round(effectiveWidth, 2),
        },
        'materialInfo': {
            'steelFyH': H_steelYieldStress,
            'steelFyU': Steel_yieldStress,
            'steelE': Steel_elasticModulus,
            'concrete': Concrete_compressiveStress,
            'fck': Concrete_compressiveStress,
            'Ec': round(Concrete_elasticModulus, 0),
            'fyr': ReBar_yieldStress,
        },
        'loads': {
            'weightDeadLoad1': round(weightDeadLoad1, 3),
            'weightDeadLoad2': round(weightDeadLoad2, 3),
            'weightLiveLoad': round(weightLiveLoad, 3),
            'weightConstructionLoad': round(weightConstructionLoad, 3),
        },
        'constructionStage': {
            'U_positive': {
                'requiredStrength': round(U_requiredMomentStrength_Construction_Positive / 1e6, 2),
                'nominalStrength': round(U_nominalMomentStrength_Positive.elasticMomentStrength / 1e6, 2),
                'designStrength': round(U_designMomentStrength_Positive / 1e6, 2),
            },
            'U_negative': {
                'requiredStrength': round(U_requiredMomentStrength_Construction_Negative / 1e6, 2),
                'nominalStrength': round(U_nominalMomentStrength_Negative.elasticMomentStrength / 1e6, 2),
                'designStrength': round(U_designMomentStrength_Negative / 1e6, 2),
            },
            'U_shear': {
                'requiredStrength': round(U_requiredShearStrength_construction / 1e3, 2),
                'nominalStrength': round(U_nominalShearStrength.nominalShearStrength / 1e3, 2),
                'designStrength': round(U_designShearStrength / 1e3, 2),
            },
            'H_negative': {
                'requiredStrength': round(H_requiredMomentStrength_Construction_Negative / 1e6, 2),
                'nominalStrength': round(H_nominalMomentStrength.elasticMomentStrength / 1e6, 2),
                'designStrength': round(H_designMomentStrength_Construction_Negative / 1e6, 2),
            },
            'H_shear': {
                'requiredStrength': round(H_requiredShearStrength_construction / 1e3, 2),
                'nominalStrength': round(H_nominalShearStrength.nominalShearStrength / 1e3, 2),
                'designStrength': round(H_designShearStrength / 1e3, 2),
            },
            'deflection': {
                'deflectionD1': round(deflection_D1, 2),
                'deflectionC': round(deflection_C, 2),
                'totalDeflection': round(deflection_D1 + deflection_C, 2),
                'limit': requiredDeflection_construction,
                'check': 'OK' if deflectionCheck else 'NG',
            },
        },
        'compositeStage': {
            'shearConnector': {
                'studCount': stud_count if studShearConnector_spacing != 0 else 0,
                'studUnitStrength': round(studAnchorStrength / 1e3, 2),
                'studTotalStrength': round(stud_strength / 1e3, 2) if studShearConnector_spacing != 0 else 0,
                'angleCount': angle_count if angleShearConnector_spacing != 0 else 0,
                'angleUnitStrength': round(angleAnchorStrength / 1e3, 2),
                'angleTotalStrength': round(angle_strength / 1e3, 2) if angleShearConnector_spacing != 0 else 0,
                'totalStrength': round(shearConnectorStrength / 1e3, 2),
            },
            'U_positive': {
                'requiredStrength': round(Comp_requiredMomentStrength_Positive / 1e6, 2),
                'nominalStrength': round(Comp_nominalMomentStrength_Positive / 1e6, 2),
                'designStrength': round(Comp_designMomentStrength_Positive / 1e6, 2),
            },
            'U_negative': {
                'requiredStrength': round(Comp_requiredMomentStrength_Negative / 1e6, 2),
                'nominalStrength': round(Comp_nominalMomentStrength_Negative / 1e6, 2),
                'designStrength': round(Comp_designMomentStrength_Negative / 1e6, 2),
            },
            'H_negative': {
                'requiredStrength': round(H_requiredMomentStrength_Permanent_Negative / 1e6, 2),
                'nominalStrength': round(H_nominalMomentStrength_Permanent_Negative / 1e6, 2),
                'designStrength': round(H_designMomentStrength_Permanent_Negative / 1e6, 2),
            },
            'shear': {
                'requiredStrength': round(U_requiredShearStrength_permanent / 1e3, 2),
                'designStrength': round(U_designShearStrength / 1e3, 2),
            },
            'deflection': {
                'compositeRatio': round(compositeRatio * 100, 1),
                'effectiveInertia': round(Comp_effctiveInertia, 0),
                'deflectionLive': round(deflection_LiveLoad, 2),
                'deflectionLiveLimit': round(beamLength / 360, 2),
                'deflectionLiveCheck': 'OK' if deflectionCheck_LiveLoad else 'NG',
                'deflectionDeadLive': round(deflection_DeadNLive_Support if beamSupport == 1 else deflection_DeadNLive_NoSupport, 2),
                'deflectionDeadLiveLimit': round(beamLength / 240, 2),
                'deflectionDeadLiveCheck': 'OK' if (deflectionCheck_DeadNLive_Support if beamSupport == 1 else deflectionCheck_DeadNLive_NoSupport) else 'NG',
            },
            'vibration': {
                'naturalFrequency': round(vibration.naturalFrequency, 2),
                'maxAccelerationRatio': round(vibration.maxAccelerationRatio * 100, 2),
                'accelerationLimit': round(vibration.accRatioLimit[useageForVibration] * 100, 1) if useageForVibration in vibration.accRatioLimit else 50.0,
            },
        },
    }
    
    # 3. 지정된 순서대로 키 목록 정의
    ordered_keys = [
        'INPUT_hSection_sectionName',
        'INPUT_hSection_height',
        'INPUT_hSection_width',
        'INPUT_hSection_webThickness',
        'INPUT_hSection_flangeThickness',
        'INPUT_hSection_bracketLength',
        'INPUT_uSection_height',
        'INPUT_uSection_width',
        'INPUT_uSection_wingWidth',
        'INPUT_uSection_thickness',
        'INPUT_slab_depth',
        'INPUT_rebar_top_quantity',
        'INPUT_rebar_top_diameter',
        'INPUT_rebar_top_diameterStr',
        'INPUT_rebar_top_area',
        'INPUT_rebar_bottom_quantity',
        'INPUT_rebar_bottom_diameter',
        'INPUT_rebar_bottom_diameterStr',
        'INPUT_rebar_bottom_area',
        'INPUT_rebar_yieldStress',
        'INPUT_shearConnector_studSpacing',
        'INPUT_shearConnector_angleSpacing',
        'INPUT_shearConnector_angleHeight',
        'INPUT_shearConnector_studDiameter',
        'INPUT_shearConnector_studStrength',
        'INPUT_steel_elasticModulus',
        'INPUT_steel_hType',
        'INPUT_steel_uType',
        'INPUT_steel_fyH',
        'INPUT_steel_fyU',
        'INPUT_concrete_grade',
        'INPUT_concrete_fck',
        'INPUT_concrete_elasticModulus',
        'INPUT_designCondition_endCondition',
        'INPUT_designCondition_beamSupport',
        'INPUT_designCondition_usageForVibration',
        'INPUT_loads_liveLoadConstruction',
        'INPUT_loads_deadLoadFinish',
        'INPUT_loads_liveLoadPermanent',
        'INPUT_manualForces_positiveMoment',
        'INPUT_manualForces_negativeMoment',
        'INPUT_manualForces_negativeMomentU',
        'INPUT_manualForces_shearForce',
        'INPUT_geometry_beamLength',
        'INPUT_geometry_spacing1',
        'INPUT_geometry_spacing2',
        'OUTPUT_sectionInfo_hSection',
        'OUTPUT_sectionInfo_uSection',
        'OUTPUT_sectionInfo_hArea',
        'OUTPUT_sectionInfo_uArea',
        'OUTPUT_sectionInfo_hInertia',
        'OUTPUT_sectionInfo_uInertia',
        'OUTPUT_sectionInfo_hModulusX1',
        'OUTPUT_sectionInfo_compositeInertia',
        'OUTPUT_sectionInfo_effectiveWidth',
        'OUTPUT_materialInfo_steelFyH',
        'OUTPUT_materialInfo_steelFyU',
        'OUTPUT_materialInfo_steelE',
        'OUTPUT_materialInfo_concrete',
        'OUTPUT_materialInfo_fck',
        'OUTPUT_materialInfo_Ec',
        'OUTPUT_materialInfo_fyr',
        'OUTPUT_loads_weightDeadLoad1',
        'OUTPUT_loads_weightDeadLoad2',
        'OUTPUT_loads_weightLiveLoad',
        'OUTPUT_loads_weightConstructionLoad',
        'OUTPUT_constructionStage_U_positive_requiredStrength',
        'OUTPUT_constructionStage_U_positive_nominalStrength',
        'OUTPUT_constructionStage_U_positive_designStrength',
        'OUTPUT_constructionStage_U_negative_requiredStrength',
        'OUTPUT_constructionStage_U_negative_nominalStrength',
        'OUTPUT_constructionStage_U_negative_designStrength',
        'OUTPUT_constructionStage_U_shear_requiredStrength',
        'OUTPUT_constructionStage_U_shear_nominalStrength',
        'OUTPUT_constructionStage_U_shear_designStrength',
        'OUTPUT_constructionStage_H_negative_requiredStrength',
        'OUTPUT_constructionStage_H_negative_nominalStrength',
        'OUTPUT_constructionStage_H_negative_designStrength',
        'OUTPUT_constructionStage_H_shear_requiredStrength',
        'OUTPUT_constructionStage_H_shear_nominalStrength',
        'OUTPUT_constructionStage_H_shear_designStrength',
        'OUTPUT_constructionStage_deflection_deflectionD1',
        'OUTPUT_constructionStage_deflection_deflectionC',
        'OUTPUT_constructionStage_deflection_totalDeflection',
        'OUTPUT_constructionStage_deflection_limit',
        'OUTPUT_constructionStage_deflection_check',
        'OUTPUT_compositeStage_shearConnector_studCount',
        'OUTPUT_compositeStage_shearConnector_studUnitStrength',
        'OUTPUT_compositeStage_shearConnector_studTotalStrength',
        'OUTPUT_compositeStage_shearConnector_angleCount',
        'OUTPUT_compositeStage_shearConnector_angleUnitStrength',
        'OUTPUT_compositeStage_shearConnector_angleTotalStrength',
        'OUTPUT_compositeStage_shearConnector_totalStrength',
        'OUTPUT_compositeStage_U_positive_requiredStrength',
        'OUTPUT_compositeStage_U_positive_nominalStrength',
        'OUTPUT_compositeStage_U_positive_designStrength',
        'OUTPUT_compositeStage_U_negative_requiredStrength',
        'OUTPUT_compositeStage_U_negative_nominalStrength',
        'OUTPUT_compositeStage_U_negative_designStrength',
        'OUTPUT_compositeStage_H_negative_requiredStrength',
        'OUTPUT_compositeStage_H_negative_nominalStrength',
        'OUTPUT_compositeStage_H_negative_designStrength',
        'OUTPUT_compositeStage_shear_requiredStrength',
        'OUTPUT_compositeStage_shear_designStrength',
        'OUTPUT_compositeStage_deflection_compositeRatio',
        'OUTPUT_compositeStage_deflection_effectiveInertia',
        'OUTPUT_compositeStage_deflection_deflectionLive',
        'OUTPUT_compositeStage_deflection_deflectionLiveLimit',
        'OUTPUT_compositeStage_deflection_deflectionLiveCheck',
        'OUTPUT_compositeStage_deflection_deflectionDeadLive',
        'OUTPUT_compositeStage_deflection_deflectionDeadLiveLimit',
        'OUTPUT_compositeStage_deflection_deflectionDeadLiveCheck',
        'OUTPUT_compositeStage_vibration_naturalFrequency',
        'OUTPUT_compositeStage_vibration_maxAccelerationRatio',
        'OUTPUT_compositeStage_vibration_accelerationLimit',
    ]
    
    # 4. 입력값과 결과값 평탄화
    input_flat = flatten_dict(parsed_inputs, 'INPUT')
    result_flat = flatten_dict(result, 'OUTPUT')
    
    # 5. 지정된 순서대로 텍스트 파일 생성 (값만 저장) - 일시 중지됨
    # lines = []
    # for key in ordered_keys:
    #     value = input_flat.get(key) if key.startswith('INPUT_') else result_flat.get(key, '')
    #     value_str = '' if value is None else str(value)
    #     lines.append(value_str)  # 키 없이 값만 저장
    # 
    # # 5. 파일 저장
    # from datetime import datetime
    # timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # filename = f'design_calculation_{timestamp}.txt'
    # filepath = os.path.join(os.path.dirname(__file__), filename)
    # 
    # with open(filepath, 'w', encoding='utf-8') as f:
    #     f.write('\n'.join(lines))
    # 
    # print(f'텍스트 파일이 생성되었습니다: {filepath}')
    # ========================================================================

    # -------------- 에러 메세지 --------------
    errorMessage = []
    if (H_width >= U_width):
        errorMessage.append('H단면의 폭은 U단면의 폭보다 작아야 합니다.')
    if (rebarSpacingCheck == False):
        errorMessage.append('하부 철근 간격이 너무 좁습니다.')
    if (0 < angleShearConnector_spacing <= 150):
        errorMessage.append('앵글 전단연결재 간격이 너무 좁습니다.')
    if (beamSupport == 1):
        errorMessage.append('서포트 사용으로 시공시 하중과 처짐이 0 처리되었습니다.') # 이건 너무 자주 뜰 것 같은데...
    
    # 처짐 관련 에러 메시지 추가
    if error_D1:
        errorMessage.append(f'시공시 고정하중 처짐 계산 오류: {error_D1}')
    if error_C:
        errorMessage.append(f'시공시 시공하중 처짐 계산 오류: {error_C}')
    if error_LiveLoad:
        errorMessage.append(f'활하중 처짐 계산 오류: {error_LiveLoad}')
    if error_DeadNLive_Support:
        errorMessage.append(f'지지보 합성단면 처짐 계산 오류: {error_DeadNLive_Support}')
    if error_DeadNLive_NoSupport_temp1 or error_DeadNLive_NoSupport_temp2:
        errorMessage.append(f'비지지보 합성단면 처짐 계산 오류: {error_DeadNLive_NoSupport_temp1 or error_DeadNLive_NoSupport_temp2}')


    # -------------- 텍스트 입력 --------------
    
    # 0. Demension
    shape_effctiveWidth.text = round(effectiveWidth, 2)    
    inputSheet['I11'].value = round(weight_U_Section*100, 2) # kg/m로 엑셀에 입력
    inputSheet['R12'].value = round(weight_H_Section*100, 2) # kg/m로 엑셀에 입력

    #  0. Section Properties
    #  1) U-section
    inputSheet['G35'].value = round(U_section.area, 2)
    inputSheet['G36'].value = round(U_section.inertiaX, 2)
    inputSheet['M36'].value = round(U_section.plasticSectionCoefficient, 2)
    inputSheet['G37'].value = round(U_section.sectionModulusX1, 2)
    inputSheet['M37'].value = round(U_section.sectionModulusX2, 2)
    inputSheet['G38'].value = round(U_section.centerY, 2)
    inputSheet['M38'].value = round(U_section.plasticNeutralAxis, 2)
    
    # 2) Composite section
    inputSheet['U35'].value = round(U_section.area + C_section.area, 2)
    inputSheet['U36'].value = round(compositeSection.inertiaX, 2)
    inputSheet['AA36'].value = round(compositeSection.plasticSectionCoefficient, 2)
    inputSheet['U37'].value = round(compositeSection.sectionModulusX1, 2)
    inputSheet['AA37'].value = round(compositeSection.sectionModulusX2, 2)
    inputSheet['U38'].value = round(compositeSection.centerY, 2)
    inputSheet['AA38'].value = round(compositeSection.plasticNeutralAxis, 2)

    #  3) H-section
    inputSheet['G42'].value = round(H_section.area, 2)
    inputSheet['G43'].value = round(H_section.inertiaX, 2)
    inputSheet['M43'].value = round(H_section.plasticSectionCoefficient, 2)
    inputSheet['G44'].value = round(H_section.sectionModulusX1, 2)
    inputSheet['M44'].value = round(H_section.sectionModulusX2, 2)
    inputSheet['G45'].value = round(H_section.centerY, 2)
    inputSheet['M45'].value = round(H_section.plasticNeutralAxis, 2)    
    
    #  1. Construction Stage
    #  1-1. U-section
    #  1) Positive Bending
    inputSheet['AS8'].value = round(U_nominalMomentStrength_Positive.elasticMomentStrength/1000000, 2)
    inputSheet['AO10'].value = round(U_nominalMomentStrength_Positive.flange_WTRatio.wtRatio, 2)
    inputSheet['AS10'].value = round(U_nominalMomentStrength_Positive.flange_WTRatio.lambda_p, 2)
    inputSheet['AW10'].value = round(U_nominalMomentStrength_Positive.flange_WTRatio.lambda_r, 2)
    inputSheet['BA10'].value = U_nominalMomentStrength_Positive.flange_WTRatio.check()
    inputSheet['AK12'].value = round(U_requiredMomentStrength_Construction_Positive/1000000, 2)
    inputSheet['AS12'].value = round(U_designMomentStrength_Positive/1000000, 2)
        
    #  2) Negative Bending
    inputSheet['AS15'].value = round(U_nominalMomentStrength_Negative.elasticMomentStrength/1000000, 2)
    # inputSheet['AZ15'].value = round(U_nominalMomentStrength_Negative.elasticMomentStrength/1000000 * 1.6, 2)
    # inputSheet['AS16'].value = round(U_nominalMomentStrength_Negative.localBucklingStrength/1000000, 2)
    inputSheet['AO17'].value = round(U_nominalMomentStrength_Negative.flange_WTRatio.wtRatio, 2)
    inputSheet['AS17'].value = round(U_nominalMomentStrength_Negative.flange_WTRatio.lambda_p, 2)
    inputSheet['AW17'].value = round(U_nominalMomentStrength_Negative.flange_WTRatio.lambda_r, 2)
    inputSheet['BA17'].value = U_nominalMomentStrength_Negative.flange_WTRatio.check()    
    inputSheet['AK19'].value = round(U_requiredMomentStrength_Construction_Negative/1000000, 2)
    inputSheet['AS19'].value = round(U_designMomentStrength_Negative/1000000, 2)
    
    #  3) Shear
    inputSheet['AS22'].value = round(U_nominalShearStrength.shearStrength/1000, 2)
    inputSheet['AS23'].value = round(U_nominalShearStrength.shearCoefficient, 2)
    inputSheet['AK24'].value = round(U_nominalShearStrength.slendernessRatio, 2)
    inputSheet['AS24'].value = round(U_nominalShearStrength.yieldLimit, 2)
    inputSheet['BA24'].value = round(U_nominalShearStrength.bucklingLimit, 2)
    inputSheet['AK26'].value = round(U_requiredShearStrength_construction/1000, 2)
    inputSheet['AS26'].value = round(U_designShearStrength/1000, 2)
    
    #  1-2. H-section
    #  1) Negative Bending
    inputSheet['AT31'].value = round(H_nominalMomentStrength.elasticMomentStrength/1000000, 2)
    inputSheet['AT32'].value = round(H_nominalMomentStrength.lateralBucklingStrength/1000000, 2)
    inputSheet['AK33'].value = round(H_nominalMomentStrength.unbracedLength/1000, 2)
    inputSheet['AQ33'].value = round(H_nominalMomentStrength.plasticUnbracedLength/1000, 2)
    inputSheet['AW33'].value = round(H_nominalMomentStrength.elasticUnbracedLength/1000, 2)
    inputSheet['AK35'].value = round(H_requiredMomentStrength_Construction_Negative/1000000, 2)
    inputSheet['AS35'].value = round(H_designMomentStrength_Construction_Negative/1000000, 2)

    #  2) Shear
    inputSheet['AS38'].value = round(H_nominalShearStrength.shearStrength/1000, 2)
    inputSheet['AS39'].value = round(H_nominalShearStrength.shearCoefficient, 2)
    inputSheet['AK40'].value = round(H_nominalShearStrength.slendernessRatio, 2)
    inputSheet['AS40'].value = round(H_nominalShearStrength.yieldLimit, 2)
    inputSheet['BA40'].value = round(H_nominalShearStrength.bucklingLimit, 2)
    inputSheet['AK42'].value = round(H_requiredShearStrength_construction/1000, 2)
    inputSheet['AS42'].value = round(H_designShearStrength/1000, 2)
    
    # 1-3. Deflection
    inputSheet['AR46'].value = round(deflection_D1, 1)
    inputSheet['AR47'].value = round(deflection_C, 1)
    inputSheet['AK49'].value = round(deflection_D1 + deflection_C, 1)
    inputSheet['AS49'].value = round(requiredDeflection_construction, 1)
    
    #  2. Composite Stage
    #  2-1. composite U-section
    #  1) Positive Bending
    inputSheet['BO8'].value = round(Comp_web1WTRatio.wtRatio, 2)
    inputSheet['BV8'].value = round(Comp_web1WTRatio.lambda_p, 2)
    inputSheet['CH8'].value = round(min(shearConnectorStrength / (Steel_yieldStress * U_section.area) * 100, 100), 2)
    inputSheet['BN10'].value = round(Comp_requiredMomentStrength_Positive/1000000, 2)
    inputSheet['BV10'].value = round(Comp_designMomentStrength_Positive/1000000, 2)
    
    #  2) Negative Bending    
    inputSheet['BQ13'].value = round(Comp_web1WTRatio.wtRatio, 2)
    inputSheet['BU13'].value = round(Comp_web1WTRatio.lambda_p, 2)
    inputSheet['BY13'].value = round(Comp_web1WTRatio.lambda_r, 2)
    inputSheet['CC13'].value = Comp_web1WTRatio.check()
    inputSheet['BQ14'].value = round(Comp_bottomFlangeWTRatio.wtRatio, 2)
    inputSheet['BU14'].value = round(Comp_bottomFlangeWTRatio.lambda_p, 2)
    inputSheet['BY14'].value = round(Comp_bottomFlangeWTRatio.lambda_r, 2)
    inputSheet['CC14'].value = Comp_bottomFlangeWTRatio.check()
    inputSheet['BN16'].value = round(Comp_requiredMomentStrength_Negative/1000000, 2)
    inputSheet['BV16'].value = round(Comp_designMomentStrength_Negative/1000000, 2)
    
    #  3) Shear
    inputSheet['BW18'].value = round(U_nominalShearStrength.shearStrength/1000, 2)
    inputSheet['BW19'].value = round(U_nominalShearStrength.shearCoefficient, 2)
    inputSheet['BN20'].value = round(U_nominalShearStrength.slendernessRatio, 2)
    inputSheet['BV20'].value = round(U_nominalShearStrength.yieldLimit, 2)
    inputSheet['CD20'].value = round(U_nominalShearStrength.bucklingLimit, 2)
    inputSheet['BN22'].value = round(U_requiredShearStrength_permanent/1000, 2)
    inputSheet['BV22'].value = round(U_designShearStrength/1000, 2)

    #  2-2. composite H-section
    #  1) Negative Bending
    inputSheet['BQ27'].value = round(H_webWTRatio.wtRatio, 2)
    inputSheet['BU27'].value = round(H_webWTRatio.lambda_p, 2)
    inputSheet['BY27'].value = round(H_webWTRatio.lambda_r, 2)
    inputSheet['CC27'].value = H_webWTRatio.check()
    inputSheet['BQ28'].value = round(H_bottomFlangeWTRatio.wtRatio, 2)
    inputSheet['BU28'].value = round(H_bottomFlangeWTRatio.lambda_p, 2)
    inputSheet['BY28'].value = round(H_bottomFlangeWTRatio.lambda_r, 2)
    inputSheet['CC28'].value = H_bottomFlangeWTRatio.check()
    inputSheet['BN30'].value = round(H_requiredMomentStrength_Permanent_Negative/1000000, 2)
    inputSheet['BV30'].value = round(H_designMomentStrength_Permanent_Negative/1000000, 2)
    inputSheet['BL32'].value = H_studAnchorRow
    inputSheet['BN32'].value = H_studAnchorSpacing
    
    #  2) Shear
    inputSheet['BW35'].value = round(H_nominalShearStrength.shearStrength/1000, 2)
    inputSheet['BW36'].value = round(H_nominalShearStrength.shearCoefficient, 2)
    inputSheet['BN37'].value = round(H_nominalShearStrength.slendernessRatio, 2)
    inputSheet['BV37'].value = round(H_nominalShearStrength.yieldLimit, 2)
    inputSheet['CD37'].value = round(H_nominalShearStrength.bucklingLimit, 2)
    inputSheet['BN39'].value = round(H_requiredShearStrength_permanent/1000, 2)
    inputSheet['BV39'].value = round(H_designShearStrength/1000, 2)
    
    #  2-3. Deflection
    inputSheet['BO42'].value = round(compositeRatio * 100, 1)
    inputSheet['BO43'].value = round(deflection_LiveLoad, 1)
    inputSheet['BV43'].value = round(beamLength / 360, 1)
    inputSheet['BO44'].value = round(deflection_DeadNLive_Support if beamSupport == 1 else deflection_DeadNLive_NoSupport, 1)
    inputSheet['BV44'].value = round(beamLength / 240, 1)
    
    #  2-4 Vibration
    inputSheet['BP47'].value = round(vibration.naturalFrequency,1)
    inputSheet['BP49'].value = round(vibration.maxAccelerationRatio * 100,2)
    inputSheet['BX49'].value = round(vibration.accRatioLimit[useageForVibration] * 100,1)
    
    # # 3-1. Weight
    # inputSheet['CO14'].value = round(cost_calc.weight_Section1/9800, 2)
    # inputSheet['CO15'].value = round(cost_calc.weight_Section2/9800, 2)
    # inputSheet['CO16'].value = round(cost_calc.bestoGirderSplice_weight/9800, 2)
    # inputSheet['CO17'].value = round(cost_calc.topRebar_weight/9800, 2)
    # inputSheet['CO18'].value = round(cost_calc.bottomRebar_weight/9800, 2)
    # inputSheet['CO19'].value = round(cost_calc.angle_weight/9800, 2)
    # inputSheet['CO20'].value = round(cost_calc.stud_number + cost_calc.section2_stud_Number, 0)
    # inputSheet['CO21'].value = round(volumn_concInU/10**9, 2)
    
    # # 3-2. Cost
    # inputSheet['CP14'].value = round(cost_calc.Section1_cost, 2)
    # inputSheet['CP15'].value = round(cost_calc.Section2_cost, 2)
    # inputSheet['CP16'].value = round(cost_calc.bestoGirderSplice_cost, 2)
    # inputSheet['CP17'].value = round(cost_calc.topRebar_cost, 2)
    # inputSheet['CP18'].value = round(cost_calc.bottomRebar_cost, 2)
    # inputSheet['CP19'].value = round(cost_calc.angle_cost, 2)
    # inputSheet['CP20'].value = round(cost_calc.stud_cost, 2)
    # inputSheet['CP21'].value = round(cost_calc.conc_cost, 2)
    # inputSheet['CP22'].value = round(cost_calc.totalCost, 2)

    # draw test
    # x = np.arange(1,5)
    # U_sectionList = [U_wing1, U_wing2, U_web1, U_web2, U_bottomFlange]
    # H_sectionList = [H_topFlange, H_bottomFlange, H_web]

    # fig, ax = plt.subplots(2,2)

    # ax[0][0].plot(x,x,'b^-')
    # ax[0][1].plot(x,x**2,'b^-')
    # for section in U_sectionList:
    #     ax[0][0].add_patch(
    #         patches.Rectangle(
    #             (section.leftCoordinate, section.bottomCoordinate),
    #             section.width, section.height,
    #             edgecolor = 'black',
    #             facecolor = 'white',
    #             fill = True,
    #         )
    #     )
        
    # for section in H_sectionList:
    #     ax[0][1].add_patch(
    #         patches.Rectangle(
    #             (section.leftCoordinate, section.bottomCoordinate),
    #             section.width, section.height,
    #             edgecolor = 'black',
    #             facecolor = 'white',
    #             fill = True,
    #         )
    #     )
    # plt.show()


if  __name__== "__main__":
    current_path = os.getcwd()
    macro_file_path = os.path.join(current_path, "BestoDesign.xlsm")
    xlwings.Book(macro_file_path).set_mock_caller()    
    main()