# WORKSPACE.md 아카이브 — Phase 4 + 보완 플랜

> 아카이브 일자: 2026-03-27
> 대상 범위: Phase 4 (임대현황 및 수익률) + 보완 플랜 B1~B7

---

## 현재 위치 (아카이브 시점)

| 항목 | 값 |
|------|-----|
| PROJECT | value-up |
| 완료 Phase | Phase 4 — 임대현황 및 수익률 계산 |
| 다음 Phase | Phase 5 — 보안정보 및 이미지 |

---

## Phase 4 완료 작업

### 보완 플랜 B1 ✅
- `seed.js` rental_use 신버전(상가/1R/1.5R/2R/3R/4R)으로 교체
- `seedMissingCodeGroups()` 추가 — 기존 DB에 신규 코드그룹 자동 보충
- `migrate.js` — PRAGMA table_info 체크 후 컬럼 누락 시 ALTER TABLE

### 보완 플랜 B2 ✅
- `schema.sql` properties 테이블에 property_type 컬럼 추가
- `seed.js` property_type 17개 코드 추가 (PT001~PT017)
- `index.html` 매물번호 옆 매물종류 select 추가
- `basicInfoForm.js` / `mapper.js` / `app.js` / `propertyRepository.js` 반영

### 보완 플랜 B4 ✅ (소스파일 현행화)
- `seed-code-items-검토.md`: 반영현황 전체 ✅, property_type 섹션 추가
- `03-database-schema.md`: properties 테이블 property_type 컬럼 반영
- `05-ui-spec.md`: 매물종류 항목, 필수 규칙, 공시지가기준년 제거 주석
- `07-phase-plan.md`: Phase 1~4 작업항목/완료조건 [x] 처리

### 보완 플랜 B5 ✅ (도로명주소 자동완성)
- `schema.sql`: road_name_codes 테이블 추가 (203,809건)
- `seed.js`: seedRoadNameCodes() 배치 삽입
- `roadNameCodesRepository.js`: findRoadNameList() 신규
- `addressIpc.js`: address:getRoadNameList 채널 추가
- `preload/index.js`: appApi.address.getRoadNameList 노출
- `basicInfoForm.js`: 읍면동 선택 → 도로명 드롭다운 + 도로명주소 자동조합
- `index.html`: 도로명 select + roadMainNo/roadSubNo 분리 필드 추가

### 보완 플랜 B6 ✅ (프로세스 개선)
- `CLAUDE.md` 작업 순서 원칙 섹션 추가
- `.claude/hooks/HOOK_GUIDE.md` 신규 작성
- `.claude/hooks/remind-plan-update.js` 신규
- `settings.local.json` PostToolUse(Edit/Write) 훅 추가

### 보완 플랜 B7 ✅ (입력규칙)
- 필드별 입력규칙 validate.js 보강
- 숫자 필드 문자 차단 적용

### Phase 4 구현 완료 ✅
- `renderer/form/rentalForm.js` 신규 (임대현황 테이블)
- `renderer/index.html` 임대현황 섹션 실제 UI + CSS + depositTotal readonly
- `renderer/app.js` rentalForm 연동 전체
- `renderer/form/saleForm.js` depositTotal bindComma 제거

### Phase 4 동작 검증 ✅
- 행 추가/삭제 + 합계 계산 (임대중만) 확인
- 매매정보 ROI 실시간 연동 확인
- 저장 후 재조회 동일 값 재현 확인

---

## 보완 플랜 최종 상태 (아카이브 시점)

| 항목 | 상태 | 비고 |
|------|------|------|
| B1 rental_use 수정 | ✅ | |
| B2 property_type 추가 | ✅ | |
| B3 아코디언 + 인쇄 | 🔲 보류 | Phase 6 통합 예정 |
| B4 소스파일 현행화 | ✅ | |
| B5 도로명주소 | ✅ | |
| B6 프로세스 개선 | ✅ | |
| B7 입력규칙 | ✅ | |
| B8 다중 지번 플랜 | 🔲 보류 | 필요 시 구현 |
