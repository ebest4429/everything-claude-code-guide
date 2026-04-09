# 훅 가이드

> 이 프로젝트에서 사용 중이거나 사용했던 훅 목록.
> 새 프로젝트 시작 시 이 파일을 복사하여 필요한 훅을 선택적으로 활성화한다.

---

## 훅 개요

| 훅 이름 | 파일 | 트리거 | 목적 | 상태 |
|---------|------|--------|------|------|
| SessionStart — 컨텍스트 주입 | (inline) | 세션 시작 | WORKSPACE.md + plans/ 전체를 AI 컨텍스트에 주입 | ✅ 활성 |
| PreToolUse(Bash) — 플랜 체크 | `check-plan.js` | git commit/push | 코드가 플랜보다 최신이면 커밋 차단 | ✅ 활성 |
| PostToolUse(Edit/Write) — 플랜 업데이트 알림 | `remind-plan-update.js` | 구현 파일 저장 후 | 플랜 체크박스 업데이트 필요 여부 알림 | ✅ 활성 |

---

## 훅 상세

### 1. SessionStart — 컨텍스트 주입

**목적**: 세션 시작 시 AI에게 현재 작업 컨텍스트를 자동으로 제공

**트리거**: 매 세션 시작

**효과**:
- WORKSPACE.md (현재 Phase + 상태) 자동 로드
- plans/*.md 전체 자동 로드
- AI가 이전 세션 결과를 별도 요청 없이 파악

**JSON**:
```json
{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "echo '========== WORKSPACE ==========' && cat .claude/WORKSPACE.md && echo '' && echo '========== PLANS ==========' && for f in .claude/plans/*.md; do [ -f \"$f\" ] && echo \"--- $(basename $f) ---\" && cat \"$f\" && echo ''; done"
        }
      ]
    }
  ]
}
```

---

### 2. PreToolUse(Bash) — 플랜 체크 (check-plan.js)

**목적**: 커밋 전 현재 활성 플랜 문서가 최신 상태인지 검증

**트리거**: Bash 도구 실행 전 (git commit / git push 명령에만 실제 검사)

**동작**:
1. `WORKSPACE.md`의 "현재 플랜" 항목에서 활성 플랜 파일 경로 파싱
2. `main/`, `preload/`, `renderer/` 내 파일 최신 수정시간 조회
3. 활성 플랜 파일 수정시간 조회
4. 코드 > 플랜이면 stderr에 경고 출력 + exit(2)로 커밋 차단

**핵심 설계**: plans/ 전체가 아닌 WORKSPACE.md에 명시된 현재 플랜만 감시
→ 완료된 플랜은 동결 상태로 보존되며 감시 대상에서 자동 제외

**우회**: 명령에 `SKIP_PLAN_CHECK=1` 포함 시 검사 통과

**파일**: `.claude/hooks/check-plan.js`

**JSON**:
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "node .claude/hooks/check-plan.js"
        }
      ]
    }
  ]
}
```

---

### 3. PostToolUse(Edit/Write) — 플랜 업데이트 알림 (remind-plan-update.js)

**목적**: 구현 파일 수정 직후 플랜 체크박스 업데이트 필요를 AI에게 상기

**트리거**: Edit 또는 Write 도구 실행 후

**동작**:
- `.js`, `.html`, `.sql`, `.css` 파일 수정 시에만 동작
- `.claude/` 내부 파일은 제외 (플랜/설정 파일 수정 시 불필요)
- 구현 파일 수정 시 컨텍스트에 알림 메시지 출력

**파일**: `.claude/hooks/remind-plan-update.js`

**JSON**:
```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "hooks": [{ "type": "command", "command": "node .claude/hooks/remind-plan-update.js" }]
    },
    {
      "matcher": "Write",
      "hooks": [{ "type": "command", "command": "node .claude/hooks/remind-plan-update.js" }]
    }
  ]
}
```

---

## 새 프로젝트 적용 절차

1. `.claude/` 폴더 전체를 새 프로젝트로 복사
2. `HOOK_GUIDE.md` 를 읽고 필요한 훅 선택
3. `settings.json` 의 훅 JSON을 새 프로젝트에 맞게 조정
4. `check-plan.js` 의 `ROOT` 경로 수정
5. `remind-plan-update.js` 의 경로 수정 (절대경로 사용 시)
6. `npm start` 또는 Claude Code 재시작으로 훅 활성화 확인

---

## 향후 추가 가능 훅 아이디어

| 아이디어 | 트리거 | 목적 |
|---------|--------|------|
| WORKSPACE 자동 업데이트 | PostToolUse(Edit) | 플랜 파일 수정 시 WORKSPACE.md 업데이트 안내 |
| Phase 범위 초과 경고 | PreToolUse(Write) | 현재 Phase 외 파일 신규 생성 시 경고 |
| Source-Files 수정 차단 | PreToolUse(Edit) | `.Source-Files/` 내 파일 수정 시도 차단 |
