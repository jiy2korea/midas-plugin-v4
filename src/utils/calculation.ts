/**
 * 단면 검증 계산 로직
 */

import { MemberStressData, MemberGeometryData } from '../data/memberData';

// 입력 데이터 타입
export interface CalculationInput {
  // 선택된 부재
  selectedMember: string;
  
  // 철근 정보
  rebarTopCount: string;
  rebarTopDia: string;
  rebarBotCount: string;
  rebarBotDia: string;
  fYr: string; // 철근 항복강도 (MPa)
  
  // 전단연결재
  studSpacing: string; // mm
  angleSpacing: string; // mm
  
  // 재료 및 구조
  fYU: string; // 상부 플랜지 항복강도 (MPa)
  fYH: string; // 웹 항복강도 (MPa)
  concrete: string; // 콘크리트 강도
  slabDs: string; // 슬래브 두께 (mm)
  slabBeff: string; // 유효폭 (mm)
  support: string; // 지지 조건
  
  // MIDAS에서 가져온 데이터
  stressData: MemberStressData;
  geometryData: MemberGeometryData;
}

// 계산 결과 타입
export interface CalculationResult {
  // H형강의 시공전 부모멘트 강도 (kN·m)
  hBeamNegativeMomentCapacity: number;
  
  // U형강의 시공전 정모멘트 강도 (kN·m)
  uBeamPositiveMomentCapacity: number;
  
  // U형강의 시공전 전단 강도 (kN)
  uBeamShearCapacity: number;
}

/**
 * H형강의 시공전 부모멘트 강도 계산
 */
const calculateHBeamNegativeMoment = (
  sectionName: string,
  fYH: number,
  stressData: MemberStressData
): number => {
  // 간단한 계산 예시 (실제로는 단면 속성과 설계 코드 기반 계산 필요)
  // H형강의 부모멘트 강도 = Z * fy (단순화된 공식)
  // 여기서는 더미 계산
  
  // H형강 명칭에서 높이 추출 (예: H-600X200X11X17 -> 600)
  const heightMatch = sectionName.match(/H-(\d+)X/);
  const height = heightMatch ? parseFloat(heightMatch[1]) : 300;
  
  // 단순화된 계산: Z ≈ bf * tf * (h - tf) + tw * (h - 2*tf)^2 / 4
  // 더미로 높이 기반 근사값 계산
  const sectionModulus = height * height * height / 6000; // 단순화된 근사식 (mm^3)
  const momentCapacity = (sectionModulus * fYH) / 1000000; // kN·m로 변환
  
  return Math.round(momentCapacity * 100) / 100;
};

/**
 * U형강의 시공전 정모멘트 강도 계산
 */
const calculateUBeamPositiveMoment = (
  fYU: number,
  stressData: MemberStressData
): number => {
  // U형강 정모멘트 강도 계산 (더미)
  // 단순화된 계산 예시
  const baseCapacity = 450; // 기본 용량 (kN·m)
  const fyFactor = fYU / 235; // 항복강도 비율
  const momentCapacity = baseCapacity * fyFactor;
  
  return Math.round(momentCapacity * 100) / 100;
};

/**
 * U형강의 시공전 전단 강도 계산
 */
const calculateUBeamShear = (
  sectionName: string,
  fYH: number,
  stressData: MemberStressData
): number => {
  // U형강 전단 강도 계산 (더미)
  // V = 0.6 * Aw * fy (단순화된 공식)
  
  // H형강 명칭에서 높이와 웹두께 추출
  const heightMatch = sectionName.match(/H-(\d+)X/);
  const webThicknessMatch = sectionName.match(/X\d+X\d+X(\d+)/);
  
  const height = heightMatch ? parseFloat(heightMatch[1]) : 300; // mm
  const webThickness = webThicknessMatch ? parseFloat(webThicknessMatch[1]) : 8; // mm
  
  const webArea = height * webThickness; // mm^2
  const shearCapacity = (0.6 * webArea * fYH) / 1000; // kN으로 변환
  
  return Math.round(shearCapacity * 100) / 100;
};

/**
 * 메인 계산 함수
 */
export const performCalculation = (input: CalculationInput): CalculationResult => {
  const fYH = parseFloat(input.fYH) || 235; // 기본값 235 MPa
  const fYU = parseFloat(input.fYU) || 235; // 기본값 235 MPa
  
  // 1. H형강의 시공전 부모멘트 강도 계산
  const hBeamNegativeMomentCapacity = calculateHBeamNegativeMoment(
    input.selectedMember,
    fYH,
    input.stressData
  );
  
  // 2. U형강의 시공전 정모멘트 강도 계산
  const uBeamPositiveMomentCapacity = calculateUBeamPositiveMoment(
    fYU,
    input.stressData
  );
  
  // 3. U형강의 시공전 전단 강도 계산
  const uBeamShearCapacity = calculateUBeamShear(
    input.selectedMember,
    fYH,
    input.stressData
  );
  
  return {
    hBeamNegativeMomentCapacity,
    uBeamPositiveMomentCapacity,
    uBeamShearCapacity,
  };
};

