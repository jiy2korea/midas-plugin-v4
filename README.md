# MIDAS Plugin V4 - BESTO Design

MIDAS 플러그인으로 구현된 BESTO 합성보 설계 도구입니다.  
기존 Excel/Python 기반 계산 로직을 웹 기반 플러그인으로 이전했습니다.

---

## 📋 프로젝트 개요

### 목적
- 기존 `BestoDesign.py` + `library.py` 계산 로직을 MIDAS 플러그인으로 변환
- Pyscript를 활용하여 Python 코드를 브라우저에서 직접 실행
- React + TypeScript UI와 Python 계산 엔진 통합

### 기술 스택
| 구분 | 기술 |
|------|------|
| 프론트엔드 | React 18 + TypeScript |
| UI 라이브러리 | @midasit-dev/moaui |
| 계산 엔진 | Pyscript (Pyodide 기반) |
| 스타일링 | CSS + Tailwind |

---

## 📁 프로젝트 구조

```
Midas Plugin V4/
├── public/
│   ├── py_main.py          # Pyscript 엔트리 포인트
│   ├── py_library.py       # 구조 계산 라이브러리 (library.py 이전)
│   ├── py_base.py          # MIDAS API 기본 함수
│   ├── py_base_sub.py      # MIDAS API 서브 함수
│   ├── py_config.json      # Pyscript 설정
│   └── index.html          # HTML 템플릿
│
├── src/
│   ├── App.tsx             # 메인 UI 컴포넌트
│   ├── App.css             # 커스텀 스타일
│   ├── utils_pyscript.ts   # Python ↔ React 연결 유틸리티
│   ├── DevTools/           # 개발 도구
│   └── SampleComponents/   # 샘플 컴포넌트
│
├── package.json
└── README.md
```

---

## 🚀 시작하기

### 1. 의존성 설치
```bash
npm install
```

### 2. 개발 서버 실행
```bash
npm start
```

**PowerShell에서 실행:**
```powershell
cd "C:\Cursor Projects\Midas Plugin V4"; npm start
```

### 3. 브라우저에서 확인
```
http://localhost:3000
```

---

## 📊 주요 기능

### UI 기능
- [x] H형강 선택 드롭다운 (68개 규격)
- [x] 철근 정보 입력 (상부/하부, 개수, 직경)
- [x] 전단연결재 간격 입력 (스터드/앵글)
- [x] 재료 물성 선택 (강재, 콘크리트)
- [x] 슬래브 정보 입력 (깊이, 유효폭)
- [x] 지지 조건 선택
- [ ] 검색 결과 테이블
- [ ] 상세 정보 화면

### 계산 기능 (py_library.py)
- [x] H형강 규격 데이터 (HBeamData)
- [x] 철근 데이터 (reBarArea, reBarUnitWeight)
- [x] 단면 클래스 (SquareSection, CombinedSection)
- [x] 콘크리트 탄성계수 (ConcreteElasticModulus)
- [x] 유효폭 계산 (EffectiveWidth)
- [x] 처짐 계산 (Deflection)
- [x] 진동 검토 (Vibration)
- [ ] 휨강도 계산 (NominalMomentStrength)
- [ ] 전단강도 계산 (NominalShearStrength)
- [ ] 합성단면 강도 (CompositeSectionMomentStrength)
- [ ] 비용 계산 (CostCalculation)

---

## 📝 이전 히스토리

### 2026-01-06: 프로젝트 초기 설정

#### 1단계: 기존 코드 분석
- `legacy/BestoDesign.py` 분석
- 입력값 정리 → `INPUT_PARAMETERS.md`
- 출력값 정리 → `OUTPUT_PARAMETERS.md`

#### 2단계: UI 개발 (기존 프로젝트)
- H형강 드롭다운 메뉴 추가 (match_list.tsv 기반)
- 입력 폼 UI 완성

#### 3단계: MIDAS 템플릿으로 이전
- `@midasit-dev/cra-template-moaui` 템플릿으로 새 프로젝트 생성 (Midas Plugin V4)
- Pyscript 환경 자동 구성
- 기존 UI 코드 이전 (App.tsx, App.css)

#### 4단계: Python 계산 로직 이전
- `library.py` → `public/py_library.py`
- 핵심 클래스/함수 이전 완료
- py_main.py에서 import 설정

---

## 🔗 Pyscript 사용 예시

### React에서 Python 함수 호출

```typescript
// H형강 데이터 조회
const getBeamData = async (sectionName: string) => {
  const result = await runPython(`
    from py_library import get_h_beam_data
    import json
    data = get_h_beam_data("${sectionName}")
    json.dumps(data)
  `);
  return JSON.parse(result);
};

// 단면 계산
const calculateSection = async () => {
  const result = await runPython(`
    from py_library import SquareSection, CombinedSection
    import json
    
    wing = SquareSection(height=6, width=50, x=25, y=147)
    web = SquareSection(height=138, width=6, x=3, y=75)
    section = CombinedSection(wing, web)
    
    json.dumps({
      'area': section.area,
      'inertiaX': section.inertiaX
    })
  `);
  return JSON.parse(result);
};
```

---

## 📚 참고 자료

### 기존 프로젝트 위치
```
C:\Cursor Projects\Midas Plugin V3\legacy\
├── BestoDesign.py      # 메인 계산 로직 (Excel 연동)
├── library.py          # 계산 함수 라이브러리
├── match_list.tsv      # H형강-U단면 매칭 데이터
├── INPUT_PARAMETERS.md # 입력값 정리 문서
└── OUTPUT_PARAMETERS.md # 출력값 정리 문서
```

### MIDAS 플러그인 개발 가이드
- [A Guide to Creating Plug-in for Developers](https://support.midasuser.com/hc/ko/articles/44321750649369)

### moaui 컴포넌트 문서
- [moaui Storybook](https://midasit-dev.github.io/moaui)

---

## 🔜 다음 작업

1. **Python 계산 로직 완성**
   - 휨강도, 전단강도 계산 함수 이전
   - 합성단면 강도 계산 함수 이전
   - 비용 계산 함수 이전

2. **React ↔ Python 연동**
   - Search 버튼 클릭 시 Python 계산 호출
   - 계산 결과를 테이블에 표시

3. **MIDAS API 연동**
   - 부재 정보 조회
   - 부재력 데이터 가져오기
   - 단면 변경 적용

---

## 📄 라이선스

MIDAS IT Co., Ltd. Internal Use Only
