# WORKSPACE.md

> 세션 시작 시 가장 먼저 읽는다.
> 현재 위치 확인 전용. 상세 내용은 plans/ 참조.
> 업데이트 방식으로 기록. 체크박스 없음. 체크박스는 페이지 플랜에만.

---

## 현재 위치

| 항목 | 값 |
|------|-----|
| PROJECT | value-up |
| 현재 Phase | Phase 5 — 보안정보 및 이미지 |
| 상태 | 구현 시작 전 |
| 현재 플랜 | `.claude/plans/value-up-phase5.md` |
| 전체 플랜 | `.claude/plans/value-up-master.md` |

---

## Phase 5 구현 순서

| 순서 | 항목 | 파일 |
|------|------|------|
| 1 | imageIpc.js 신규 | `main/ipc/imageIpc.js` |
| 2 | imageIpc 등록 | `main/index.js` |
| 3 | image.getDataPath 추가 | `preload/index.js` |
| 4 | 소유주 테이블 | `renderer/form/ownersForm.js` |
| 5 | 임차인 테이블 | `renderer/form/tenantsForm.js` |
| 6 | 상담내역 테이블 | `renderer/form/consultationsForm.js` |
| 7 | 이미지 업로드/미리보기 | `renderer/form/imagesForm.js` |
| 8 | 이미지/보안정보 UI | `renderer/index.html` |
| 9 | 4개 form 연동 | `renderer/app.js` |

mapper.js — owners/tenants/consultations/images 매핑 이미 완료 (Phase 2)

---

## 진행 현황

### 2026-03-27 구현 완료 (동작 검증 전)

| 파일 | 내용 |
|------|------|
| `main/ipc/imageIpc.js` | 신규 — upload/delete/getDataPath |
| `main/index.js` | imageIpc 등록 |
| `preload/index.js` | image.getDataPath 추가, delete 인자 수정 |
| `renderer/utils/format.js` | formatPhone() 추가 |
| `renderer/form/ownersForm.js` | 신규 |
| `renderer/form/tenantsForm.js` | 신규 |
| `renderer/form/consultationsForm.js` | 신규 |
| `renderer/form/imagesForm.js` | 신규 |
| `renderer/index.html` | 이미지/보안정보 섹션 실제 UI + CSS |
| `renderer/app.js` | 4개 form 연동 완료 |

### 2026-03-27 보완 구현 (동작 검증 전)

| 파일 | 내용 |
|------|------|
| `format.js` | formatPhone 02지역번호/일반전화/휴대폰 분기 수정 |
| `migrate.js` | owners.note / tenants.note 컬럼 추가 마이그레이션 |
| `ownersRepository.js` | note 컬럼 INSERT 반영 |
| `tenantsRepository.js` | note 컬럼 INSERT 반영 |
| `ownersForm.js` | 비고 필드 추가 |
| `tenantsForm.js` | 비고 필드 추가 |
| `consultationsForm.js` | 상담내용 별도행(2행세트) + 상담일 오늘날짜 기본값 + textarea 자동높이 |
| `index.html` | 테이블 헤더 비고 추가, 상담내역 헤더 수정, 이미지추가버튼 no-print |

### 2026-03-27 동작 검증 완료

소유주/임차인/상담내역 저장-재조회 정상, 이미지 업로드/미리보기/삭제 정상 확인.
imagesForm.js btn-del-image에 no-print 클래스 누락 발견 → 수정 완료.

---

## 보류 중인 보완 항목

| 항목 | 내용 | 처리 시점 |
|------|------|---------|
| B3 아코디언 + 인쇄 연동 | 닫힌 섹션 인쇄 제외 | Phase 6 통합 |
| B8 다중 지번 지원 | 플랜만 작성, 구현 미정 | 필요 시 협의 |

---

## 완료된 Phase 요약

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 1 | Electron + SQLite 초기화 | 완료 |
| Phase 2 | Repository + Service + IPC | 완료 |
| Phase 3 | 기본 UI (기본정보/건축물/토지/매매) | 완료 |
| 보완 B1~B7 | rental_use/property_type/도로명/입력규칙 등 | 완료 |
| Phase 4 | 임대현황 + 수익률 계산 | 완료 |
| Phase 5 | 보안정보 및 이미지 | 완료 |

---

## 아카이브

| 파일 | 내용 |
|------|------|
| `.claude/archive/WORKSPACE.phase4.2026-03-27.md` | Phase 4 + 보완 B1~B7 완료 기록 |
