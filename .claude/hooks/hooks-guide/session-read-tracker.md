# PostToolUse(Read) — 읽기 추적 (session-read-tracker.js)

## 목적

Read 도구 실행 후 읽은 파일이 gate의 required 목록에 있는지 확인하고 추적한다.
필수 파일 3개가 모두 읽히면 gate 파일을 삭제하여 차단을 해제한다.

## 트리거

Read 도구 실행 후

## 동작

1. `.claude/.session-gate.json` 존재 여부 확인
2. 없으면 무시 (이미 초기화 완료)
3. Read된 파일 경로를 gate의 required와 대조 (경로 정규화 후 비교)
4. 일치하면 read 배열에 추가
5. read 배열이 required 전체와 일치하면 gate 파일 삭제 → 차단 해제

## 경로 매칭

절대경로로 정규화 후 비교. Windows/Unix 경로 구분자 차이 처리.

## 파일

`.claude/hooks/session-read-tracker.js`

## 연관 훅

- SessionStart: gate 파일 생성
- session-gate.js: gate 존재 시 차단
