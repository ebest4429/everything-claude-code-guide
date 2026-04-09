# WORKSPACE.md

> 세션 시작 시 읽는다.
> **기본 읽기**: 현재 위치 + 남은 과제까지.

---

## 현재 위치

| 항목 | 값 |
|------|-----|
| PROJECT | everything-claude-code (Claude Code 전체 기능 가이드 웹사이트) |
| 현재 Phase | Phase 2 — 기본 UI 구현 |
| 상태 | 🔄 진행 중 — UI 셸 완성. 항목 6(검색) + GitHub Pages 배포 남음 |
| 현재 플랜 | `.claude/plans/everything-claude-code-phase2.md` |
| 마스터플랜 | `.claude/plans/everything-claude-code-master.md` |

---

## 남은 과제

Phase 2 잔여:
- 항목 6: fuse.js 전체 콘텐츠 검색 + 하이라이팅
- GitHub Pages 배포 (`npm run deploy`)

`.Source-Files/everything-claude-code.md` 플레이스홀더 복구 완료. Phase 3 시작 전 실제 내용 채움

---

## 진행 이력

### 2026-04-10 구조 점검 및 보완

| 항목 | 내용 |
|------|------|
| 점검-연결 | scope 경로 오류 2건 수정 (HOOK_GUIDE, SKILL_GUIDE 실제 경로로 교정) |
| 점검-연결 | SKILL_GUIDE.md commands 목록 schedule → session-schedule 수정 |
| 점검-구현 | CLAUDE.md 훅 복구 경고 섹션 제거 |
| 점검-구현 | phase2.md 참고 섹션 구 복구 안내 제거 |
| 점검-구현 | master.md 결정사항 이력 복구 완료로 업데이트 |

### 2026-04-09 .claude 소실 및 복구

| 항목 | 내용 |
|------|------|
| 원인 | `npx create-vite --overwrite`가 프로젝트 루트 전체 삭제 |
| 피해 | .claude/, .Source-Files/, .Template/, .mcp.json 등 소실 |
| 보존 | src/, dist/, node_modules/, package.json 등 Vite 파일은 정상 |
| 조치 | CLAUDE.md, plans, WORKSPACE.md 핵심 파일 복구 완료 |
| 2026-04-10 복구 | project-init에서 hooks, settings.json, commands, skills, .mcp.json, .Template 등 복구 |
| 2026-04-10 수정 | CODE_DIRS, RULES.md, 점검-scope.md 프로젝트 맞게 수정 |
| 2026-04-10 git | git init + 커밋 2개 (init, fix) |

### 2026-04-09 Phase 2 UI 셸 구현

| 항목 | 내용 |
|------|------|
| 완료 | Vite + React + Tailwind 초기화, 다크테마, Pretendard, 리사이즈 사이드바 |
| 완료 | HashRouter 7개 섹션, 필터링, 아코디언·카드 컴포넌트, 스텁 페이지 |
| 빌드 | npm run build 성공, dist/ 생성 확인 |
| dev서버 | http://localhost:5173/everything-claude-code/ |
