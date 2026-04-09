# Phase 2 — 기본 UI 구현 (레이아웃·테마·네비게이션)

> 참조: `.claude/plans/everything-claude-code-master.md`
> **이 Phase의 목표:** 동작하는 UI 셸 완성. 콘텐츠는 Phase 3에서 채운다.

---

## 작업 항목

### 1. 프로젝트 초기화

- ✅ Vite + React + TypeScript 프로젝트 생성
- ✅ Tailwind CSS 설치 및 설정 (@tailwindcss/vite)
- ✅ react-router-dom 설치 (HashRouter)
- ✅ GitHub Pages 배포 설정 (base: '/everything-claude-code/' + gh-pages + deploy script)

### 2. 기본 레이아웃

- ✅ 전체 레이아웃 구조 (사이드바 + 메인 영역)
- ✅ 리사이즈 가능한 사이드바 (drag handle, min 180 / max 420)
- ✅ 상단 타이틀 영역 (90px) + 검색바
- ✅ 다크 테마 (#0f0f0f 배경, #e5e5e5 텍스트, #2a2a2a 경계선)

### 3. 폰트·타이포그래피

- ✅ Pretendard 폰트 적용 (CDN via index.html)
- ✅ 기본 타이포그래피 (소제목 16~18px / 본문 14px / #ffffff 헤딩)

### 4. 사이드바 네비게이션

- ✅ 7개 섹션 메뉴 목록 렌더링
- ✅ 구분선 (메인 섹션 / 상세 가이드)
- ✅ 필터링 기능 (검색 입력 → 사이드바 메뉴 필터)
- ✅ Hash 라우터 연동

### 5. 메인 영역 기본 컴포넌트

- ✅ 아코디언 컴포넌트
- ✅ 카드 컴포넌트
- ✅ 각 섹션 페이지 라우팅 연결 (스텁 페이지 7개)

### 6. 검색 기능

- 🔲 전체 콘텐츠 검색 (fuse.js)
- 🔲 검색 결과 하이라이팅

---

## 완료 조건

- [x] `npm run dev` 로컬 동작 확인
- [x] 사이드바 리사이즈 동작
- [x] 필터링 동작
- [x] 7개 섹션 라우팅 동작
- [x] `npm run build` → `dist/` 생성 확인
- [ ] GitHub Pages 배포 확인

---

## 참고

- 콘텐츠(텍스트 내용)는 Phase 3에서 채움
