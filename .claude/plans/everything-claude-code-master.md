# everything-claude-code 가이드 마스터플랜

**현재 활성 플랜:** `everything-claude-code-phase2.md`

> 이 문서는 everything-claude-code 가이드 웹사이트의 전체 방향·목표·단계를 기록한다.

---

## 프로젝트 정체성

Claude Code(CLI)의 전체 기능과 사용법을 다루는 가이드 웹사이트.
다크 테마, Pretendard 폰트, 리사이즈 가능한 사이드바, 아코디언·카드형 레이아웃을 사용한다.

---

## 전체 Phase 구조

| Phase | 이름 | 상태 |
|-------|------|------|
| Phase 1 | 기술스택 협의 + 전체 구조 설계 | ✅ 완료 |
| Phase 2 | 기본 UI 구현 (레이아웃·테마·네비게이션) | 🔄 진행 중 |
| Phase 3 | 콘텐츠 구현 (페이지별 상세 작성) | 🔲 대기 |
| Phase 4 | 검색 기능 + 완성 + 배포 | 🔲 대기 |

---

## 확정 사항

### 기술스택 (확정)

> 취지: 완전 정적 사이트, 개인용이라 SSR/SSG 불필요. GitHub Pages 배포 최적, 커스텀 레이아웃 자유도 최고.

- 프레임워크: Vite + React + TypeScript
- CSS: Tailwind CSS (@tailwindcss/vite)
- 배포: GitHub Pages
- 라우팅: HashRouter (react-router-dom v7)
- 검색: fuse.js

### 페이지 구조 (확정)

> 취지: 개인 용도. 가독성·검색 편의 우선. 2단계 단순 구조.

**사이드바:** 개요 / 설치 / 사용법 / 주요 기능 / 메뉴별 소개 ── 스킬 가이드 / 에이전트 가이드
**URL:** `/#/overview` `/#/install` `/#/usage` `/#/features` `/#/menus` `/#/skills` `/#/agents`
**레이아웃:** 아코디언 카드 방식

### 디자인 방향 (확정)

- 테마: 다크 (#0f0f0f 배경, #e5e5e5 텍스트, #7c3aed 강조)
- 폰트: Pretendard (CDN)
- 소제목: 16~18px / 본문: 14px / 헤딩: #ffffff
- 타이틀 영역: 90px + 검색바
- 사이드바: 리사이즈 가능 (180~420px, 기본 260px)

---

## 미결 항목

- [x] 기술스택 결정 → Vite + React + Tailwind CSS
- [x] 전체 페이지 구조 설계
- [x] 배포 환경 결정 → GitHub Pages
- [ ] 콘텐츠 구조 설계 (Phase 3에서 병행)
- [ ] 디자인 시스템 세부 정의 (구현 중 보완)

---

## 결정사항 이력

| 날짜 | 항목 | 결정 + 취지 |
|------|------|------------|
| 2026-04-09 | 프로젝트 초기화 | everything-claude-code로 신규 초기화. Claude Code 전체 기능 가이드 웹사이트. |
| 2026-04-09 | 기술스택 | Vite + React + Tailwind CSS. 취지: 완전 정적, 개인용, GitHub Pages 최적. |
| 2026-04-09 | 배포 환경 | GitHub Pages. 취지: 무료, Vercel 슬롯 보존. |
| 2026-04-09 | 페이지 구조 | 7개 섹션 + Hash 라우팅 + 아코디언 카드. 취지: 개인용, 가독성·검색 편의 우선. |
| 2026-04-09 | .claude 소실 및 복구 | create-vite --overwrite로 .claude/ 전체 삭제. 소스 코드(src/)는 정상 보존. 2026-04-10 전체 복구 완료. |
