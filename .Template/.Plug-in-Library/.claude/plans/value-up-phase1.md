# value-up Phase 1 — 프로젝트 골격

**참조 문서 (구현 전 반드시 읽기)**
- 아키텍처: `.Source-Files/02-architecture.md`
- DB 스키마: `.Source-Files/03-database-schema.md`
- Phase 완료 조건 원본: `.Source-Files/07-phase-plan.md` Phase 1

---

## 1. 프로젝트 초기화

- [x] `package.json` 작성
  - dependencies: `electron`, `better-sqlite3`
  - devDependencies: `electron-builder`
  - scripts: `start`, `build`
- [x] `main/index.js` — BrowserWindow 생성, DB 초기화 호출
- [x] `preload/index.js` — contextBridge 기본 구조 (`window.appApi` 노출 준비)
- [x] `renderer/index.html` — 최소 스켈레톤 (앱 실행 확인용)

## 2. DB 연결 모듈

- [x] `main/db/connection.js` — better-sqlite3 연결
  - DB 파일 경로: `data/value-up.db`
  - WAL 모드 활성화 (`PRAGMA journal_mode=WAL`)
  - foreign_keys 활성화 (`PRAGMA foreign_keys=ON`)

## 3. Schema

- [x] `main/db/schema.sql` — 11개 테이블 + 인덱스 전체 작성
  - 단일행: `properties`, `building_info`, `land_info`, `sale_info`
  - 다중행: `rental_units`, `owners`, `tenants`, `consultations`, `property_images`
  - 참조: `address_codes`, `code_items`
  - 인덱스 10개 포함
  - 스키마 전체 내용: `.Source-Files/03-database-schema.md`
- [x] `main/db/migrate.js` — schema.sql 자동 실행 (앱 시작 시)

## 4. Seed 데이터

- [x] `main/db/seed.js` — 최초 1회 실행 구조
- [x] `code_items` 기본값 삽입
  - 건물용도, 건축물구조, 지목, 용도지역, 임대용도, 공실여부, 작성자
- [x] `address_codes` 삽입
  - 소스: `.Source-Files/법정동코드.md` (탭 구분 TSV, 법정동코드 + 법정동명)
  - 파싱: 10자리 코드만 추출, sido/sigungu/eupmyeondong/ri 분리
  - 중복 실행 방지 (`INSERT OR IGNORE`)

## 5. 앱 실행 확인

- [x] `npm start` 실행 시 앱 창 열림
- [x] `data/value-up.db` 파일 생성 확인
- [x] 11개 테이블 생성 확인
- [x] `code_items` seed 데이터 삽입 확인 (54건)
- [x] `address_codes` 데이터 삽입 확인 (20,560건)

---

## 완료 조건 (전부 충족 시 Phase 1 완료)

- [x] 앱이 정상 실행된다
- [x] `data/value-up.db` 파일이 생성된다
- [x] 11개 테이블이 모두 생성된다
- [x] `code_items` seed 데이터가 삽입된다
- [x] `address_codes` 법정동코드 데이터가 삽입된다
- [x] main / preload / renderer 계층이 분리되어 있다

---

## 생성 파일 목록

```
value-up/
├── package.json
├── main/
│   ├── index.js
│   └── db/
│       ├── connection.js
│       ├── schema.sql
│       ├── migrate.js
│       └── seed.js
├── preload/
│   └── index.js
└── renderer/
    └── index.html
```

> `data/` 디렉토리는 런타임 생성 — `.gitignore` 등록 필요

---

## 세션 추가 작업 (2026-03-26, 플랜 외 확정 작업)

- [x] `schema.sql` — `code_items`에 `code_key` 컬럼 추가
- [x] `schema.sql` — `building_use_codes` 테이블 추가 (건축물용도 전체 968건, 검색용)
- [x] `schema.sql` — `users` 테이블 추가 (작성자 등록 UI용)
- [x] `schema.sql` — 총 13개 테이블로 확정 (인덱스 11개)
- [x] `seed.js` — 하드코딩 제거, 소스파일 파싱 기반으로 전면 교체
  - land_category 28건 (지목코드.csv)
  - use_district 20건 (용도지역.csv)
  - zone_district 1,447건 (지구구역.csv)
  - structure_type 44건 (건축물구조.csv)
  - building_type 33건 상위분류 (건축물용도.csv)
  - building_use_codes 968건 전체 (건축물용도.csv)
  - rental_use 5건, vacancy_status 3건 (내부 코드)
  - author → users 테이블로 분리, seed 대상 아님
- [x] `RULES.md` — 하드코딩 금지 원칙 추가
- [x] `.Source-Files/seed-code-items-검토.md` — 코드 데이터 출처 및 상태 관리 문서 작성
- [x] DB 재초기화 검증 완료 (13개 테이블, code_items 1,580건, address_codes 20,560건)
