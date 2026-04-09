# PreToolUse(Write) — WORKSPACE 보호 (protect-workspace.js)

## 목적

WORKSPACE.md를 Write 도구로 덮어쓰는 것을 차단한다.
WORKSPACE.md는 반드시 Edit 도구로만 수정 가능하도록 강제한다.

## 트리거

Write 도구 실행 전

## 동작

- 대상 파일이 `WORKSPACE.md`이면 차단 + 안내 메시지 출력
- 파일이 아직 존재하지 않으면 최초 생성 허용
- 기존 파일을 다른 이름으로 변경한 후 새 WORKSPACE.md 작성은 허용

## 핵심 설계

WORKSPACE.md는 진행 이력이 누적되는 파일이므로 실수로 전체 덮어쓰기 방지가 중요.
새 Phase 시작 시: 기존 파일을 `WORKSPACE.{플랜명}.md`로 이름 변경 → 새 파일 Write 허용.

## 버그 이력

- 초기 정규식 `/[/\\]?WORKSPACE\.md$/i` — 슬래시가 선택적이어서 `protect-workspace.md` 등 파일명에 `workspace.md`가 포함된 파일도 차단하는 오탐 발생
- 수정: `/[/\\]WORKSPACE\.md$/i` — 슬래시 필수로 변경, 절대경로에서만 정확히 동작

## 파일

`.claude/hooks/protect-workspace.js`

## JSON

```json
{
  "PreToolUse": [
    {
      "matcher": "Write",
      "hooks": [
        {
          "type": "command",
          "command": "node .claude/hooks/protect-workspace.js"
        }
      ]
    }
  ]
}
```
