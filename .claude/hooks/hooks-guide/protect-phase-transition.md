# protect-phase-transition.js 가이드

## 목적

새 페이지플랜을 `plans/` 직하위에 Write할 때 WORKSPACE.md 아카이브 여부를 강제 확인한다.
Phase 전환 시 WORKSPACE.md를 Edit으로 덮어쓰는 문제를 구조적으로 방지한다.

---

## 트리거 조건

| 항목 | 값 |
|------|-----|
| 이벤트 | PreToolUse(Write) |
| 대상 | `.claude/plans/*.md` (직하위만, designs/ 등 하위 폴더 제외) |
| 제외 | `*-master.md`, 활성 플랜과 동일 파일 재작성, 초기화 중(활성 플랜 없음) |

---

## 동작

1. Write 대상이 `plans/` 직하위 `.md` 파일인지 확인
2. 마스터플랜에서 현재 활성 플랜 파일명 추출
3. `WORKSPACE.{활성플랜stem}.md` 아카이브 존재 여부 확인
4. 아카이브 없으면 → exit(2) 차단 + 처리 순서 안내

---

## Phase 전환 올바른 순서

```
1. Bash: mv .claude/WORKSPACE.md .claude/WORKSPACE.{현재플랜stem}.md
2. Write: 새 WORKSPACE.md 작성
3. Edit: 마스터플랜 활성 플랜 포인터 업데이트
4. Write: 새 페이지플랜 작성 → 이 시점에 훅 통과
```

---

## designs/ 파일과의 관계

`plans/designs/`에 있는 사전설계 파일은 이 훅의 대상이 아니다.
Phase가 활성화될 때 `plans/designs/{파일}` 을 참조하여 `plans/`에 새 플랜을 Write하는 시점에만 훅이 발동한다.

---

## 돌발상황(hotfix) 플랜

활성 플랜을 뒤로 돌리지 않고 `plans/hotfix-{날짜}-{설명}.md` 형태로 임시 플랜을 작성한다.
이 경우도 WORKSPACE 아카이브가 없으면 차단된다.
hotfix 완료 후 원래 Phase로 복귀 시 동일 절차 적용.
