/**
 * py_config.py의 기본값을 기반으로 한 부재 응력 정보 및 기하 정보
 * MIDAS에서 가져와야 할 값들을 py_config.py의 상수를 사용하여 생성
 */

// py_config.py의 기본값 (py_config.py에서 가져온 값)
const DEFAULT_SPAN_LENGTH = 10000; // 10m (mm)
const DEFAULT_UNIFORM_LOAD = 30; // 30 kN/m = 30 N/mm
const DEFAULT_UNBRACED_LENGTH = 0; // 완전 구속
const DEFLECTION_LIMIT_RATIO = 360; // L/360

// 부재 응력 정보 타입 정의
export interface MemberStressData {
  memberId: string;
  // Before Composite (시공전)
  beforeComposite: {
    mEnd: number; // 끝단 모멘트 (kN·m)
    mMid: number; // 중앙 모멘트 (kN·m)
    v: number;    // 전단력 (kN)
  };
  // After Composite (시공후)
  afterComposite: {
    mEnd: number; // 끝단 모멘트 (kN·m)
    mMid: number; // 중앙 모멘트 (kN·m)
    v: number;    // 전단력 (kN)
    delta: number; // 변위 (mm)
  };
}

// 부재 기하 정보 타입 정의
export interface MemberGeometryData {
  memberId: string;
  length: number; // 부재 길이 (m)
  lengthMm: number; // 부재 길이 (mm)
  sectionName: string; // 단면명
}

/**
 * 단순보 등분포하중에 의한 모멘트/전단력 계산
 * py_config.py의 DEFAULT_UNIFORM_LOAD와 DEFAULT_SPAN_LENGTH 사용
 */
const calculateSimpleBeamStresses = (
  length: number, // m
  uniformLoad: number = DEFAULT_UNIFORM_LOAD // kN/m
): { mMid: number; mEnd: number; v: number } => {
  const L = length; // m
  const w = uniformLoad; // kN/m
  
  // 단순보 계산
  // 중앙 모멘트: M = w*L²/8
  const mMid = (w * L * L) / 8; // kN·m
  // 끝단 모멘트: 0 (단순보)
  const mEnd = 0; // kN·m
  // 전단력: V = w*L/2
  const v = (w * L) / 2; // kN
  
  return { mMid, mEnd, v };
};

/**
 * 부재 ID로 응력 데이터 가져오기
 * py_config.py의 기본값을 사용하여 계산
 */
export const getMemberStressData = (memberId: string): MemberStressData => {
  // py_config.py의 DEFAULT_SPAN_LENGTH를 m 단위로 변환
  const lengthM = DEFAULT_SPAN_LENGTH / 1000; // 10m
  const lengthMm = DEFAULT_SPAN_LENGTH; // 10000mm
  
  // 시공전 응력 계산 (단순보)
  const beforeComposite = calculateSimpleBeamStresses(lengthM, DEFAULT_UNIFORM_LOAD);
  
  // 시공후 응력 계산 (더 큰 하중 가정)
  const afterCompositeLoad = DEFAULT_UNIFORM_LOAD * 1.5; // 시공후 하중 증가
  const afterComposite = calculateSimpleBeamStresses(lengthM, afterCompositeLoad);
  
  // 변위 계산 (간단한 근사: M*L²/(8*EI), 더미값 사용)
  const delta = (lengthM * 1000) / DEFLECTION_LIMIT_RATIO; // L/360 기준 근사값 (mm)
  
  return {
    memberId,
    beforeComposite: {
      mEnd: Math.round(beforeComposite.mEnd * 100) / 100,
      mMid: Math.round(beforeComposite.mMid * 100) / 100,
      v: Math.round(beforeComposite.v * 100) / 100,
    },
    afterComposite: {
      mEnd: Math.round(afterComposite.mEnd * 100) / 100,
      mMid: Math.round(afterComposite.mMid * 100) / 100,
      v: Math.round(afterComposite.v * 100) / 100,
      delta: Math.round(delta * 100) / 100,
    },
  };
};

/**
 * 부재 ID로 기하 데이터 가져오기
 * py_config.py의 DEFAULT_SPAN_LENGTH 사용
 */
export const getMemberGeometryData = (memberId: string): MemberGeometryData => {
  // py_config.py의 DEFAULT_SPAN_LENGTH 사용
  const lengthMm = DEFAULT_SPAN_LENGTH; // 10000 mm
  const lengthM = lengthMm / 1000; // 10 m
  
  return {
    memberId,
    length: lengthM, // m 단위
    lengthMm, // mm 단위
    sectionName: memberId,
  };
};

