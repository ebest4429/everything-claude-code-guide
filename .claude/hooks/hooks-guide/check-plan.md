# PreToolUse(Bash) — 플랜 체크 (check-plan.js)

## 목적

커밋 전 현재 활성 플랜 문서가 최신 상태인지 검증한다.
코드가 플랜보다 최신이면 "플랜을 먼저 업데이트하라"는 경고와 함께 커밋을 차단한다.

## 트리거

Bash 도구 실행 전 (git commit / git push 명령에만 실제 검사 수행)

## 동작

1. `.claude/WORKSPACE.md`의 "현재 플랜" 항목에서 활성 플랜 파일 경로 파싱
2. `main/`, `preload/`, `renderer/` 내 파일 최신 수정시간 조회
3. 활성 플랜 파일 수정시간 조회
4. 코드 > 플랜이면 stderr에 경고 출력 + exit(2)로 커밋 차단

## 핵심 설계

`plans/` 전체가 아닌 WORKSPACE.md에 명시된 현재 플랜만 감시.
완료된 플랜은 동결 상태로 보존되며 감시 대상에서 자동 제외.

## 우회

명령에 `SKIP_PLAN_CHECK=1` 포함 시 검사 통과.

## 파일

`.claude/hooks/check-plan.js`

## JSON

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
