# 새 프로젝트 초기화 가이드

> AI에게 이 파일을 읽히고 아래 지시문을 주면 된다.
> 매번 설명하지 않아도 이 가이드 하나로 초기화 진행 가능.

---

## AI에게 줄 지시문 (복사해서 사용)

```
NEW-PROJECT-GUIDE.md 읽고, 내가 설명하는 프로젝트 기본 구상에 맞춰
.claude/ 설정 파일들을 초기화해줘.

[여기에 프로젝트 기본 구상 작성]
```

---

## 초기화 전 준비 (사용자가 직접)

### 1. 파일 복사

이전 프로젝트에서 새 프로젝트 루트로 복사:

```
복사 대상:
├─ .claude/          ← 폴더 전체 복사
├─ .agentignore
├─ .claudeignore
├─ .gitignore
├─ .mcp.json
└─ settings.local.json  ← 또는 settings.json (프로젝트마다 다를 수 있음)
```

> **참고 (2026-04-02):** bkit·OMC 플러그인 비활성화 설정을 적용한 프로젝트는
> `settings.local.json` 대신 `settings.json`으로 통합 운용 중.
> `enabledPlugins`를 `settings.local.json`에만 두면 무시되는 버그(CC Issue #27247) 우회 목적.
> 신규 프로젝트 초기화 시 어느 파일을 기준으로 할지 프로젝트별로 확인 필요.

### 2. 복사 후 상태

복사된 `.claude/`에는 이전 프로젝트 내용이 그대로 들어 있다.
AI가 아래 순서로 초기화한다.

### 3. 첫 세션 시작 시 — 게이트 수동 해제 (필수)

새 프로젝트에서 첫 세션을 시작하면 SessionStart 훅이 **존재하지 않는 파일**로
게이트(`.session-gate.json`)를 생성한다.

**원인:** `plans/` 폴더에 `*-master.md`가 없거나, 마스터플랜에 `현재 활성 플랜` 포인터가
없으면 훅이 빈 경로 또는 이전 프로젝트 경로로 required를 설정한다.

**결과:** Read 도구로 아무리 파일을 읽어도 게이트가 해제되지 않아
Bash/Edit/Write가 영구 차단된다.

**해결:** 터미널에서 직접 게이트 파일을 삭제한다.

```
! rm .claude/.session-gate.json
```

이후 AI 초기화 절차(Step 1~6)를 진행한다.
마스터플랜과 페이지플랜이 생성된 이후부터는 다음 세션부터 정상 동작한다.

> **요약**: 새 프로젝트 첫 세션 = 반드시 `! rm .claude/.session-gate.json` 먼저 실행

---

## AI 초기화 순서 (AI가 따를 절차)

### Step 1 — 현황 파악

다음 파일을 읽어 현재 구조 파악:

- `.claude/CLAUDE.md`, `.claude/CONTEXT.md`, `.claude/RULES.md`, `.claude/WORKSPACE.md`
- `plans/` 폴더 전체 (designs/ 포함)
- `.claude/skills/SKILL_GUIDE.md` (스킬 라이브러리 현황)
- `.claude/hooks/HOOK_GUIDE.md` (훅 목록 확인)

### Step 2 — 설정 파일 재작성

사용자가 제공한 프로젝트 구상을 기반으로 아래 파일을 새 프로젝트 내용으로 재작성:

| 파일         | 재작성 내용                                | 포함 금지               |
| ------------ | ------------------------------------------ | ----------------------- |
| `CLAUDE.md`  | 프로젝트 정체성, 작업 원칙                 | 현재 Phase, 현재 플랜명 |
| `CONTEXT.md` | 기술 환경, 디렉토리 구조, 프로젝트 범위    | Phase 현황, 진행 상태   |
| `RULES.md`   | 실행 환경, 프로젝트별 작성 원칙, 금지 사항 | 현재 Phase 정보         |
| `점검-scope.md` | `## 구현 점검 대상` 섹션을 이 프로젝트의 실제 구현 파일 목록으로 교체 | 이전 프로젝트 파일 참조 |

> **원칙**: 설정 파일은 Phase가 바뀌어도 수정할 필요가 없어야 한다.
> 현재 Phase와 진행 상황은 WORKSPACE.md에만 기록한다.

### Step 3 — 마스터플랜 작성

`plans/` 폴더에 마스터플랜 신규 작성:

- 파일명: `{프로젝트명}-master.md` (반드시 `-master.md` 로 끝낼 것 — 훅이 이 패턴으로 탐색)
- 두 번째 줄에 반드시 포함: `**현재 활성 플랜:** \`{페이지플랜 파일명}\``
- 내용: 전체 Phase 체크리스트, Phase별 완료 조건, 결정사항 기록

이전 프로젝트 마스터플랜 파일은 삭제.

### Step 4 — Phase 1 플랜 작성

`plans/` 폴더에 Phase 1 플랜 신규 작성:

- 내용: 작업 항목(체크박스), 완료 조건, 확정 사항
- 반드시 `## 작업 항목` 섹션 포함 (고정 이름 — SessionStart 훅이 이 섹션 경로를 읽기 지시에 포함)

### Step 5 — WORKSPACE.md 초기화

새 WORKSPACE.md 작성 (훅이 기존 파일 존재 시 차단하므로 먼저 이름 변경 필요):

3섹션 구조 고정:
- `## 현재 위치` — 현재 Phase, 상태, 플랜 파일명
- `## 남은 과제` — 플랜 미완료 항목 + 미반영 협의 항목
- `## 진행 이력` — 완료 내역 (최신→과거 순)

### Step 6 — 라이브러리 점검

`.claude/skills/SKILL_GUIDE.md`와 `.claude/hooks/HOOK_GUIDE.md`를 읽고 확인:

- 기존 스킬/훅 중 이 프로젝트에서 활용 가능한 것 파악
- 새로 만들어야 할 것 파악 → Phase 플랜에 항목 추가
- 새로 만든 후 해당 가이드 파일에 추가

---

## 훅 운용 원칙

훅 파일에 프로젝트 경로를 하드코딩하지 않는다.
항상 `__dirname` 기준 상대경로를 사용한다:

```javascript
const ROOT = path.resolve(__dirname, "../..");
```

훅 파일이 `.claude/hooks/` 에 있으므로 `../..` = 프로젝트 루트.
프로젝트명이 바뀌거나 다른 프로젝트로 복사해도 그대로 동작한다.

### SessionStart 훅 구조

파일 내용을 직접 주입하지 않고, Claude에게 순차 읽기 지시만 출력한다:

1. `*-master.md` 패턴으로 마스터플랜 파일명 자동 탐색
2. 마스터플랜의 `**현재 활성 플랜:**` 포인터에서 페이지플랜 파일명 추출
3. 읽어야 할 파일 3개 경로를 포함한 지시문 출력
4. Claude가 Read 도구로 3개 파일을 순서대로 읽음

**읽기 순서 (고정):**
1. 마스터플랜 전체
2. 현재 페이지플랜 `## 작업 항목` 섹션
3. `.claude/WORKSPACE.md` — `## 현재 위치` + `## 남은 과제`

**왜 직접 주입하지 않는가:**
CLAUDE.md는 Claude Code가 항상 먼저 로드한다.
훅이 파일 내용을 직접 주입하면 CLAUDE.md 규칙이 그 내용에 묻혀 무시된다.
지시문만 출력하면 CLAUDE.md → 훅 지시 순서가 유지되고 규칙 준수율이 높아진다.

---

## WORKSPACE.md 운용 원칙

**3섹션 구조 고정** (항상 이 순서):
1. `## 현재 위치` — 항상 읽음
2. `## 남은 과제` — 항상 읽음
3. `## 진행 이력` — 필요할 때만 (최신→과거 순)

- **Edit 도구로만 수정** (훅이 Write 도구 덮어쓰기 차단)
- **새 Phase 시작 시**: 기존 파일 이름 변경 → 새 파일 작성
  - 형식: `WORKSPACE.md` → `WORKSPACE.{현재플랜stem}.md`
  - 예) 활성 플랜이 `phase2-flow.md`이면 → `WORKSPACE.phase2-flow.md`
  - 훅(`protect-phase-transition.js`)이 아카이브 여부를 자동 검증
- **남은 과제**: 완료 전까지 새 WORKSPACE.md에도 계속 포함
- **체크박스 없음**: 서술 방식으로 기록

---

## 라이브러리 운용 원칙

> 스킬 / 훅 / 에이전트는 프로젝트마다 새로 만들지 않는다.
> 한 번 만든 것은 라이브러리로 축적하고, 다음 프로젝트에서 재활용한다.

### 구조

```
.claude/
├─ commands/          # 스킬 파일 (.md)
├─ hooks/             # 훅 스크립트
│   ├─ hooks-guide/   # 훅별 상세 가이드
│   └─ HOOK_GUIDE.md  ← 훅 목록 인덱스
└─ skills/
    └─ SKILL_GUIDE.md ← 스킬 목록 인덱스
```

### SKILL_GUIDE.md 역할 (`.claude/skills/SKILL_GUIDE.md`)

- 현재까지 만들어진 모든 스킬/에이전트 목록
- 각 항목의 용도, 위치, 사용 방법 한 줄 요약
- 새 프로젝트 시작 시 AI가 읽고 활용 가능 항목 파악
- 새 스킬 완성 후 반드시 이 파일에 추가

### HOOK_GUIDE.md 역할 (`.claude/hooks/HOOK_GUIDE.md`)

- 훅 목록 및 간단 개요만 포함 (인덱스 역할)
- 상세 내용은 `.claude/hooks/hooks-guide/` 폴더의 훅별 파일 참조
- 새 훅 추가 시 HOOK_GUIDE.md 목록 + hooks-guide/ 상세 파일 모두 추가

---

## 초기화 완료 기준

- [ ] CLAUDE.md — Phase 정보 없이 재작성
- [ ] CONTEXT.md — Phase 현황 없이 재작성
- [ ] RULES.md — Phase 정보 없이 재작성
- [ ] WORKSPACE.md — Phase 1 시작 전 상태로 초기화
- [ ] `{프로젝트명}-master.md` — 신규 작성 (`-master.md` 접미사 확인)
- [ ] 마스터플랜 두 번째 줄 — `**현재 활성 플랜:** \`파일명\`` 포함 확인
- [ ] Phase 1 플랜 — `## 작업 항목` 섹션 포함하여 `plans/`에 신규 작성
- [ ] 미래 Phase 사전설계 — `plans/designs/`에 작성 (plans/ 직하위 금지)
- [ ] 이전 마스터플랜 파일 — 삭제
- [ ] 훅 경로 점검 (`__dirname` 상대경로 사용 확인)
- [ ] **CODE_DIRS 수정** — `.claude/hooks/check-plan.js` 의 `CODE_DIRS` 배열을 이 프로젝트의 실제 코드 디렉터리로 변경 (기본값 `['main','preload','renderer']`는 Electron 프로젝트 기준)
- [ ] **점검-scope.md 초기화** — `## 구현 점검 대상` 섹션을 이 프로젝트의 실제 구현 파일 목록으로 교체 (이전 프로젝트 파일 참조 제거)
- [ ] `.claude/skills/SKILL_GUIDE.md` — 이 프로젝트에서 활용할 항목 확인 완료
- [ ] `.claude/hooks/HOOK_GUIDE.md` — 활성 훅 목록 확인 완료
- [ ] **init-checklist 생성** — `.Template/.init-checklist.md` 에 이 체크리스트 항목 복사 (미체크 상태). 전항목 완료 전 커밋 불가
