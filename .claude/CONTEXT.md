# CONTEXT.md

## 프로젝트 정체성

**everything-claude-code 가이드 웹사이트**
Claude Code(CLI)의 전체 기능과 사용법을 다루는 가이드 웹사이트.

---

## 콘텐츠 구조 (예정)

- 개요
- 설치법 (claude cli / antigravity ide)
- 사용법
- 주요 내용 (상세)
- 메뉴별 소개 (상세)
- 기타: 전체 기능 — 스킬별, 에이전트별 상세 가이드

---

## 디자인 방향

| 항목 | 값 |
|------|----|
| 테마 | 다크 (#0f0f0f) |
| 폰트 | Pretendard (CDN) |
| 소제목 | 16~18px |
| 본문 최소 | 14px |
| 헤딩 컬러 | #ffffff |
| 강조 컬러 | #7c3aed |
| 타이틀 영역 | 90px + 검색바 |
| 네비게이션 | 사이드바 (180~420px 리사이즈) |
| 상세 영역 | 아코디언 컨테이너 |
| 레이아웃 | 카드형 / 리스트형 |

---

## 기술 환경

| 항목 | 값 |
|------|----|
| OS | Windows 10 Pro |
| Shell | bash (Git Bash) |
| 프레임워크 | Vite + React + TypeScript |
| CSS | Tailwind CSS (@tailwindcss/vite) |
| 라우팅 | react-router-dom v7 (HashRouter) |
| 검색 | fuse.js |
| 배포 | GitHub Pages (npm run deploy) |

---

## 디렉토리 구조

```
everything-claude-code/
├── .claude/          ← Claude Code 설정 (훅 복구 필요)
│   ├── plans/        ← 플랜 파일
│   └── WORKSPACE.md
├── src/
│   ├── App.tsx           ← HashRouter + 7개 라우트
│   ├── index.css         ← 다크테마 + Tailwind
│   ├── components/
│   │   ├── Layout.tsx    ← 사이드바 + 메인
│   │   ├── Sidebar.tsx   ← 네비게이션 + 필터
│   │   ├── Header.tsx    ← 타이틀 + 검색바
│   │   ├── Accordion.tsx
│   │   └── Card.tsx
│   ├── pages/            ← 7개 섹션 페이지
│   └── data/nav.ts       ← 네비게이션 데이터
├── index.html            ← Pretendard CDN 포함
├── vite.config.ts        ← base: '/everything-claude-code/'
└── package.json          ← deploy: gh-pages -d dist
```

---

## ⚠️ 복구 필요 항목

- `.claude/hooks/` — 훅 파일 전체 소실 (create-vite --overwrite)
- `settings.json` — 훅 설정 소실
- `.Source-Files/`, `.Template/` — 참조 문서 소실
- `.mcp.json`, `.agentignore`, `.claudeignore` 소실
