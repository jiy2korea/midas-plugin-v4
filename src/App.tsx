/**
 * BESTO Design Plugin
 * 기존 UI 코드를 MIDAS Pyscript 템플릿에 통합
 */

import React, { useState } from 'react';
import './App.css';

// H형강 리스트 (match_list.tsv 기반)
const H_SECTION_LIST = [
  'H-248X124X5X8', 'H-250X125X6X9', 'H-244X175X7X11',
  'H-298X149X5.5X8', 'H-300X150X6.5X9', 'H-294X200X8X12', 'H-298X201X9X14',
  'H-346X174X6X9', 'H-350X175X7X11', 'H-354X176X8X13',
  'H-336X249X8X12', 'H-340X250X9X14',
  'H-396X199X7X11', 'H-400X200X8X13', 'H-404X201X9X15',
  'H-386X299X9X14', 'H-390X300X10X16',
  'H-446X199X8X12', 'H-450X200X9X14',
  'H-434X299X10X15', 'H-440X300X11X18',
  'H-496X199X9X14', 'H-500X200X10X16', 'H-506X201X11X19',
  'H-482X300X11X15', 'H-488X300X11X18',
  'H-596X199X10X15', 'H-600X200X11X17', 'H-606X201X12X20', 'H-612X202X13X23',
  'H-582X300X12X17', 'H-588X300X12X20', 'H-594X302X14X23',
  'H-692X300X13X20', 'H-700X300X13X24', 'H-708X302X15X28',
  'H-792X300X14X22', 'H-800X300X14X26', 'H-808X302X16X30',
  'H-890X299X15X23', 'H-900X300X16X28', 'H-912X302X18X34', 'H-918X303X19X37',
  'H-244X252X11X11', 'H-248X249X8X13', 'H-250X250X9X14', 'H-250X255X14X14',
  'H-294X302X12X12', 'H-298X299X9X14', 'H-304X301X11X17', 'H-310X305X15X20', 'H-310X310X20X20',
  'H-338X351X13X13', 'H-344X348X10X16', 'H-344X354X16X16', 'H-350X350X12X19', 'H-350X357X19X19',
  'H-388X402X15X15', 'H-394X398X11X18', 'H-394X405X18X18', 'H-400X400X13X21', 'H-400X408X21X21',
  'H-406X403X16X24', 'H-414X405X18X28', 'H-428X407X20X35',
  'H-458X417X30X50', 'H-498X432X45X70',
];

// 섹션 데이터 타입 정의
interface SectionData {
  section: string;
  chk: string;
  selected: boolean;
  beforeComposite: {
    mEnd: number;
    mMid: number;
    v: number;
  };
  afterComposite: {
    mEnd: number;
    mMid: number;
    v: number;
  };
}

const App = () => {
  // 선택된 부재 이름
  const [selectedMember, setSelectedMember] = useState(H_SECTION_LIST[0]);

  // Additional Informations 상태
  // 철근 - 개수와 지름
  const [rebarTopCount, setRebarTopCount] = useState('');
  const [rebarTopDia, setRebarTopDia] = useState('');
  const [rebarBotCount, setRebarBotCount] = useState('');
  const [rebarBotDia, setRebarBotDia] = useState('');
  const [fYr, setFYr] = useState('');
  
  // 전단연결재 - 간격
  const [studSpacing, setStudSpacing] = useState('');
  const [angleSpacing, setAngleSpacing] = useState('');

  // 오른쪽 영역
  const [fYU, setFYU] = useState('');
  const [fYH, setFYH] = useState('');
  const [concrete, setConcrete] = useState('');
  const [slabDs, setSlabDs] = useState('');
  const [slabBeff, setSlabBeff] = useState('');
  const [support, setSupport] = useState('');

  // Section List 상태
  const [sectionList, setSectionList] = useState<SectionData[]>([]);
  const [selectedSectionIndex, setSelectedSectionIndex] = useState<number | null>(null);

  // Search Satisfied Section 버튼 핸들러
  const handleSearch = () => {
    // 예시 데이터 - 실제로는 Pyscript를 통해 계산된 데이터
    const mockData: SectionData[] = [
      {
        section: 'H-600x300x11x12\nU-400x350x7',
        chk: 'OK',
        selected: false,
        beforeComposite: { mEnd: 0.7, mMid: 0.8, v: 0.6 },
        afterComposite: { mEnd: 0.7, mMid: 0.8, v: 0.6 },
      },
    ];
    setSectionList(mockData);
  };

  // 섹션 선택 핸들러
  const handleSectionSelect = (index: number) => {
    setSelectedSectionIndex(index);
    setSectionList(prev =>
      prev.map((item, i) => ({
        ...item,
        selected: i === index,
      }))
    );
  };

  // Change 버튼 핸들러
  const handleChange = () => {
    if (selectedSectionIndex !== null) {
      alert(`선택된 섹션: ${sectionList[selectedSectionIndex].section.replace('\n', ' / ')}\n마이다스 연동 시 해당 부재가 변경됩니다.`);
    } else {
      alert('섹션을 먼저 선택해주세요.');
    }
  };

  // Detail 버튼 핸들러
  const handleDetail = () => {
    if (selectedSectionIndex !== null) {
      alert('상세 정보 화면이 열립니다.');
    } else {
      alert('섹션을 먼저 선택해주세요.');
    }
  };

  // Close 버튼 핸들러
  const handleClose = () => {
    alert('플러그인을 종료합니다.');
  };

  return (
    <div className="plugin-container">
      {/* Selected Member */}
      <fieldset className="section-fieldset">
        <legend>Selected Member</legend>
        <select 
          className="member-select" 
          value={selectedMember} 
          onChange={(e) => setSelectedMember(e.target.value)}
        >
          {H_SECTION_LIST.map((section) => (
            <option key={section} value={section}>{section}</option>
          ))}
        </select>
      </fieldset>

      {/* Additional Informations */}
      <fieldset className="section-fieldset">
        <legend>Additional Informations</legend>
        <div className="additional-info-container">
          {/* 왼쪽 영역 - 테이블 레이아웃 */}
          <div className="info-left">
            <table className="info-table-left">
              <tbody>
                <tr>
                  <td className="label-cell-left-title">- Re-bar</td>
                  <td className="label-cell-left-sub">top</td>
                  <td className="input-cell-left">
                    <input 
                      type="text" 
                      value={rebarTopCount} 
                      onChange={(e) => setRebarTopCount(e.target.value)} 
                      placeholder="개수"
                      className="input-small"
                    />
                    <span className="separator">-</span>
                    <select value={rebarTopDia} onChange={(e) => setRebarTopDia(e.target.value)}>
                      <option value="">지름</option>
                      <option value="D10">D10</option>
                      <option value="D13">D13</option>
                      <option value="D16">D16</option>
                      <option value="D19">D19</option>
                      <option value="D22">D22</option>
                      <option value="D25">D25</option>
                      <option value="D29">D29</option>
                      <option value="D32">D32</option>
                    </select>
                  </td>
                  <td className="unit-cell-left"></td>
                </tr>
                <tr>
                  <td className="label-cell-left-title"></td>
                  <td className="label-cell-left-sub">bot.</td>
                  <td className="input-cell-left">
                    <input 
                      type="text" 
                      value={rebarBotCount} 
                      onChange={(e) => setRebarBotCount(e.target.value)} 
                      placeholder="개수"
                      className="input-small"
                    />
                    <span className="separator">-</span>
                    <select value={rebarBotDia} onChange={(e) => setRebarBotDia(e.target.value)}>
                      <option value="">지름</option>
                      <option value="D10">D10</option>
                      <option value="D13">D13</option>
                      <option value="D16">D16</option>
                      <option value="D19">D19</option>
                      <option value="D22">D22</option>
                      <option value="D25">D25</option>
                      <option value="D29">D29</option>
                      <option value="D32">D32</option>
                    </select>
                  </td>
                  <td className="unit-cell-left"></td>
                </tr>
                <tr>
                  <td className="label-cell-left-title"></td>
                  <td className="label-cell-left-sub">f_yr</td>
                  <td className="input-cell-left">
                    <select value={fYr} onChange={(e) => setFYr(e.target.value)}>
                      <option value=""></option>
                      <option value="300">300</option>
                      <option value="400">400</option>
                      <option value="500">500</option>
                    </select>
                  </td>
                  <td className="unit-cell-left">MPa</td>
                </tr>
                <tr>
                  <td className="label-cell-left-title">- Shear Connector</td>
                  <td className="label-cell-left-sub">stud</td>
                  <td className="input-cell-left">
                    <input 
                      type="text" 
                      value={studSpacing} 
                      onChange={(e) => setStudSpacing(e.target.value)} 
                      placeholder="간격"
                    />
                  </td>
                  <td className="unit-cell-left">mm</td>
                </tr>
                <tr>
                  <td className="label-cell-left-title"></td>
                  <td className="label-cell-left-sub">angle</td>
                  <td className="input-cell-left">
                    <input 
                      type="text" 
                      value={angleSpacing} 
                      onChange={(e) => setAngleSpacing(e.target.value)} 
                      placeholder="간격"
                    />
                  </td>
                  <td className="unit-cell-left">mm</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* 오른쪽 영역 - 그리드 레이아웃 */}
          <div className="info-right">
            <table className="info-table">
              <tbody>
                <tr>
                  <td className="label-cell-wide" colSpan={2}>- F_yU</td>
                  <td className="input-cell">
                    <select value={fYU} onChange={(e) => setFYU(e.target.value)}>
                      <option value=""></option>
                      <option value="235">235</option>
                      <option value="275">275</option>
                      <option value="355">355</option>
                    </select>
                  </td>
                  <td className="label-cell-inline">F_yH</td>
                  <td className="input-cell">
                    <select value={fYH} onChange={(e) => setFYH(e.target.value)}>
                      <option value=""></option>
                      <option value="235">235</option>
                      <option value="275">275</option>
                      <option value="355">355</option>
                    </select>
                  </td>
                </tr>
                <tr>
                  <td className="label-cell-wide" colSpan={2}>- Concrete</td>
                  <td className="input-cell">
                    <select value={concrete} onChange={(e) => setConcrete(e.target.value)}>
                      <option value=""></option>
                      <option value="C24">C24</option>
                      <option value="C30">C30</option>
                      <option value="C40">C40</option>
                    </select>
                  </td>
                  <td className="label-cell-inline"></td>
                  <td className="unit-cell"></td>
                </tr>
                <tr>
                  <td className="label-cell-right">- Slab</td>
                  <td className="label-cell-sub-left">d_s</td>
                  <td className="input-cell">
                    <input type="text" value={slabDs} onChange={(e) => setSlabDs(e.target.value)} />
                  </td>
                  <td className="unit-cell-inline">mm</td>
                  <td className="unit-cell"></td>
                </tr>
                <tr>
                  <td className="label-cell-right"></td>
                  <td className="label-cell-sub-left">b_eff</td>
                  <td className="input-cell">
                    <input type="text" value={slabBeff} onChange={(e) => setSlabBeff(e.target.value)} />
                  </td>
                  <td className="unit-cell-inline">mm</td>
                  <td className="unit-cell"></td>
                </tr>
                <tr>
                  <td className="label-cell-wide" colSpan={2}>- Support</td>
                  <td className="input-cell">
                    <select value={support} onChange={(e) => setSupport(e.target.value)}>
                      <option value=""></option>
                      <option value="Simple">Simple</option>
                      <option value="Continuous">Continuous</option>
                    </select>
                  </td>
                  <td className="label-cell-inline"></td>
                  <td className="unit-cell"></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </fieldset>

      {/* Search Button - 필드 바깥쪽 */}
      <div className="search-button-container">
        <button className="search-button" onClick={handleSearch}>
          Search Satisfied Section
        </button>
      </div>

      {/* Section List */}
      <fieldset className="section-fieldset">
        <legend>Section List</legend>
        <div className="table-container">
          <table className="section-table">
            <thead>
              <tr>
                <th rowSpan={2}>Section</th>
                <th rowSpan={2}>CHK</th>
                <th rowSpan={2}>SEL</th>
                <th colSpan={3}>Before Composite</th>
                <th colSpan={3}>After Composite</th>
              </tr>
              <tr>
                <th colSpan={2}>M</th>
                <th rowSpan={2}>V</th>
                <th colSpan={2}>M</th>
                <th rowSpan={2}>Δ</th>
              </tr>
              <tr>
                <th></th>
                <th></th>
                <th></th>
                <th>end</th>
                <th>mid</th>
                <th>end</th>
                <th>mid</th>
              </tr>
            </thead>
            <tbody>
              {sectionList.length === 0 ? (
                <tr>
                  <td colSpan={9} className="empty-row">
                    Search 버튼을 눌러 섹션을 검색하세요.
                  </td>
                </tr>
              ) : (
                sectionList.map((section, index) => (
                  <tr key={index} className={section.selected ? 'selected-row' : ''}>
                    <td className="section-cell">
                      {section.section.split('\n').map((line, i) => (
                        <div key={i}>{line}</div>
                      ))}
                    </td>
                    <td>{section.chk}</td>
                    <td>
                      <input
                        type="checkbox"
                        checked={section.selected}
                        onChange={() => handleSectionSelect(index)}
                      />
                    </td>
                    <td>{section.beforeComposite.mEnd}</td>
                    <td>{section.beforeComposite.mMid}</td>
                    <td>{section.beforeComposite.v}</td>
                    <td>{section.afterComposite.mEnd}</td>
                    <td>{section.afterComposite.mMid}</td>
                    <td>{section.afterComposite.v}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </fieldset>

      {/* Bottom Buttons */}
      <div className="bottom-buttons">
        <button className="action-button" onClick={handleDetail}>
          Detail...
        </button>
        <button className="action-button" onClick={handleChange}>
          Change
        </button>
        <button className="action-button" onClick={handleClose}>
          Close
        </button>
      </div>
    </div>
  );
};

export default App;
