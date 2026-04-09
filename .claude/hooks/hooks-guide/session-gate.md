# PreToolUse(Bash/Edit/Write) — 세션 게이트 (session-gate.js)

## 목적

세션 초기화 미완료 시 Bash/Edit/Write 도구를 기술적으로 차단한다.
필수 파일 3개를 Read 완료하기 전까지 어떤 변경도 불가능하게 강제한다.

## 트리거

Bash, Edit, Write 도구 실행 전

## 동작

1. `.claude/.session-gate.json` 존재 여부 확인
2. 없으면 통과
3. 있으면 미읽은 파일 목록 확인
4. 미읽은 파일 있으면 목록 출력 + exit(2) 차단
5. 모두 읽혔으면 gate 삭제 후 통과

## gate 파일 구조

```json
{
  "required": [
    ".claude/plans/재정계획-master.md",
    ".claude/plans/스킬수정플랜.md",
    ".claude/WORKSPACE.md"
  ],
  "read": []
}
```

## 파일

`.claude/hooks/session-gate.js`

## 연관 훅

- SessionStart: gate 파일 생성
- session-read-tracker.js: read 배열 업데이트 + gate 삭제
