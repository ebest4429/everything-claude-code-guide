# CONTEXT.md

## 프로젝트 정체성

**value-up — 부동산 매물관리 및 수익률 분석 시스템**
Excel 기반 구조를 SQLite 기반 Electron 데스크톱 앱으로 재구축.
로컬 전용. 배포 없음. 단일 사용자 업무용 애플리케이션.

---

## 기술 스택

| 항목 | 내용 |
|------|------|
| Shell | Electron |
| UI | HTML + CSS + JavaScript (프레임워크 없음) |
| DB | SQLite (better-sqlite3) |
| Excel | exceljs (import/export 보조) |
| 실행 | 로컬 전용 (`npm start`) |

---

## 계층 구조

```
Renderer (UI/DOM)
   ↓ window.appApi.*
Preload (API 브릿지)
   ↓ IPC
Main Process
   ↓
Service Layer → Repository Layer → SQLite / File System
```

---

## 디렉토리 구조

```
value-up/
├── main/
│   ├── db/              # DB 연결, schema.sql, migration, seed
│   ├── repositories/    # 테이블 단위 CRUD
│   ├── services/        # 비즈니스 흐름, 트랜잭션
│   └── ipc/             # IPC 채널 등록
├── preload/
│   └── index.js         # window.appApi 노출
├── renderer/
│   ├── index.html
│   ├── form/            # 섹션별 폼 모듈
│   ├── components/      # 재사용 UI 컴포넌트
│   ├── utils/           # format, validate, mapper, calculator
│   └── print/           # 인쇄 제어
├── data/
│   └── uploads/         # 이미지 파일 저장
├── .Source-Files/       # 기획 문서 (읽기 전용)
└── .claude/             # Claude Code 설정
```

---

## Phase 현황

| Phase | 내용 | 상태 |
|-------|------|------|
| 1 | 프로젝트 골격 (Electron + SQLite 초기화) | ✅ 완료 |
| 2 | 데이터 레이어 (Repository + Service + IPC) | ✅ 완료 |
| 3 | 기본 UI (기본정보 / 건축물 / 토지 / 매매) | ✅ 완료 |
| 보완 B1~B8 | rental_use/property_type/도로명/입력규칙/다중지번 등 | ✅ 완료 |
| 4 | 임대현황 및 수익률 계산 | ✅ 완료 |
| 5 | 보안정보 및 이미지 | ✅ 완료 |
| 6 | 인쇄 (Pretendard + @media print + 미리보기) | ✅ 기능 완료 동결 |
| 보완2 | 주소구조 수정(이슈1) + 토지 지번 추가(이슈2) + 빌드 경로 분기(이슈3) | ✅ 완료 |
| 7 | Excel import/export (exceljs, 9시트) | ✅ 기능 완료 동결 |
| 기능 보완 | Phase 1~5 구조 보완 + 목록탭 + 설정탭 | 🔄 진행 예정 |
| 8 | 백업/복원 및 마감 (패키징) | ⏸ 보류 |

---

## DB 테이블 목록 (14개)

| 테이블 | 유형 | 설명 |
|--------|------|------|
| `properties` | 단일행 | 매물 기본정보 (마스터) |
| `building_info` | 단일행 | 건축물정보 |
| `land_info` | 단일행 | 토지이용정보 (대표 지번) |
| `land_parcels` | 다중행 | 추가 지번 (보완2 이슈2 추가) |
| `sale_info` | 단일행 | 매매 및 수익률 정보 |
| `rental_units` | 다중행 | 임대현황 |
| `owners` | 다중행 | 소유주 |
| `tenants` | 다중행 | 임차인 |
| `consultations` | 다중행 | 상담내역 |
| `property_images` | 다중행 | 이미지 메타데이터 |
| `building_use_codes` | 참조 | 건축물용도 전체 968건 (검색용) |
| `address_codes` | 참조 | 법정동코드 |
| `users` | 참조 | 작성자 등록 |
| `code_items` | 참조 | 공통코드 (지목, 용도지역, 건축물구조 등) |

---

## IPC 네임스페이스

| 네임스페이스 | 담당 |
|-------------|------|
| `property:` | 매물 CRUD |
| `codes:` | 코드 조회 |
| `address:` | 주소 조회 |
| `image:` | 이미지 저장/삭제 |
| `excel:` | import/export |
| `backup:` | 백업/복원 |
