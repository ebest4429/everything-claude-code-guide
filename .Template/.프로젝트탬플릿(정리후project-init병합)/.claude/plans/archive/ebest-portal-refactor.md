# ebest-portal 리팩토링 플랜

> 세션마다 완료 항목 체크 후 갱신. 다음 세션은 이 파일 기준으로 시작.
> 이 플랜은 롤링 플랜 — 전체 완료 전까지 archive 이동 금지.

---

## 리팩토링 배경 (의사결정 근거)

### 실패 경험 1 — 단일 프로젝트 통합 방식
- 메인 프로젝트 하위에 개별 서비스를 추가하는 방식
- AI가 경계 규칙(강제/이중 규칙 포함) 무시하고 완성된 하위 프로젝트 코드 침범
- 프로젝트 비대화 및 복잡도 증가

### 실패 경험 2 — 개별 프로젝트 → 통합 방식
- 각 프로젝트를 독립 개발 후 ebest-portal로 통합 시도
- 양쪽 프로젝트에 UI 잔재 발생, 프로젝트별 일관성 없음
- 통합 시 혼선 및 애로사항 과다

### 채택 아키텍처 (확정)

```
ebest-portal (Vercel, 포트 4000)
    └── 모든 서비스의 프론트엔드 단일 위치
    └── 각 백엔드 API 호출만 담당
    └── 현재 2개 서비스, 최종 10~20개 서비스 확장 예정

Youtube-WebDown (포트 4005 / yt.ebest4429.com)
    └── API만 존재 — UI 없음

Image-Source-Download (포트 4010 / img.ebest4429.com)
    └── API만 존재 — UI 없음
```

---

## .claude/ 파일 구조 (확정)

```
ebest-portal/.claude/
├── CLAUDE.md       ← 프로젝트 영구 정체성 + 세션 시작 순서
├── CONTEXT.md      ← 전체 서비스 레지스트리 + 포트 현황 (확장성 기준)
├── RULES.md        ← 영구 규칙 (아키텍처 원칙, 신규 서비스 추가 표준)
├── WORKSPACE.md    ← 현재 페어링 프로젝트 + 작업 목적 (전환마다 교체)
└── plans/          ← 상세 체크리스트 (이 파일)
```

**핵심 원칙:**
- CLAUDE.md / CONTEXT.md / RULES.md = 영구 파일, 프로젝트 정체성 담당
- WORKSPACE.md = 프로젝트 전환마다 교체, 통합/수정 작업 컨텍스트 담당
- plans/ = 세부 체크리스트, 완료 후 archive 이동

---

## 작업 방식 (확정)

### 멀티루트 워크스페이스 1:1 페어링

```
1단계: ebest-portal + Youtube-WebDown     ← 현재 진행
2단계: ebest-portal + Image-Source-Download
3단계: ebest-portal + [다음 프로젝트]
```

**워크스페이스 파일 (폴더명 변경 후 기준):**
```
C:/Users/admin/Project/Project-Main/
├── ebest+youtube.code-workspace
├── ebest+image-source.code-workspace
└── ebest+[신규].code-workspace
```

---

## 결정 사항 기록

| 항목 | 결정 내용 | 상태 |
|------|-----------|------|
| 루트 폴더명 | `Main-Project` → `Project-Main` | 협의 완료, 미실행 |
| 포트 체계 | 4000번대, 프로젝트당 5단위 | 확정 |
| ebest-portal 포트 | 4000 | 확정 (미변경) |
| Youtube-WebDown 포트 | 4005 (기존 3005) | 확정 (미변경) |
| Image-Source-Download 포트 | 4010 (기존 3006) | 확정 (미변경) |
| 3000번대 | 신규 테스트 프로젝트용으로 비워둠 | 확정 |
| 서버 자동 구동 | PM2로 전환 | 확정, 적용 예정 |
| .claude/ 4파일 구조 | CLAUDE/CONTEXT/RULES + WORKSPACE.md | 확정, 적용 완료 |

### 포트 할당 현황

```
4000   ebest-portal
4005   Youtube-WebDown
4010   Image-Source-Download
4015   Real-Transaction-Price (예정)
4020   Juso-Convert (예정)
4025~  미배정
```

---

## 서버 자동 구동 방식

### 작업스케줄러 vs NSSM 비교

| 항목 | 작업스케줄러 | NSSM |
|------|-------------|------|
| 설치 | 기본 내장 | 별도 설치 |
| 등록 방식 | 프로젝트마다 스크립트 다름 | 동일 패턴 반복 |
| 일관성 | 없음 (현재 문제 원인) | 모든 프로젝트 동일 |
| 구동 시점 | 로그온 후 | 시스템 시작 시 |
| 크래시 재시작 | 설정 복잡 | 기본 지원 |

**채택: NSSM** — setup_all_services.ps1 NSSM 방식으로 전면 재작성 예정

---

## 실행 체크리스트

### Step 0: 작업 환경 구성

- [ ] 루트 폴더명 변경: `Main-Project` → `Project-Main`
  - 보류: /resume 경로 문제로 리팩토링 완료 후 진행
- [x] `ebest+youtube.code-workspace` 파일 생성 및 정상 로드 확인

---

### Step 1: .claude/ 설정 완료

- [x] ebest-portal CLAUDE.md 재작성 (프로젝트 정체성 중심)
- [x] ebest-portal CONTEXT.md 재작성 (서비스 레지스트리 + 확장성)
- [x] ebest-portal RULES.md 재작성 (신규 서비스 추가 표준 포함)
- [x] ebest-portal WORKSPACE.md 신규 생성
- [x] Youtube-WebDown CLAUDE.md 재작성
- [x] Youtube-WebDown CONTEXT.md 재작성 (영구 정보만)
- [x] Youtube-WebDown RULES.md 재작성
- [x] Youtube-WebDown plans/youtube-cleanup.md 생성
- [x] Youtube-WebDown .claude/ 불필요 폴더 제거
  - agents/ config/ context/ handoffs/ hooks/ notes/
  - plugins/ Project-Guide/ rules/ skills/ tasks/ walkthroughs/

---

### Step 2: 현재 상태 진단

- [x] ebest-portal 실제 라우팅 구조 확인
  - app/youtube/page.tsx ✓
  - app/image-source/page.tsx ✓ (이미 존재)
  - features/youtube/ ✓ (컴포넌트 3개)
  - features/image-source/ ✓ (컴포넌트 10개 + hooks 4개 + utils 3개 — 이미 구현됨)
  - dev 포트: 3000 → 4000 변경 필요
- [x] Youtube-WebDown UI 잔재 확인
  - app/page.tsx, layout.tsx, globals.css, components/ 2개 → 제거 대상
  - dev 포트: 3005 → 4005 변경 필요
- [ ] Image-Source-Download 상태 확인 → Step 4(ebest+image-source 워크스페이스)에서 진행

> **image-source 발견 사항 (Step 4에서 처리):**
> - ebest-portal 프론트는 구현 완료 상태이나 동작 불가 (백엔드 미연결)
> - 통합 과정에서 정상 동작하지 않는 부분 존재
> - 작업스케줄러 등 수정 요인 존재
> - ebest+image-source 워크스페이스 전환 시 전체 점검 예정

---

### Step 3: Youtube-WebDown 정리

> 상세 체크리스트: `Youtube-WebDown/.claude/plans/youtube-cleanup.md`

- [x] UI 잔재 제거 완료
- [x] 포트 변경 완료 (3005 → 4005)
- [x] CORS 수정 완료
- [x] 중복 프론트엔드 처리 완료
  - yt.ebest4429.com/ → ebest4429.com/youtube 리다이렉트 (next.config.ts, 308)
  - ebest4429.com/youtube-webdown → /youtube 리다이렉트 (next.config.ts, permanent)
- [x] ebest-portal → youtube 동작 검증 완료
- [x] cloudflare 터널 포트 수정 완료 (3005 → 4005)

---

### Step 4: Image-Source-Download 백엔드 복구

> WORKSPACE.md를 Image-Source-Download로 전환 후 진행

- [x] WORKSPACE.md 업데이트
- [x] ebest+image-source.code-workspace 생성
- [x] 이미지 추출 API 복구 (UI 없이) — 이미 완료 상태였음
- [x] 포트 변경 (3006 → 4010) — 이미 완료 상태였음
- [x] cloudflared 터널 설정 확인 (Cloudflare 대시보드에 img.ebest4429.com 추가 완료)
- [x] PM2 ecosystem.config.js 생성 및 등록 (NSSM → PM2로 변경)
- [x] API 엔드포인트 문서화 (scan/proxy/download)
- [x] Image-Source-Download/.claude/ 설정 적용

---

### Step 5: ebest-portal 프론트 통합

- [x] image-source 페이지 구현 (이미 구현 완료 상태였음)
- [x] 네비게이션 정리
  - Under Construction: /pptx
  - Coming Soon: /dashboard, /analysis, /market, /address, /school, /complex
- [x] 전체 링크 동작 검증 (빌드 확인 완료)

---

### Step 6: 인프라 정리 (PM2 방식)

> WORKSPACE.md에 상세 명령어 기록됨

- [x] PM2 설치 (`npm install -g pm2`)
- [x] Youtube-WebDown PM2 등록 및 저장 (ecosystem.config.js)
- [x] pm2-windows-startup 설치 및 레지스트리 등록 (부팅 자동시작)
- [x] 기존 작업스케줄러 항목 제거 (YoutubeWebDown, CloudflareTunnel)
- [x] Cloudflare Tunnel PM2 등록
- [x] setup_all_services.ps1 PM2 방식으로 재작성
- [x] Image-Source-Download PM2 등록 (Step 4 완료 후)
- [x] 재부팅 후 자동 구동 확인

---

### Step 7: 신규 서비스 추가 표준 수립

- [ ] ebest+[신규].code-workspace 템플릿 확정
- [ ] 백엔드용 .claude/ 최소 템플릿 확정 (backend-claude-snippet.md 업데이트)
- [ ] 신규 서비스 추가 전체 프로세스 문서화

---

## 세션 시작 규칙

> WORKSPACE.md 먼저 읽고 현재 페어링 프로젝트 확인.
> 이 파일의 미완료 항목 순서대로 진행.

---

## 검증

- [ ] ebest-portal → youtube 다운로드 정상 동작
- [ ] ebest-portal → 이미지 추출 정상 동작
- [ ] 중복 프론트엔드 없음 확인
- [ ] 각 백엔드 서버 재부팅 후 자동 구동 확인
- [ ] 포트 충돌 없음 확인 (4000번대)
- [ ] CONTEXT.md 서비스 레지스트리 최신 상태 확인
