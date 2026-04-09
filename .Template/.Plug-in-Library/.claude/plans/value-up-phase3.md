# value-up Phase 3 — 기본 UI

**참조 문서 (구현 전 반드시 읽기)**
- IPC 명세: `.Source-Files/04-ipc-api-spec.md`
- UI 명세: `.Source-Files/05-ui-spec.md`
- Phase 완료 조건 원본: `.Source-Files/07-phase-plan.md` Phase 3

---

## 목표

기본정보 / 건축물정보 / 토지이용정보 / 매매정보 화면에서 저장·조회 가능한 상태

> 임대현황 → Phase 4 / 이미지 → Phase 5 / 보안정보 → Phase 5

---

## 1. index.html 전면 재작성

- [x] `renderer/index.html`
  - 상단 컨트롤 바: 새 매물 / 매물 선택 / 저장 / 인쇄 / Excel 가져오기 / Excel 내보내기 / 백업
  - 섹션 구성: 기본정보 / 건축물정보 / 토지이용정보 / 매매정보 및 수익률 / 임대현황(틀) / 이미지(틀) / 보안정보(틀)
  - 임대현황·이미지·보안정보는 구조만 배치, 기능은 Phase 4/5에서 구현
  - `<script src="app.js">` 진입점 연결

---

## 2. utils 모듈

- [x] `renderer/utils/format.js`
  - `toComma(num)` — 숫자 → 콤마 형식 문자열
  - `fromComma(str)` — 콤마 제거 → 숫자
  - `toDate(str)` — YYYY-MM-DD 정규화
  - `toPyeong(m2)` — ㎡ → 평 환산 (÷ 3.3058)

- [x] `renderer/utils/validate.js`
  - `required(value, label)` — 필수값 검증
  - `isDate(str)` — YYYY-MM-DD 형식 검증
  - `isPhone(str)` — 연락처 형식 검증
  - `validateBasicInfo(data)` — 기본정보 필드 검증

- [x] `renderer/utils/calculator.js`
  - `buildPnu(legalDongCode, mountainYn, mainNo, subNo)` — PNU 자동 생성
  - `calcSaleInfo(saleData, rentalTotals)` — 매매정보 계산 필드 산출
    - 대출이자(월) = 대출금액 × 이자율 ÷ 12
    - 대출이자(연) = 대출이자(월) × 12
    - 실투자금 = 매매금액 - 보증금합계 - 대출금액
    - 연간순이익 = 연간임대료 - 대출이자(연)
    - 수익률 = 연간순이익 ÷ 실투자금 × 100

- [x] `renderer/utils/mapper.js`
  - `aggregateToForm(data)` — API 응답 → 폼 필드 매핑
  - `formToPayload()` — 폼 필드 → 저장 payload 매핑

---

## 3. components

- [x] `renderer/components/propertySelector.js`
  - 매물 목록 드롭다운 또는 팝업
  - `loadList()` — `appApi.property.list()` 호출
  - 선택 시 `appApi.property.getById(id)` 호출 → 폼 전체 바인딩

---

## 4. form 모듈

- [x] `renderer/form/basicInfoForm.js`
  - 매물번호 자동 제안 (`appApi.property.getNextPropertyNo()`)
  - 주소 종속 드롭다운 (시도 → 시군구 → 읍면동 → 리)
    - 각 단계별 `appApi.address.*` 호출
  - 법정동코드 조회 → PNU 자동 생성 (`calculator.buildPnu`)
  - 전체주소 자동 조합 (읽기전용)
  - `getValues()` / `setValues(data)` / `validate()`

- [x] `renderer/form/buildingForm.js`
  - 건축물종류 / 건축물구조 select → `appApi.codes.getByGroup()`
  - 건축면적(평) / 연면적(평) 자동 계산 (blur 시)
  - `getValues()` / `setValues(data)` / `validate()`

- [x] `renderer/form/landForm.js`
  - 지목 / 용도지역 select → `appApi.codes.getByGroup()`
  - 대지면적(평) 자동 계산
  - 공시지가(원/평) 자동 계산
  - `getValues()` / `setValues(data)` / `validate()`

- [x] `renderer/form/saleForm.js`
  - 계산 필드 전체 읽기전용
  - 입력값 변경 시 `calculator.calcSaleInfo()` 재계산
  - `getValues()` / `setValues(data)`
  - `updateTotals(rentalTotals)` — Phase 4 연동 준비용 메서드

---

## 5. app.js — 진입점

- [x] `renderer/app.js`
  - DOMContentLoaded 시 초기화
    - 코드 목록 로드 (`appApi.codes.getAll()`)
    - 시도 목록 로드 (`appApi.address.getSidoList()`)
    - 매물 목록 로드 (`propertySelector.loadList()`)
  - **새 매물** 버튼 → 폼 초기화 + 매물번호 자동 제안
  - **저장** 버튼 → `mapper.formToPayload()` → `appApi.property.save()` → 결과 처리
  - **매물 선택** → `propertySelector` → 폼 전체 바인딩

---

## 6. 동작 검증

- [x] 새 매물 생성 → 저장 → DB 확인
- [x] 저장 후 재조회 시 동일 값 재현 (propertySelector 표시 수정 후 확인)
- [x] 주소 선택 4단계 종속 드롭다운 동작
- [x] PNU 자동 생성 확인
- [x] 평 자동 계산 확인 (건축면적, 연면적, 대지면적)
- [x] 공시지가 원/평 자동 계산 확인
- [x] 매매정보 계산 필드 자동 계산 확인
- [x] 필수값 누락 시 에러 표시 확인

---

## 완료 조건 (전부 충족 시 Phase 3 완료)

- [x] 새 매물 생성 가능
- [x] 저장 후 재조회 가능
- [x] 주소 선택 → PNU 자동 생성
- [x] 기본 필드 검증 동작

---

## 생성/수정 파일 목록

```
renderer/
├── index.html          (전면 재작성)
├── app.js              (신규)
├── components/
│   └── propertySelector.js  (신규)
├── form/
│   ├── basicInfoForm.js     (신규)
│   ├── buildingForm.js      (신규)
│   ├── landForm.js          (신규)
│   └── saleForm.js          (신규)
└── utils/
    ├── format.js        (신규)
    ├── validate.js      (신규)
    ├── calculator.js    (신규)
    └── mapper.js        (신규)
```

---

## 설계 결정사항

| 항목 | 결정 | 이유 |
|------|------|------|
| 임대현황 섹션 처리 | 틀만 배치, Phase 4 구현 | 합계 연동 로직이 ROI 계산과 묶임 |
| 보안정보/이미지 | 틀만 배치, Phase 5 구현 | 인쇄 제외 처리와 함께 구현 필요 |
| saleForm.updateTotals | Phase 4 연동 준비용 빈 메서드로 선언 | 나중에 rentalForm에서 호출 |
| 폼 모듈 인터페이스 | getValues/setValues/validate 통일 | app.js에서 일관된 방식으로 호출 |
| 도로명주소 | 수동 입력 유지, 자동완성은 별도 플랜으로 분리 | 203,809건 seed + IPC 추가 필요, Phase 3 범위 초과 |
| 공시지가 기준년 | UI 제거 (DB 컬럼은 유지) | 매년 1월 1일 자동 변경으로 입력 불필요 |
| 날짜 입력 | type=text + blur 시 YYYY-MM-DD 정규화 | Chromium date input 분절 입력 UX 문제 |

---

## 버그수정 이력 (구현 후 검증 단계)

| 파일 | 수정 내용 |
|------|----------|
| `main/ipc/codesIpc.js` | 코드 목록을 `{key,value}` 객체 → 문자열 배열로 변경 |
| `renderer/utils/mapper.js` | 전면 재작성 — camelCase↔snake_case 양방향 변환, structure_type 추가 |
| `renderer/utils/calculator.js` | PNU 산여부: 일반=1, 산=2 (기존 0/1 오류 수정) |
| `renderer/form/basicInfoForm.js` | `_legalDongCode` 변수 추가 — getValues/setValues/reset 반영 |
| `renderer/form/landForm.js` | officialPriceYear 필드 전체 제거 |
| `renderer/app.js` | clearForms async 처리, alert→toast, 포커스 전체선택, 날짜 blur포맷 |
| `renderer/index.html` | date→text 변환, officialPriceYear 제거 |

---

## 후속 작업 (별도 플랜)

- **도로명주소 자동완성**: `.claude/plans/value-up-road-address.md`
  - 읍면동 선택 → 도로명 드롭다운 자동 로드 (도로명코드.csv 기반)
  - road_name_codes 테이블 신규, seed 203,809건
  - Phase 3 완료 후 또는 Phase 4 전 처리
