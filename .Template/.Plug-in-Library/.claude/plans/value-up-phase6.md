# value-up Phase 6 — 인쇄

**참조 문서**
- 인쇄 명세: `.Source-Files/06-print-spec.md`

---

## 목표

Pretendard 폰트 적용 + A4 인쇄 기본형 구현
인쇄 전용 디자인(입력폼과 분리), 추후 전면 재구성 예정

---

## 현재 상태 (Phase 6 진입 시점)

| 항목 | 상태 |
|------|------|
| `no-print` 클래스 — 보안정보 섹션 | ✅ Phase 5 적용 완료 |
| `no-print` 클래스 — 이미지 추가/삭제 버튼 | ✅ Phase 5 적용 완료 |
| Pretendard 폰트 | ❌ 미적용 |
| `@media print` CSS 규칙 | ❌ 미구현 |
| 인쇄 헤더/푸터 | ❌ 미구현 |
| 페이지 구분 (`page-break`) | ❌ 미구현 |
| B3 아코디언 닫힘 → 인쇄 제외 | ❌ 보류 → Phase 6 통합 |

---

## 작업 순서 원칙

**Pretendard 먼저** — 폰트 변경 후 인쇄 레이아웃 작업해야 간격/줄바꿈 재수정 없음

---

## 0. Pretendard 폰트 적용 (화면 + 인쇄 공통)

- [x] `npm install pretendard` 설치
- [x] `node_modules/pretendard/dist/web/static/` → `renderer/fonts/` 복사 (woff2만)
- [x] `renderer/index.html` `<head>` 에 `<link rel="stylesheet" href="fonts/pretendard.css">` 추가
- [x] `body` 기본 폰트: `'Pretendard', 'Segoe UI', sans-serif` (맑은 고딕 제거)
- [x] CSS 타입 스케일 변수 추가 (--font-xs/sm/md/lg/xl)
- [x] 전체 하드코딩 font-size → CSS 변수로 통일
- [x] 섹션 헤더 — SemiBold(600), var(--font-lg: 15px)
- [x] 테이블 헤더 — Medium(500)
- [x] 강조값(ROI) — var(--font-xl: 17px)
- [ ] 인쇄 시 폰트 동일 적용 확인 (인쇄 CSS 구현 후)

---

## 1. index.html 수정 — 인쇄 전용

### 1.1 인쇄 헤더/푸터

- [x] 화면에서는 숨김, 인쇄 시만 표시 (`print-only` 클래스)
- [x] 헤더: "중개매물 현황 보고서" (1페이지 상단)
  ```html
  <div class="print-header print-only">중개매물 현황 보고서</div>
  ```
- [x] 푸터: "팩토리공인중개사 사무소 010-8949-4429" (각 페이지 하단 또는 마지막 페이지)
  ```html
  <div class="print-footer print-only">팩토리공인중개사 사무소 010-8949-4429</div>
  ```

### 1.2 `@media print` CSS 추가

- [x] 기본 규칙
  ```css
  @media print {
    .no-print { display: none !important; }
    .print-only { display: block !important; }
    input, select, textarea {
      border: none !important;
      background: transparent !important;
      -webkit-appearance: none;
    }
    button { display: none !important; }
  }
  ```
- [x] 용지: A4 세로, 여백 10~12mm
  ```css
  @page { size: A4 portrait; margin: 10mm 12mm; }
  @media print { body { font-size: 10pt; } }
  ```
- [x] 표 행 찢김 방지
  ```css
  @media print { tr { break-inside: avoid; } }
  ```
- [x] 인쇄 전용 레이아웃 (입력폼 UI와 분리)
  - 섹션 헤더 배경/테두리 단순화
  - 입력 필드 → 텍스트처럼 보이게 처리

### 1.3 페이지 구분 마커

- [x] 임대현황 섹션 앞 `<div class="page-break"></div>`
- [x] 이미지 섹션 앞 `<div class="page-break"></div>`
- [x] `.page-break` CSS
  ```css
  .page-break { display: none; }
  @media print { .page-break { page-break-before: always; break-before: page; display: block; } }
  ```

### 1.4 인쇄 제외 항목 처리

- [x] 상단 컨트롤 바 → `no-print`
- [x] 아코디언 토글 버튼 → `no-print` (`::before` CSS 처리)
- [x] 주소 입력 드롭다운 행 (시도/시군구/읍면동/리/산여부/본번/부번/PNU) → `no-print`
- [x] 임대현황 행추가/삭제 버튼 → `no-print` (rental-toolbar)

### 1.5 B3 아코디언 인쇄 연동

- [x] 닫힌 섹션 → 인쇄 제외
  ```css
  @media print {
    .section.collapsed .section-body { display: none !important; }
  }
  ```

---

## 2. 인쇄 레이아웃 검증

### 1페이지 확인
- [ ] "중개매물 현황 보고서" 헤더 표시
- [ ] 기본정보 (매물번호, 주소, 도로명주소)
- [ ] 건축물정보 표
- [ ] 토지이용정보 표
- [ ] 매매정보 및 수익률 표
- [ ] 주소 입력 드롭다운 UI 숨김
- [ ] 상단 버튼 바 숨김

### 이후 페이지 (결과 보고 후 보완)
- [ ] 임대현황 — 1페이지 내 포함 여부 결과 보고 후 결정
- [ ] 이미지 페이지
- [ ] 푸터 위치 확정

### 보안정보
- [ ] 인쇄 시 보안정보 섹션 전체 미출력 확인

---

## 3. 인쇄 버튼 연결

- [x] 상단 컨트롤 바 `인쇄` 버튼 → `window.print()` 호출
- [x] 저장되지 않은 변경사항 시 경고 토스트 — 기본형에서는 `window.print()` 직결 (경고 없이 허용)

## 4. 인쇄 미리보기

- [x] `인쇄` 버튼 → `window.print()` 직결 대신 `openPreview()` 호출로 변경
- [x] 미리보기 전용 상단 바 (`#preview-bar`) 추가 — "인쇄" / "닫기" 버튼 포함
- [x] `body.print-preview` 클래스로 화면에서 인쇄 스타일 시뮬레이션
  - `.no-print` 숨김, `.print-only` 표시, 입력필드 텍스트화, 버튼 숨김
  - A4 너비(794px) 흰 배경 카드로 미리보기
  - `.page-break` → 점선 + "페이지 구분" 라벨로 시각화
- [x] 미리보기에서 "인쇄" → `window.print()` 호출
- [x] 미리보기에서 "닫기" → 원래 화면 복원
- [x] `#preview-bar` → `@media print`에서 제외

## 5. 미리보기 버그 수정 (검증 중 발견)

- [x] 닫기 버튼 숨김 — `body.print-preview button { display:none }` 이 preview-bar 버튼도 숨기는 문제
  - `#preview-bar .preview-btn-print/close { display: inline-block !important }` 예외 추가
- [x] 인쇄 헤더/푸터 A4 카드 외부(좌측) 표시 — `print-header`/`print-footer`가 `#main-content` 밖에 있던 문제
  - 두 요소를 `#main-content` 안(첫/마지막 자식)으로 이동
- [x] Electron 메뉴바(File/Edit/View 등) 항상 표시 — `main/index.js` BrowserWindow에 `autoHideMenuBar: true` 추가

---

## 완료 조건

- [ ] Pretendard 폰트 화면 적용 확인
- [ ] A4 1페이지 (기본정보~매매정보) 정상 출력
- [ ] 인쇄 헤더/푸터 표시 확인
- [ ] 보안정보/버튼/컨트롤 인쇄 제외 확인
- [ ] 닫힌 아코디언 섹션 인쇄 제외 확인 (B3)
- [ ] 표 행 페이지 중간 찢김 없음

---

## 생성/수정 파일 목록

```
renderer/
└── index.html    (수정 — Pretendard 폰트 + @media print CSS + 헤더/푸터 + page-break)
```

---

## 설계 결정사항

| 항목 | 결정 | 이유 |
|------|------|------|
| 폰트 적용 순서 | 인쇄 CSS보다 먼저 | 폰트 후적용 시 인쇄 간격/줄바꿈 전체 재수정 필요 |
| Pretendard 로드 방식 | 로컬 파일 권장 (CDN 대안) | Electron 로컬 앱, 인터넷 미보장 |
| print.css 별도 파일 여부 | index.html 내 `<style>` 통합 | 단일 파일 구조 |
| 인쇄 디자인 | 입력폼과 분리된 전용 레이아웃 | 필드 너비/높이가 인쇄용과 불일치 |
| Phase 6 범위 | 기본형만 구축 | 추후 전면 재구성 별도 플랜 예정 |
| 임대현황 페이지 배치 | 결과 보고 후 결정 | 1페이지 내 포함 가능 여부 실측 필요 |
| 푸터 내용 | 팩토리공인중개사 사무소 010-8949-4429 | 협의 확정 |
| PDF 저장 | 미구현 (Phase 8 이후 선택) | 초기 Phase는 브라우저 인쇄 우선 |
