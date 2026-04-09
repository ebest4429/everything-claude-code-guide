# SessionStart — 세션 게이트 생성

## 목적

세션 시작 시 `.session-gate.json`을 생성하여 필수 파일 3개 읽기 전까지
Bash/Edit/Write를 기술적으로 차단한다.
Claude Code 런타임이 실행 — Claude(AI) 판단과 무관하게 보장됨.

## 트리거

매 세션 시작

## 동작

1. `*-master.md` 패턴으로 마스터플랜 파일명 자동 탐색
2. 마스터플랜의 `**현재 활성 플랜:**` 포인터에서 페이지플랜 파일명 추출
3. `.claude/.session-gate.json` 생성 — required 3개 파일 경로 기록
4. 필수 읽기 파일 목록 출력

## gate 파일 구조

```json
{
  "required": ["마스터플랜경로", "활성플랜경로", ".claude/WORKSPACE.md"],
  "read": []
}
```

## 이전 방식과의 차이

| 이전 | 현재 |
|------|------|
| 마스터플랜 전체 주입 (텍스트, 강제력 없음) | gate 파일 생성 (기술적 강제) |
| "읽을까요?" 질문 (Claude 판단 의존) | PreToolUse exit(2) 차단 (Claude 판단 불필요) |

## JSON (settings.json 등록 위치)

```json
{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "MASTER=$(ls .claude/plans/*-master.md 2>/dev/null | head -1) && ACTIVE=$(grep '현재 활성 플랜' \"$MASTER\" 2>/dev/null | grep -o '`[^`]*`' | tr -d '`') && env MASTER=\"$MASTER\" ACTIVE=\"$ACTIVE\" node -e \"var fs=require('fs'),g={required:[process.env.MASTER,'.claude/plans/'+process.env.ACTIVE,'.claude/WORKSPACE.md'],read:[]};fs.writeFileSync('.claude/.session-gate.json',JSON.stringify(g,null,2))\" && echo '========== 세션 시작 ==========' && echo '' && echo '아래 3개 파일을 Read 도구로 읽어야 Bash/Edit/Write가 해제됩니다.' && echo '' && echo \"1. $MASTER\" && echo \"2. .claude/plans/$ACTIVE\" && echo '3. .claude/WORKSPACE.md'"
        }
      ]
    }
  ]
}
```
