<!--
스킬명    : archive-workspace
호출 방법 : "워크스페이스 아카이브해" / "archive workspace" / "워크스페이스 정리"
목적      : 현재 WORKSPACE.md를 날짜/Phase 기반 파일명으로 .claude/archive/ 에 보존하고
           새 WORKSPACE.md 작성을 준비한다.
호출 조건 : 페이지 플랜 전환 시점 — 사용자가 명시적으로 호출할 때만 실행
주의      : 복수 플랜이 WORKSPACE.md에 혼재할 경우 사용자가 내용을 검토 후 호출할 것
-->

# archive-workspace 스킬

## 실행 순서

### 1단계 — 현재 WORKSPACE.md 읽기
- `.claude/WORKSPACE.md` 내용 전체 읽기
- "현재 Phase" 항목에서 Phase 명칭 파악
  - 예: "Phase 4 — 임대현황 및 수익률" → `phase4`
  - 정식 Phase가 아닌 경우(보완 등) → 날짜만 사용

### 2단계 — 아카이브 파일명 결정
```
형식: WORKSPACE.{phase명}.{YYYY-MM-DD}.md
예시: WORKSPACE.phase4.2026-03-26.md
      WORKSPACE.보완.2026-03-27.md
```

### 3단계 — 아카이브 실행
- `.claude/archive/` 폴더가 없으면 생성
- 현재 WORKSPACE.md 내용을 `.claude/archive/{파일명}` 으로 Write (복사)
- 원본 WORKSPACE.md는 건드리지 않음 (덮어쓰기 금지)

### 4단계 — 사용자 확인
- 아카이브 완료 사실과 경로를 사용자에게 보고
- "새 WORKSPACE.md를 작성할까요?" 질문

### 5단계 — 새 WORKSPACE.md 작성 (사용자 승인 시)
아래 템플릿으로 새 WORKSPACE.md 작성:

```markdown
# WORKSPACE.md

> 세션 시작 시 가장 먼저 읽는다.
> 현재 위치 확인 전용. 상세 내용은 plans/ 참조.

---

## 현재 위치

| 항목 | 값 |
|------|-----|
| PROJECT | {프로젝트명} |
| 현재 Phase | {Phase명} |
| 상태 | 🔲 시작 전 |
| 현재 플랜 | `.claude/plans/{플랜파일명}` |
| 전체 플랜 | `.claude/plans/value-up-master.md` |

---

## 진행 현황

> 업데이트 방식으로 기록. 체크박스 없음. 체크박스는 페이지 플랜에만.

(내용 없음 — 작업 시작 후 업데이트)

---

## 아카이브

| 파일 | 내용 |
|------|------|
| (이전 아카이브 파일명) | (이전 Phase 요약) |
```

---

## 주의사항

- 이 스킬은 **사용자 명시적 호출 시에만** 실행한다 (자동 실행 금지)
- 복수 플랜이 WORKSPACE.md에 혼재할 경우 사용자가 내용 검토 후 호출 여부 결정
- 아카이브 후 원본을 삭제하지 않음 — 새 WORKSPACE.md 작성만 제안
