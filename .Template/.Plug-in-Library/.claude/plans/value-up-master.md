# value-up 전체 프로젝트 플랜

## 프로젝트 개요

**부동산 매물관리 및 수익률 분석 시스템**
Electron + SQLite + HTML/CSS/JS | 로컬 데스크톱 전용 | 단일 사용자

설계 원본: `.Source-Files/00-project-overview.md`
아키텍처: `.Source-Files/02-architecture.md`
DB 스키마: `.Source-Files/03-database-schema.md`

---

## 전체 Phase 체크리스트

- [x] **Phase 1** — 프로젝트 골격 (Electron + SQLite 초기화)
- [x] **Phase 2** — 데이터 레이어 (Repository + Service + IPC)
- [x] **Phase 3** — 기본 UI (기본정보 / 건축물 / 토지 / 매매)
- [x] **Phase 4** — 임대현황 및 수익률 계산
- [x] **Phase 5** — 보안정보 및 이미지
- [x] **Phase 6** — 인쇄 (기능 완료 동결 — 보강 플랜 별도 예정)
- [x] **Phase 7** — Excel import/export (기본 구현 완료 동결 — 보강 플랜 별도 예정)
- [ ] **Phase 8** — 백업/복원 및 마감 (패키징) ⏸ 보류
- [ ] **Phase 9** — (미정) ⏸ 보류
- [ ] **Phase 10** — (미정) ⏸ 보류

---

## Phase별 완료 조건 요약

### Phase 1 ✅ 완료
- 앱 정상 실행
- `data/value-up.db` 생성
- 13개 테이블 생성 (기존 11 + building_use_codes + users 추가)
- code_items seed 삽입 (1,580건: CSV 파싱 기반)
- building_use_codes seed 삽입 (968건)
- 법정동코드 seed 삽입 (20,560건)
- main / preload / renderer 계층 분리

### Phase 2
- UI 없이 매물 aggregate 저장/조회 가능
- 단일행 upsert 동작
- 다중행 replace 동작
- 트랜잭션 rollback 동작
- IPC 채널 전체 등록

### Phase 3
- 새 매물 생성 가능
- 저장 후 재조회 가능
- 주소 선택 → PNU 자동 생성
- 기본 필드 검증

### Phase 4
- 최대 30행 임대현황 관리
- 합계 계산 정확
- 임대현황 변경 시 ROI 실시간 반영
- 저장/재조회 시 동일 값 재현

### Phase 5
- 보안정보(소유주/임차인/상담) 저장/조회
- 이미지 파일 저장/재조회
- 인쇄 제외 UI 구분

### Phase 6
- 3페이지 인쇄 레이아웃
- 보안정보 완전 제외
- A4 기준 출력

### Phase 7
- 기존 Excel 데이터 import
- DB → Excel export
- 법정동코드 API 연동 (운영계정 승인 후)

### Phase 8
- DB + 이미지 백업/복원
- 설치형 빌드 (electron-builder)
- 문서 최신화

---

## 다음 목표 — Phase 1~5 기능 보완 (Phase 8~10 보류 후 우선 진행)

> Phase 6(인쇄), Phase 7(Excel) 기본 구현 동결 후 방향 전환
> Phase 8~10 보류 — 기초 기능 완성도 확보가 우선

### 핵심 방향

| 항목 | 내용 |
|------|------|
| 목록탭 | 매물목록 관리 전용 탭 — 조회/검색/선택/삭제 등 |
| 설정탭 | 설정 페이지 — 코드목록 관리, 작성자 관리 등 |
| 구조 보완 | Phase 1~5 구현 중 누적된 결함/구조적 문제 해결 |
| 추가기능 | 기본 업무에 필요한 기능 보완 (우선순위 협의 후 결정) |

> 상세 구현 계획은 별도 플랜 파일로 작성

---

## 프로젝트 범위 외 계획

> 현재 value-up Electron 앱의 구현 범위에 포함되지 않는 별도 개발 계획
> 참조 폴더: `.Source-Files/`
> 여건에 따라 개발 / 여건이 안 되면 상황에 맞게 사용

| 계획 | 파일 | 개발 시점 |
|------|------|---------|
| 엑셀 원본 정규화 도구 | `.Source-Files/엑셀정규화-계획.md` | 여건 확보 시 |
| 엑셀 통합관리 시트 | `.Source-Files/엑셀통합관리-계획.md` | 앱 범용성 확보 + 내보내기 전면 재구상 후 |

### 배경

- **엑셀 정규화**: 불러오기 기능은 사용자 Excel 구조가 표준과 일치해야 동작. 불특정 다수 사용자의 다양한 구조를 정규화하는 별도 앱/에이전트/스킬이 필요
- **통합관리 시트**: 내보내기는 시트 분할 구조. Excel 내에서 분할 시트를 통합 관리하는 시트가 없으면 실무 활용 어려움. 앱 범용성 확보(아파트/공장/분양권/재개발 등 섹션 추가) 및 내보내기 전면 재구상 이후 설계

---

## 결정사항 기록

| 날짜 | 결정 | 이유 |
|------|------|------|
| 2026-03-26 | Electron 채택 | 로컬 파일/SQLite 직접 접근, 인쇄 제어, 개인정보 보호 |
| 2026-03-26 | 법정동코드 seed 방식 | `.Source-Files/법정동코드.md` 파일로 초기 로드, API는 Phase 7에서 업데이트 기능으로 추가 |
| 2026-03-26 | 저장 진입점 단일화 | `propertyService.savePropertyAggregate()` 1개 메서드만 사용 |
| 2026-03-26 | 스키마 13개 테이블 확정 | building_use_codes(검색용), users(작성자) 추가, code_items에 code_key 컬럼 추가 |
| 2026-03-26 | seed 소스파일 파싱 방식 확정 | 하드코딩 금지 원칙, CSV 파싱 기반으로 전면 교체 |
| 2026-03-26 | 도로명주소 자동완성 별도 플랜 분리 | 도로명코드 203,809건 seed + IPC 추가 필요, Phase 3 범위 초과. 플랜: `plans/value-up-road-address.md` |
| 2026-03-26 | 공시지가 기준년 UI 제거 | 매년 1월 1일 자동 변경으로 입력 불필요. DB 컬럼은 유지 |
| 2026-03-26 | property_no는 PK 아님 확정 | properties.id(자동증가)가 실제 PK, property_no는 UNIQUE 비즈니스 키. 추후 변경 가능 |
