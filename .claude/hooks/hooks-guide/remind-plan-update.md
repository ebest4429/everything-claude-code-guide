# PostToolUse(Edit/Write) — 플랜 업데이트 알림 (remind-plan-update.js)

## 목적

구현 파일 수정 직후 플랜 체크박스 업데이트 필요를 Claude에게 상기시킨다.
"구현 완료 후 플랜 업데이트를 잊는" 패턴을 방지한다.

## 트리거

Edit 또는 Write 도구 실행 후

## 동작

- `.js`, `.html`, `.sql`, `.css` 파일 수정 시에만 동작
- `.claude/` 내부 파일은 제외 (플랜·설정 파일 수정 시 불필요)
- 구현 파일 수정 시 컨텍스트에 알림 메시지 출력

## 파일

`.claude/hooks/remind-plan-update.js`

## JSON

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "command",
          "command": "node .claude/hooks/remind-plan-update.js"
        }
      ]
    },
    {
      "matcher": "Write",
      "hooks": [
        {
          "type": "command",
          "command": "node .claude/hooks/remind-plan-update.js"
        }
      ]
    }
  ]
}
```
