# 훅 가이드

> 훅 목록 및 간단 개요. 상세 내용은 각 훅의 가이드 파일 참조.
> 상세 파일 위치: `.claude/hooks-guide/`

---

## 훅 목록

| 훅 이름 | 파일 | 트리거 | 목적 | 상태 | 상세 |
|---------|------|--------|------|------|------|
| SessionStart — 세션 게이트 생성 | (inline) | 세션 시작 | .session-gate.json 생성 → 3개 파일 읽기 전 Bash/Edit/Write 차단 | ✅ 활성 | [상세](hooks-guide/session-start.md) |
| PreToolUse(Bash/Edit/Write) — 세션 게이트 | `session-gate.js` | Bash/Edit/Write 실행 전 | gate 존재 시 exit(2) 차단 | ✅ 활성 | [상세](hooks-guide/session-gate.md) |
| PostToolUse(Read) — 읽기 추적 | `session-read-tracker.js` | Read 실행 후 | 필수 파일 읽기 완료 추적, 완료 시 gate 삭제 | ✅ 활성 | [상세](hooks-guide/session-read-tracker.md) |
| PreToolUse(Bash) — 플랜 체크 | `check-plan.js` | git commit/push | 코드가 플랜보다 최신이면 커밋 차단 | ✅ 활성 | [상세](hooks-guide/check-plan.md) |
| PreToolUse(Edit) — 작업 순서 체크 | `check-work-order.js` | Edit 실행 전 | 플랜 항목 없이 구현 시작 시 경고 | ✅ 활성 | [상세](hooks-guide/check-work-order.md) |
| PreToolUse(Write) — WORKSPACE 보호 | `protect-workspace.js` | Write 실행 전 | WORKSPACE.md 덮어쓰기 차단 | ✅ 활성 | [상세](hooks-guide/protect-workspace.md) |
| PreToolUse(Write) — Phase 전환 게이트 | `protect-phase-transition.js` | Write 실행 전 | 새 페이지플랜 작성 시 WORKSPACE 아카이브 여부 강제 확인 | ✅ 활성 | [상세](hooks-guide/protect-phase-transition.md) |
| PostToolUse(Edit/Write) — 플랜 알림 | `remind-plan-update.js` | 구현 파일 저장 후 | 플랜 체크박스 업데이트 상기 | ✅ 활성 | [상세](hooks-guide/remind-plan-update.md) |

---

## 새 프로젝트 적용 절차

1. `.claude/` 폴더 전체를 새 프로젝트로 복사
2. `HOOK_GUIDE.md` 읽고 필요한 훅 선택
3. `settings.json` 훅 JSON 확인 (하드코딩 경로 없음 — 그대로 사용 가능)
4. 마스터플랜 파일명 `-master.md` 로 끝나도록 작성
5. 마스터플랜 상단에 `**현재 활성 플랜:** \`파일명\`` 포인터 추가
6. 새 페이지플랜에 `## 작업 항목` 섹션 포함
7. Claude Code 재시작으로 훅 활성화 확인

---

## 향후 추가 가능 훅 아이디어

| 아이디어 | 트리거 | 목적 |
|---------|--------|------|
| 초기화 체크리스트 게이트 | PreToolUse(Bash) git commit | `.Template/.init-checklist.md` 미완료 항목 있으면 커밋 차단 |
| WORKSPACE 자동 업데이트 알림 | PostToolUse(Edit) | 플랜 파일 수정 시 WORKSPACE.md 업데이트 안내 |
| Phase 범위 초과 경고 | PreToolUse(Write) | 현재 Phase 외 파일 신규 생성 시 경고 |
| Source-Files 수정 차단 | PreToolUse(Edit) | `.Source-Files/` 내 파일 수정 시도 차단 |
