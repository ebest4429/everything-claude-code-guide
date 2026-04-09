# RULES.md

## 실행 환경

- OS: Windows 10 Pro
- Node.js: v24 (시스템), Electron v29 내장 Node (앱 실행 시)
- Shell: bash (Git Bash / Claude Code 기준)
- 실행: `npm start` (Electron)

## 빌드 규칙

- `npm rebuild` **금지** — 시스템 Node용으로 빌드되어 Electron에서 동작 안 함
- better-sqlite3 재빌드 필요 시: `node_modules/.bin/electron-rebuild -f -w better-sqlite3`
- `npm install` 실행 시 postinstall 훅으로 electron-rebuild 자동 실행됨
- DB 검증은 `sqlite3 data/value-up.db "..."` (sqlite3 CLI) 사용

---

## 계층 원칙 (영구 불변)

- Renderer는 DB에 직접 접근하지 않는다
- Renderer는 파일 시스템에 직접 접근하지 않는다
- 모든 저장은 Main Process의 Service Layer에서 처리한다
- 모든 다중 테이블 저장은 트랜잭션으로 처리한다
- 계산 로직은 순수 함수로 분리한다 (Renderer utils 또는 Main Service)
- 주소 목록 / 코드 목록 하드코딩 금지 (DB에서 조회)

---

## 저장 정책

- 단일행 테이블 (`properties`, `building_info`, `land_info`, `sale_info`): **upsert**
- 다중행 테이블 (`rental_units`, `owners`, `tenants`, `consultations`, `property_images`): **기존 삭제 후 전체 재삽입**
- 저장 진입점: `propertyService.savePropertyAggregate(payload)` 단일 메서드만 사용
- 오류 발생 시 전체 rollback

---

## Phase 원칙

**현재 모드 (2026-03-28~): 기능 보완 모드 — 순차 Phase 진행 아님**

- 현재 활성 마스터 플랜: `.claude/plans/value-up-기능보완.md`
- Phase 8~10 보류 — 기능 보완 완료 후 재검토
- 기능 보완 플랜 범위를 초과하는 구현 금지
- 대형 항목(목록탭·설정탭) 착수 전 별도 플랜 파일 생성 필수
- 완료 조건 기준: `.claude/plans/value-up-기능보완.md` (및 하위 플랜 파일)

---

## 코딩 규칙

- Renderer 파일 하나가 500줄 초과 시 분리 검토
- IPC 채널 네임스페이스 형식: `domain:action` (예: `property:save`, `codes:getAll`)
- Repository: SQL 쿼리만 담당
- Service: 비즈니스 흐름 / 트랜잭션만 담당
- `console.log` 프로덕션 코드 삽입 금지
- 임시 코드 TODO로 방치 금지 → 즉시 정식 구조에 흡수

---

## 하드코딩 금지 원칙

- **DB 경로, 파일 경로, 코드 목록, 주소 목록 등 모든 데이터성 값의 하드코딩 금지**
- 코드/목록 데이터는 반드시 `code_items` 또는 해당 DB 테이블에서 조회
- 더미 데이터도 하드코딩 최대한 배제 — seed 방식으로 DB에 주입
- **하드코딩이 불가피한 경우**: 사전 협의 필수 + `.Source-Files/seed-code-items-검토.md`에 사유 및 내역 명시
- 향후 추가/수정이 예상되는 모든 목록은 DB화하여 UI에서 관리 가능하도록 설계

---

## 플랜 규칙

- 코드 수정 전 `WORKSPACE.md` + `plans/` 확인 필수
- 완료된 체크박스 즉시 `[x]`로 업데이트
- 플랜에 없는 작업 시작 전 사용자 확인 필수

## 전면 변경 시 필수 점검 원칙

다음 상황 중 하나라도 해당하면 **플랜 및 지침 파일 전체 점검·업데이트 후 진행**한다:

- 플랜에 없던 작업이 추가된 경우 (스키마 변경, 테이블 추가, 컬럼 추가 등)
- 기존 구현을 전면 재작성하는 경우
- 설계 결정이 바뀌어 이전 플랜 내용이 더 이상 유효하지 않은 경우
- Phase 완료 조건이 변경되는 경우

**점검 대상:**

| 파일 | 확인 항목 |
|------|----------|
| `WORKSPACE.md` | 현재 상태, 다음 작업 최신화 |
| `CONTEXT.md` | 테이블 목록, Phase 현황 최신화 |
| `plans/value-up-기능보완.md` | 완료 조건, 결정사항 최신화 |
| 현재 활성 플랜 파일 | 체크박스, 추가 작업 반영 (목록탭·설정탭 별도 플랜 포함) |
| `RULES.md` | 새 원칙이 생긴 경우 추가 |

> 세션 말미 또는 커밋 전 위 파일들이 현재 구현과 일치하는지 반드시 확인한다.

---

## 참조 문서 (읽기 전용)

`.Source-Files/` 내 기획 문서는 수정하지 않는다.

| 파일 | 내용 |
|------|------|
| `00-project-overview.md` | 프로젝트 개요 및 목표 |
| `02-architecture.md` | 시스템 아키텍처 |
| `03-database-schema.md` | DB 스키마 전체 |
| `04-ipc-api-spec.md` | IPC API 명세 |
| `05-ui-spec.md` | UI 명세 |
| `06-print-spec.md` | 인쇄 명세 |
| `07-phase-plan.md` | Phase별 완료 조건 |
| `08-migration-plan.md` | Excel 마이그레이션 계획 |
