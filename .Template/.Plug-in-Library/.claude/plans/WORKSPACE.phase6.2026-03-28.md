# WORKSPACE.md

> 세션 시작 시 가장 먼저 읽는다.
> 현재 위치 확인 전용. 상세 내용은 plans/ 참조.
> 업데이트 방식으로 기록. 체크박스 없음. 체크박스는 페이지 플랜에만.

---

## 현재 위치

| 항목 | 값 |
|------|-----|
| PROJECT | value-up |
| 현재 Phase | Phase 6 → Phase 7 전환 준비 |
| 상태 | Phase 6 구현 동결 — 검증은 추후 보강 플랜에서 처리 |
| 현재 플랜 | `.claude/plans/value-up-보완2.md` (이슈1→이슈2 순서 진행) |
| 전체 플랜 | `.claude/plans/value-up-master.md` |

---

## Phase 6 구현 순서

| 순서 | 항목 | 파일 |
|------|------|------|
| 1 | @media print CSS + 용지 규격 | `renderer/index.html` |
| 2 | 페이지 구분 마커 (page-break) | `renderer/index.html` |
| 3 | 인쇄 제외 항목 no-print 처리 | `renderer/index.html` |
| 4 | B3 아코디언 닫힘 인쇄 제외 | `renderer/index.html` |
| 5 | 인쇄 버튼 window.print() 연결 | `renderer/index.html` |

---

## Phase 6 협의 확정 내용 (2026-03-27)

| 항목 | 결정 |
|------|------|
| 폰트 | Pretendard — 인쇄 전 먼저 적용 (화면+인쇄 공통) |
| 인쇄 제목 | "중개매물 현황 보고서" (1페이지 상단) |
| 인쇄 푸터 | "팩토리공인중개사 사무소 010-8949-4429" |
| 인쇄 디자인 원칙 | 입력폼과 분리된 전용 레이아웃 |
| Phase 6 범위 | 기본형만 구축 — 전면 재구성은 추후 별도 플랜 |
| 1페이지 필수 | 기본정보 + 건축물 + 토지 + 매매정보 |
| 임대현황 1페이지 포함 | 결과 보고 후 결정 |
| B3 아코디언 인쇄 연동 | Phase 6 플랜에 포함 완료 |

## 보완2 진행 현황

### 2026-03-27 세션 — 협의 및 준비 작업 완료

| 항목 | 내용 |
|------|------|
| CLAUDE.md | 파일 내용 보고 원칙 추가 (파일 외 정보 덧붙이기 금지) |
| electron-rebuild | npm run build 후 better-sqlite3 바이너리 유실 → electron-rebuild로 복구 |
| 이슈3 해결 | connection.js/seed.js app.isPackaged 분기 + package.json extraResources 추가 → 빌드 정상 확인 |
| 이슈1 구현 완료 | seed.js 파싱 로직 교체 + migrate.js 재적재 처리 → 비자치구형/세종 드롭다운 정상 확인 |
| 이슈1 플랜 강화 | 4개 필드 원칙 + 비자치구형/세종 파싱 방향 확정 |
| 이슈2 플랜 강화 | 테이블 행 방식 + 최소 너비 원칙 확정 |
| 이슈2 구현 완료 | schema.sql + Repository + Service + mapper + landParcelsForm.js + index.html(CSS/HTML/script) + app.js 연동 |
| 이슈2 버그수정 완료 | pnuInput td 제거, 컬럼 너비 % 비율(최장텍스트 기준), 삭제버튼 ✕, 산여부 일반/산 |
| 비자치구 현황.md | 소스파일 추가 |

---

## 진행 현황

### 2026-03-27 Pretendard 폰트 적용 완료

| 파일 | 내용 |
|------|------|
| `renderer/fonts/pretendard.css` | 신규 — npm 설치 후 복사 (woff2) |
| `renderer/fonts/woff2/` | Pretendard 폰트 파일 9종 |
| `renderer/index.html` | Pretendard 링크, 폰트패밀리 변경, CSS 타입 스케일 변수 추가, 전체 font-size 변수 통일 |

### 2026-03-27 Phase 6 인쇄 기본형 구현 완료

| 항목 | 내용 |
|------|------|
| `renderer/index.html` | `@media print` CSS + `@page` 용지 규격 추가 |
| `renderer/index.html` | `.print-only` / `.page-break` / `.no-print` 클래스 처리 |
| `renderer/index.html` | 인쇄 헤더 "중개매물 현황 보고서" + 푸터 "팩토리공인중개사 사무소 010-8949-4429" 추가 |
| `renderer/index.html` | page-break: 임대현황 앞, 이미지 앞 (페이지 2, 페이지 3) |
| `renderer/index.html` | no-print: 컨트롤바, 주소 입력 UI(11개 form-group), rental-toolbar |
| `renderer/index.html` | B3 아코디언 — `.section.collapsed .section-body { display: none }` CSS 처리 |
| `renderer/index.html` | 인쇄 버튼 `onclick="openPreview()"` 연결 |
| `renderer/index.html` | 인쇄 미리보기 모드: `#preview-bar`, `body.print-preview` CSS, `openPreview/exitPreview/doPrint` JS |
| `renderer/index.html` | 미리보기 버그 수정: 닫기버튼 숨김 예외처리, 헤더/푸터 `#main-content` 안으로 이동 |
| `main/index.js` | Electron 메뉴바 숨김: `autoHideMenuBar: true` 추가 |

---

## 보류 중인 보완 항목

| 항목 | 내용 | 처리 시점 |
|------|------|---------|
| B8 다중 지번 지원 | 협의 완료 — 토지 섹션 행추가 방식으로 구현 예정 | Phase 6 완료 후 별도 플랜 |
| Phase 6 인쇄 보강 | 레이아웃 미세조정 + 이미지 배치 모드(미구현) + 검증 + Phase 6 플랜 전면 재검토 | 전체 플랜 완성 후 별도 보강 플랜 |

---

## 완료된 Phase 요약

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 1 | Electron + SQLite 초기화 | 완료 |
| Phase 2 | Repository + Service + IPC | 완료 |
| Phase 3 | 기본 UI (기본정보/건축물/토지/매매) | 완료 |
| 보완 B1~B7 | rental_use/property_type/도로명/입력규칙 등 | 완료 |
| Phase 4 | 임대현황 + 수익률 계산 | 완료 |
| Phase 5 | 보안정보 및 이미지 | 완료 |
| Phase 6 | 인쇄 (Pretendard + @media print + 미리보기 + 메뉴바) | 기능 완료 동결 |

---

## 보류/미완 — 전체 워크플로우 구조도 작성 계획

> 상태: 미착수 | 우선순위: 낮음 | 보관: Phase가 바뀌어도 삭제 금지, 계속 가지고 다닐 것

### 왜 만드는가

지침 파일이 너무 많아졌다 (CLAUDE.md / RULES.md / CONTEXT.md / WORKSPACE.md / 마스터플랜 / 페이지플랜 / 보완플랜 / 훅스크립트 등).
각각의 역할과 서로 어떻게 연결되는지, 언제 어떤 상황에서 무엇을 해야 하는지 **한 장에 그림으로** 볼 수 있어야 한다.
기술적인 설명이 아니라 **"지금 이 상황이면 이렇게 한다"** 흐름으로 작성한다.

### 만들 파일

`.claude/workflow-guide.md`
→ 완성 후 이미지(.png/.svg)로도 제작 예정
→ 새로운 상황 발생할 때마다 업데이트하며 완성해 나간다

### 담을 내용 (초안 목차)

---

**1. 프로젝트를 처음 시작할 때**
- 맨 처음 무엇부터 만드는가 (마스터플랜 → 설정파일 → 워크스페이스)
- 어떤 파일이 생기고 각각 무슨 역할인가
- Claude에게 처음 무엇을 시켜야 하는가

**2. 각 파일의 역할 한 줄 요약**

| 파일 | 한 줄 설명 | 언제 읽나 | 언제 수정하나 |
|------|-----------|---------|------------|
| 마스터플랜 | 전체 큰 그림. 몇 단계로 나눌지 | 단계 시작 전 | 큰 결정 바뀔 때 |
| 페이지플랜 | 지금 이 단계에서 할 일 목록 | 매번 작업 전 | 작업 전/후 |
| WORKSPACE | 지금 어디까지 왔는지 일지 | 세션 시작할 때마다 | 작업 완료 후 |
| CLAUDE.md | Claude가 지켜야 할 규칙 | Claude가 자동으로 읽음 | 규칙 바꿀 때 |
| RULES.md | 코드 작성 세부 규칙 | Claude가 자동으로 읽음 | 규칙 바꿀 때 |
| CONTEXT.md | 프로젝트 구조 설명 | Claude가 자동으로 읽음 | 구조 바뀔 때 |
| 보완플랜 | 원래 계획에 없던 추가 작업 | 보완 작업 시 | 새 항목 생길 때 |
| 훅 스크립트 | Claude가 순서 안 지키면 자동 차단 | 없음(자동 실행) | 규칙 바꿀 때 |

**3. 평소 작업 순서 (반복)**

```
① 플랜에서 다음 할 일 확인
   없으면 → 먼저 플랜에 항목 추가
② 할 일 "진행중" 표시
③ Claude에게 구현 지시
④ 결과 확인
⑤ 할 일 "완료" 표시
⑥ WORKSPACE에 한 줄 기록
⑦ 저장(커밋)
   훅이 ②⑤⑥ 안 했으면 자동 차단
```

**4. 돌발 상황별 대응**

| 상황 | 하는 일 |
|------|--------|
| 구현 중 버그 발견 | 페이지플랜에 버그수정 항목 추가 → 작업순서 ①~⑦ |
| 구현 중 설계 변경 | 페이지플랜 수정 → 필요시 마스터플랜도 수정 → 작업순서 |
| 계획에 없던 기능 추가 | 보완플랜에 항목 추가 → 작업순서 |
| 단계(Phase) 완료 | 완료 조건 확인 → WORKSPACE 업데이트 → 기존 WORKSPACE 아카이브 → 다음 단계 플랜 준비 |
| 새 세션 시작 | WORKSPACE 읽기 → 페이지플랜 읽기 → 이어서 진행 |
| 중간에 컨텍스트 날아감 | WORKSPACE 읽기 → 어디까지 했는지 확인 → 이어서 진행 |

**5. 각 파일 간 연결 관계 (그림으로 표현 예정)**

```
마스터플랜
  └─ 페이지플랜 (단계별)
       └─ 보완플랜 (돌발 추가)
            └─ WORKSPACE (진행 일지)
                 └─ 아카이브 (완료된 단계 보관)

CLAUDE.md / RULES.md / CONTEXT.md
  → Claude가 매 세션 자동으로 읽음
  → 규칙·구조 설명 (프로젝트 전체에 걸쳐 유효)

훅 스크립트 (자동 감시)
  → 구현 전: 플랜 업데이트 확인
  → 구현 후: WORKSPACE 업데이트 촉구
  → 저장 전: 순서 지켰는지 최종 검사
```

**6. 아직 정리 안 된 것들 (추후 추가 예정)**
- 프로젝트 처음 셋업할 때 파일 생성 순서 (체크리스트 형태)
- 다른 사람(또는 다른 Claude 세션)이 이어받을 때 인수인계 절차
- 플랜이 너무 커졌을 때 쪼개는 기준
- 마스터플랜의 단계 완료 조건을 언제 수정하는가

---

### 작업 지시 (나중에 할 것)

1. 위 목차 기반으로 `.claude/workflow-guide.md` 초안 작성
2. 그림으로 표현할 부분 mermaid 다이어그램으로 작성
3. 검토 후 이미지 파일로 출력

---

## 아카이브

| 파일 | 내용 |
|------|------|
| `.claude/archive/WORKSPACE.phase4.2026-03-27.md` | Phase 4 + 보완 B1~B7 완료 기록 |
| `.claude/archive/WORKSPACE.phase5.2026-03-27.md` | Phase 5 보안정보/이미지 완료 기록 |
