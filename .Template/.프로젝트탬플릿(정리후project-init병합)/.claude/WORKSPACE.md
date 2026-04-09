# WORKSPACE.md

> 세션 시작 시 읽는다.
> **기본 읽기**: 현재 위치 + 남은 과제까지.
> **진행 이력**: 필요할 때만 추가 요청.

---

## 현재 위치

| 항목 | 값 |
|------|-----|
| PROJECT | 재정계획 스킬 |
| 현재 Phase | Phase 1 — 스킬 재작성 |
| 상태 | 🔄 진행 중 — 점검 스킬 2종 구현 완료, 스킬 UX 수정 대기 |
| 현재 플랜 | `.claude/plans/스킬수정플랜.md` |
| 전체 플랜 | `.claude/plans/재정계획-master.md` |

---

## 남은 과제

**플랜 미완료** (`.claude/plans/스킬수정플랜.md` 상세 참조):
- 🔲 **Step 4 UX 구조 수정** — 전체 목록+★추천 통합, `-번호` 제거 문법, Step 2+4 통합 여부 (협의 후 구현)
- 🔲 **소스 데이터 연결 로직 설계** — 소스 파일 형식·위치, 폴백 처리 (협의 후 설계)

**미반영 (협의 필요)**:
- 전체 5단계 흐름 중복·비효율 점검
- 파일 간 참조·연결 유효성 점검

---

## 진행 이력

### 2026-04-02 점검 스킬 2종 구현

| 항목 | 내용 |
|------|------|
| 점검-scope.md | `.claude/점검-scope.md` — 기본 대상(설정파일+훅가이드+스킬가이드) + 프로젝트 추가 대상 + 구현 점검 대상 분리 구조 |
| 점검-연결.md | `.claude/commands/점검-연결.md` — 설정 파일 간 경로·포인터·훅 구조 유기적 연결 점검 |
| 점검-구현.md | `.claude/commands/점검-구현.md` — 플랜 체크박스 ↔ 실제 구현 파일 갭 점검 |
| 결과 저장 | `.claude/점검결과/연결-YYYYMMDD.md`, `구현-YYYYMMDD.md` — 점검 시 자동 생성 |
| 설계 원칙 | 분리 원칙 / scope 파일 수동 지정 / 결과 파일 저장 / 컨텍스트 초과 시 외부 환경(1M API, Gemini) 활용 |

---

### 2026-04-02 세션 게이트 구현 (exit(2) 강제차단)

| 항목 | 내용 |
|------|------|
| session-gate.js | PreToolUse(Bash/Edit/Write) — gate 존재 시 exit(2) 차단 |
| session-read-tracker.js | PostToolUse(Read) — 필수 파일 읽기 추적, 완료 시 gate 삭제 |
| settings.json | SessionStart gate 생성 + 신규 훅 2개 등록 |
| CLAUDE.md | 세션 시작 섹션 — gate 구조로 업데이트 |
| HOOK_GUIDE.md | 신규 훅 2개 목록 추가 |
| hooks-guide/ | session-gate.md, session-read-tracker.md, session-start.md 업데이트 |
| .gitignore | .session-gate.json 런타임 파일 제외 추가 |

---

### 2026-04-02 SessionStart 훅 구조 개선 + 가이드 정비

| 항목 | 내용 |
|------|------|
| SessionStart 훅 변경 | 마스터플랜 전체 주입 제거 → 3파일 순차 읽기 지시문으로 교체 (컨텍스트 과부하 해소) |
| protect-workspace.js 버그 수정 | 정규식 `?` 제거 — `protect-workspace.md` 등 오탐 방지 |
| HOOK_GUIDE.md 재편 | 목록+개요 인덱스로 축소, 상세 내용 hooks-guide/로 이관 |
| hooks/hooks-guide/ 신규 | 훅별 상세 가이드 5개 생성 (session-start, check-plan, check-work-order, protect-workspace, remind-plan-update) |
| NEW-PROJECT-GUIDE.md 보완 | SessionStart 설명 업데이트, 파일 경로 명시, SKILL/HOOK_GUIDE 역할 정리 |
| CLAUDE.md 경로 수정 | WORKSPACE.md 등 파일 경로 `.claude/` 명시 |

---

### 2026-04-02 플러그인 충돌 해소 및 구조 진단

| 항목 | 내용 |
|------|------|
| bkit-starter 원인 확인 | `hooks/session-start.sh`가 SessionStart에 강제 주입 — 프로젝트 훅과 충돌 |
| bkit-starter 전역 비활성화 | `~/.claude/settings.json` `enabledPlugins: false` 적용 |
| settings 단일화 | settings.local.json → settings.json 통합 (enabledPlugins 버그 우회) |
| DISABLE_OMC=1 | 이 프로젝트에서 OMC 비활성화 (settings.json env) |
| 구조 진단 | 훅 주입이 데이터만 전달하고 CLAUDE.md 행동 지시와 연결되지 않는 구멍 확인 |
| SessionStart 훅 수정 | 마지막에 "CLAUDE.md 세션 시작 절차를 따른다" 지시 추가 |
| 플러그인 제어 가이드 | `.Template/Bkit 제어/플러그인-제어-가이드.md` 작성 및 업데이트 |

---

### 스킬 실행 검증 완료 + 구조 문제 발견 (2026-04-02)

대전광역시 기준으로 `/재정계획` 실행 완료. 파일 2종 생성 확인.
실행 중 Step 4에서 구조적 UX 문제 발견 → 다음 세션에서 수정 진행.

| 문제 | 내용 |
|------|------|
| 번호 없는 목록에서 번호 입력 요구 | 초기 화면에 추천 분야 번호 없이 나열 → 혼란 |
| 전체 목록 2단계 분리 | 'ㄷ' 눌러야 등장 → 맥락 단절 |
| 토글 비직관적 | 기선택 번호 재입력 시 제거 → 의도와 불일치 |

미확인 사항: 전체 5단계 흐름의 중복·비효율 여부 (다음 세션 재협의)

---

### NotebookLM_프롬프트.md + Claude_세션1_시작프롬프트.md 동적 생성 로직 구체화 (2026-04-02)

| 항목 | 내용 |
|------|------|
| 파일 1 설계 원칙 | 분야명 기반 추출 (키워드 하드코딩 제거) — 지자체 독립적 동작 |
| 파일 1 섹션 구조 | 고정 서두 + 선택 분야별 섹션 (12대분류 번호 순) + 데이터 2·3번 조건부 섹션 + 고정 마무리 |
| 파일 1 추출 지시 | 분야명 분야의 모든 세부사업 추출, 사업개요 있는 행만, 원문 그대로, 중복 포함 |
| 파일 2 설계 원칙 | 선택 분야 수만큼 Phase 자동 구성, 마지막 Phase 종합 인사이트 |
| 파일 2 섹션 구조 | 목적+기간+데이터+분야 헤더 + 전체 로드맵 + 세션1 요청 |
| 분야-키워드 매핑표 | 제거 — 분야명 기반 방식으로 완전 대체 |

---

### 2026-04-02 샘플 기반 수정 사항 반영 완료

| 항목 | 내용 |
|------|------|
| Step 1 수정 | 자유 단위 입력 구조 (광역~기초단체), 약칭 규칙 추가 (경기화성·대전서구·충북옥천 형식) |
| Step 2 수정 | 다중선택 구조 전환 (9개 목적 항목 + 직접입력), 12개 대분류 기반 목적→분야 추천 매핑표 |
| Step 3 수정 | PDF 전처리 안내 추가 (EZPDF→Microsoft Print to PDF 권장, 인식 불가 형식 경고) |
| Step 4 수정 | 전체 분야 목록 12개 대분류 기준으로 교체 (기존 임시 그룹 목록 제거) |
| 한자 제거 | 析·分 문자 전체 치환 완료 (분석→분석), grep 확인 zero |
| 어노테이션 제거 | 샘플의 `- 수정:` 인라인 주석 전체 제거 |

---

### 2026-04-01 플랜 정리 완료

| 항목 | 내용 |
|------|------|
| 세션 목표 | 플랜 완성 및 정리만 (구현 없음) |
| 12개 대분류 확보 | `.Source-Files/중기지방재정계획 노토북LM 요청 및 결과.md` 에서 확인 |
| 보류 해제 | Step 2/4 분야 목록 — 12개 대분류 확정으로 보류 해제 |
| 스킬수정플랜.md 업데이트 | Step 2 다중선택 화면 구조 확정, Step 4 분야 목록 12개 대분류로 교체, 목적-분야 추천 매핑표 재구성 |
| 구현 스펙 추가 | 스킬수정플랜.md에 스펙 1~3 추가 — 다음 세션 바로 구현 가능 수준 |

---

### 2026-04-01 세션 자동주입 구조 개선 완료

| 항목 | 내용 |
|------|------|
| settings.local.json | SessionStart 훅 재작성 — 마스터플랜 전체 + 페이지플랜 `## 작업 항목` 섹션만 주입 |
| 재정계획-master.md | 상단에 `**현재 활성 플랜:** \`스킬수정플랜.md\`` 포인터 추가 |
| CLAUDE.md | 세션 시작 섹션 재작성 + 페이지플랜 규칙 추가 |
| NEW-PROJECT-GUIDE.md | 마스터플랜 포인터 규칙, `## 작업 항목` 고정 규칙, SessionStart 훅 구조 설명 추가 |
| 주입 크기 | 714줄(14.6KB) → 약 175줄 (76% 감소) |
| WORKSPACE.md | 자동 주입 대상에서 제외 — 세션 시작 시 사용자가 읽기 여부 결정 |
| HOOK_GUIDE.md | SessionStart 상세 업데이트 + check-work-order.js, protect-workspace.js 누락 항목 추가 |

---

### 2026-04-01 PDF 전처리 검증 및 스킬 샘플 수정 협의

| 항목 | 내용 |
|------|------|
| 스킬 샘플 작성 | `.claude/commands/재정계획.md` 샘플 완성 |
| PDF 전처리 확정 | 원본 EZPDF → Microsoft Print to PDF → NotebookLM (인식 성공 확인) |
| 한컴/PDF2022 추출본 | NotebookLM 인식 불가 확인 (폰트 인코딩 문제) |
| Step 1 수정 방향 | 지자체 단위를 구·시 레벨까지 지정 가능, 약칭 형식 변경 |
| Step 2 수정 방향 | 목적 선택 다중선택 구조, 대분류 데이터 확보 후 업데이트 예정 |
| Step 3 수정 방향 | PDF 전처리 안내 추가, 구별 데이터는 기타(5번)로 처리 |
| Step 4 수정 방향 | 전체 분야 목록 중기재정계획 대분류 기반 재구성 예정 |

---

### 2026-04-01 프로젝트 구조 정비 완료 (2차)

| 항목 | 내용 |
|------|------|
| 구조 문제 파악 | 설정파일(CLAUDE.md 등)이 페이지 플랜을 중심으로 작성되어 있었음 |
| 훅 경로 수정 | 3개 훅 ROOT 하드코딩 → `path.resolve(__dirname, '../..')` 상대경로로 수정 |
| 새 훅 추가 | protect-workspace.js — WORKSPACE.md Write 차단 (이름 변경 후 새 파일 허용) |
| settings.local.json | PreToolUse(Write) → protect-workspace.js 등록 |
| CLAUDE.md | Phase 정보 제거, 마스터플랜 참조로 재작성, WORKSPACE.md 운용 원칙 현실화 |
| CONTEXT.md | Phase 현황 제거, 파일명 오류 수정(분석용→Claude_세션1_시작프롬프트), 프로젝트 범위 명시 |
| RULES.md | Phase 정보 제거, 파일명 오류 수정, CONTEXT.md 삭제된 항목 제거 |
| NEW-PROJECT-GUIDE.md | 올바른 구조 기반으로 전면 재작성 |

---

### 2026-04-01 설계 협의 완료

| 항목 | 내용 |
|------|------|
| 스킬 목적 확정 | 완성된 프롬프트 2종 직접 생성 (NotebookLM_프롬프트.md + Claude_세션1_시작프롬프트.md) |
| 동적 생성 원리 확정 | 사용자 목적 → 분야 자동 추천 → 확정 → 선택 분야 기반 2종 동적 생성 |
| 분야 선택 이유 확정 | 방대한 재정계획 데이터 → 목적별 필터링 필수 → 컨텍스트 절약 |
| 전체 워크플로우 작성 | 재정계획-master.md 에 워크플로우 다이어그램 추가 |
| 대전 기존 결과물 분석 | 대전광역시-재정분석/ 3종 파일 구조 확인 → 스킬 설계 반영 |
| 한자 오염 원인 파악 | Claude Desktop 생성 파일의 析 문자가 CLI 세션 컨텍스트에 전파된 것 확인 |
| 한자 오염원 격리 | 재정분석.md → .Source-Files/재정계획-폐기버전.md 이동 완료 |

---

### 2026-03-31 프로젝트 정비 완료

| 항목 | 내용 |
|------|------|
| CLAUDE.md | 재정계획 스킬 프로젝트 기준으로 전면 재작성 |
| CONTEXT.md | 재정계획 스킬 구조로 전면 재작성 |
| RULES.md | 스킬 작성 원칙 기준으로 전면 재작성 |
| 재정계획-master.md | 마스터플랜 신규 작성 |
| 스킬수정플랜.md | Phase 1 플랜 형식으로 재작성 |
| WORKSPACE.md | 재정계획 스킬 프로젝트 기준으로 재작성 |
| NEW-PROJECT-GUIDE.md | 새 프로젝트 초기화 가이드 신규 작성 |
| HOOK_GUIDE.md | .claude/hooks/ → .claude/ 루트로 이동 |

