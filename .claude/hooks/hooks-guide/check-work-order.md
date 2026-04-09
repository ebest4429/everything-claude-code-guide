# PreToolUse(Edit) — 작업 순서 체크 (check-work-order.js)

## 목적

플랜 항목 없이 구현을 시작하는 순서 위반을 감지한다.
"구현 먼저 → 나중에 플랜 업데이트" 패턴을 차단한다.

## 트리거

Edit 도구 실행 전

## 동작

- 구현 파일(`.js`, `.html`, `.css`, `.md` 등) 수정 시 활성 플랜에 해당 작업이 등록되어 있는지 확인
- 플랜에 없는 작업이면 경고 메시지 출력

## 파일

`.claude/hooks/check-work-order.js`

## JSON

```json
{
  "PreToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "command",
          "command": "node .claude/hooks/check-work-order.js"
        }
      ]
    }
  ]
}
```
