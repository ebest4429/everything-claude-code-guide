# value-up Phase 4 — 임대현황 및 수익률 계산

**참조 문서**
- IPC 명세: `.Source-Files/04-ipc-api-spec.md`
- UI 명세: `.Source-Files/05-ui-spec.md`
- DB 스키마: `.Source-Files/03-database-schema.md`

---

## 목표

임대현황 다중행 관리 및 매매정보 수익률 계산 완성

---

## 1. index.html 수정

- [x] 임대현황 섹션 stub → 실제 테이블 UI 교체
  - 컬럼: No / 호실 / 면적(㎡) / 용도 / 보증금(만) / 월세(만) / 관리비(만) / 공실여부 / 비고 / 삭제
  - tfoot 합계 행 (임대중 기준)
  - 임대개요 영역 (동적 생성 — rentalForm.init 담당)
- [x] 임대현황 테이블 CSS 추가
- [x] `depositTotal` 입력 → readonly 변경 (임대현황에서 자동 연동)
- [x] `<script src="form/rentalForm.js">` 로드 추가 (saleForm.js 뒤)

---

## 2. rentalForm.js (신규)

- [x] `renderer/form/rentalForm.js`
  - `init(codesMap)` — rental_use / vacancy_status 코드 로드, 임대개요 DOM 생성
  - `addRow(data)` — 행 추가 (최대 30행), select 옵션 생성, 숫자 포맷 바인딩
  - `recalc()` — 합계 계산 (임대중 행만), 임대개요 카운트, saleForm.updateTotals() 호출
  - `getValues()` — 전체 행 → snake_case 배열 (저장용)
  - `setValues(units)` — DB 배열 → 행 렌더링
  - `reset()` — 테이블 비우기

---

## 3. app.js 수정

- [x] `rentalForm.init(codesMap)` 추가 (폼 초기화 순서 내)
- [x] `clearForms()` 에 `rentalForm.reset()` 추가
- [x] `onPropertySelected()` 에 `rentalForm.setValues(mapped.rentalUnits)` 추가
  - saleForm.setValues() 뒤에 호출 (updateTotals 덮어쓰기 순서 보장)
- [x] `onSave()` payload에 `rentalUnits: rentalForm.getValues()` 추가

---

## 4. saleForm.js 수정

- [x] `bindComma()` 목록에서 `'depositTotal'` 제거
  (readonly 필드라 포맷 이벤트 불필요)

---

## 완료 조건

- [x] 최대 30행 관리 가능
- [x] 합계 계산 정확 (임대중 행만)
- [x] 임대현황 변경 시 매매정보(보증금합계/월세합계/관리비합계/수익률) 실시간 반영
- [x] 저장 후 재조회 시 동일 값 재현

---

## 생성/수정 파일 목록

```
renderer/
├── index.html           (수정 — rental 섹션 + CSS + readonly + script)
├── app.js               (수정 — rentalForm 연동)
├── form/
│   ├── rentalForm.js    (신규)
│   └── saleForm.js      (수정 — depositTotal bindComma 제거)
```

---

## 설계 결정사항

| 항목 | 결정 | 이유 |
|------|------|------|
| depositTotal | readonly (자동계산) | UI 명세 12항: 보증금합계는 읽기전용 |
| 합계 계산 기준 | vacancy_status = '임대중' | UI 명세 8항: 합계는 임대중 행만 반영 |
| 임대개요 DOM | init() 시 동적 생성 | rental_use 코드 목록 기반, 하드코딩 금지 |
| rentalForm.setValues 호출 순서 | saleForm.setValues 이후 | updateTotals로 depositTotal 덮어쓰기 보장 |
| mapper.js | 수정 불필요 | rentalUnits는 snake_case 그대로 pass-through |
