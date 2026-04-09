# 스킬 가이드

> 이 라이브러리의 전체 스킬 목록 및 배치 가이드.
> 새 프로젝트 시작 시 `.claude/` 폴더 복사 후 이 파일을 읽고 재사용 여부를 결정한다.

---

## ⚠️ AI 필수 준수 사항

**이 폴더의 스킬 파일은 프로젝트와 무관하게 전부 보존한다.**
프로젝트와의 연관성을 이유로 임의로 삭제하거나 비활성화하지 않는다.
스킬 제거 여부는 반드시 사용자가 이 가이드를 보고 직접 판단한다.

---

## 스킬 분류 체계

| 분류 | 배치 위치 | 호출 방식 | 설명 |
|------|----------|----------|------|
| **필수 Commands** | `commands/` | `/명령어` | 자동 실행 절대 금지 — 인자 필요 또는 부작용 위험 |
| **권장 Commands** | `commands/` | `/명령어 <인자>` | 명시적 인자 필요, 명시적 호출이 자연스러운 것 |
| **Both** | `commands/` + `skills/` | `/명령어` 또는 자동 트리거 | 양쪽 모두 유용 |
| **Pure Skills** | `skills/` | 키워드 자동 트리거 | AI가 문맥에 따라 자동 실행 |

---

## 전체 스킬 목록

### 1. 필수 Commands — /명령어 방식 필수 (자동 실행 금지)

| 스킬명 | 호출 형태 | 설명 | 전역 | 프로젝트 |
|--------|----------|------|:----:|:-------:|
| `translate-plugin` | `/translate-plugin <폴더>` | 플러그인 폴더 영문→한글 번역. 대상 폴더 지정 필수, 잘못 실행 시 파일 변조 위험 | ✅ | ✅ |
| `road-name-merge` | `/road-name-merge` | 시도별 도로명 xlsx 통합. 파일 처리 작업이라 명시적 호출 필수 | ✅ | ✅ |
| `skill-creator` | `/skill-creator` | 스킬 생성·반복 개선. 스킬 구조 변경이므로 명시적 제어 필수 | ✅ | ✅ |
| `session-schedule` | `/session-schedule` | 현재 세션 기반 예약 작업 생성. 세션 분석 후 자동 생성은 위험. bkit:schedule과 이름 충돌 방지로 변경 | ✅ | ✅ |

### 2. 권장 Commands — 명시적 인자 필요

| 스킬명 | 호출 형태 | 설명 | 전역 | 프로젝트 |
|--------|----------|------|:----:|:-------:|
| `analyze` | `/analyze <질문>` | 빠른 조회~심층 분석까지 데이터 질문 답변 | ✅ | ✅ |
| `build-dashboard` | `/build-dashboard <설명> [데이터소스]` | 차트·필터 포함 독립형 인터랙티브 HTML 대시보드 생성 | ✅ | ✅ |
| `create-viz` | `/create-viz <데이터소스> [차트유형]` | Python으로 출판 품질의 데이터 시각화 생성 | ✅ | ✅ |
| `explore-data` | `/explore-data <테이블/파일>` | 데이터셋 구조·품질·패턴 종합 프로파일링 | ✅ | ✅ |
| `validate` | `/validate <검토할 분석내용>` | 공유 전 분석 결과 QA — 방법론·정확성·편향 점검 | ✅ | ✅ |
| `write-query` | `/write-query <설명>` | 방언별 최적화 SQL 쿼리 작성 | ✅ | ✅ |

### 3. Both — 명령어 + 자동 트리거

> `.claude/commands/`와 `.claude/skills/` 양쪽에 모두 배치

| 스킬명 | 자동 트리거 조건 | 설명 | 전역 | 프로젝트 |
|--------|----------------|------|:----:|:-------:|
| `pdf` | `.pdf` 언급, PDF 작업 요청 | PDF 생성·편집·추출·병합·OCR 등 모든 PDF 작업 | ✅ Skills | ✅ |
| `docx` | `.docx`, Word 언급 | Word 문서 생성·편집·서식·이미지·차트 | ✅ Skills | ✅ |
| `pptx` | `deck`, `slides`, `.pptx` 언급 | 프레젠테이션 생성·편집·분석·변환 | ✅ Skills | ✅ |
| `xlsx` | `.xlsx`, 스프레드시트 언급 | 스프레드시트 생성·편집·수식·차트·정리 | ✅ Skills | ✅ |
| `mcp-builder` | MCP 서버, 외부 서비스 연동 언급 | Python/Node.js MCP 서버 개발 가이드 | ✅ Skills | ✅ |
| `data-context-extractor` | "데이터 컨텍스트 스킬", "웨어하우스 분석 설정" 언급 | 조직 맞춤형 데이터 분석 스킬 생성·개선 메타 스킬 | ⚠️ 선택 | ✅ |

### 4. Pure Skills — 자동 트리거 전용

| 스킬명 | 자동 트리거 키워드 | 설명 | 전역 | 프로젝트 |
|--------|-----------------|------|:----:|:-------:|
| `algorithmic-art` | 알고리즘 아트, 제너러티브 아트, p5.js, 파티클 | p5.js 기반 알고리즘 아트 생성 (철학+코드+HTML) | ❌ | ✅ |
| `brand-guidelines` | 브랜딩, 브랜드 색상, Anthropic 스타일 | Anthropic 공식 브랜드 색상·타이포그래피 적용 | ✅ | ✅ |
| `canvas-design` | 포스터, 시각 디자인, .png/.pdf 제작 요청 | 정적 시각 디자인 창작 (철학+PDF/PNG) | ❌ | ✅ |
| `cowork-plugin-customizer` | 플러그인 커스터마이징, 플러그인 설정 | Cowork 플러그인 커스터마이징 (Cowork 환경 전용) | ❌ | ✅ |
| `create-cowork-plugin` | 플러그인 생성, 플러그인 만들기 | Cowork 플러그인 신규 제작 (Cowork 환경 전용) | ❌ | ✅ |
| `data-exploration` | 데이터셋 탐색, 데이터 품질 평가, 컬럼 분포 | 데이터 프로파일링·구조 파악 방법론 참조 | ✅ | ✅ |
| `data-validation` | 분석 결과 공유 전 검증, 편향 탐지, 재현성 | 분석 배포 전 QA 체크리스트 방법론 참조 | ✅ | ✅ |
| `data-visualization` | 차트 작성, matplotlib, seaborn, plotly | 시각화 방법론·차트 유형 선택 가이드 참조 | ✅ | ✅ |
| `doc-coauthoring` | 문서 작성, 제안서, 명세서, PRD, RFC | 구조화된 문서 공동 작성 3단계 워크플로우 | ✅ | ✅ |
| `interactive-dashboard-builder` | 인터랙티브 대시보드, Chart.js, 필터 포함 | HTML/JS 대시보드 빌드 패턴·기법 참조 | ❌ | ✅ |
| `internal-comms` | 3P 업데이트, 사내 뉴스레터, 인시던트 보고서 | 사내 커뮤니케이션(현황보고·FAQ·업데이트) 작성 | ✅ | ✅ |
| `slack-gif-creator` | Slack GIF, 애니메이션 GIF 제작 요청 | Slack 최적화 GIF 제작 (이모지/메시지 규격) | ❌ | ✅ |
| `sql-queries` | SQL 작성, 쿼리 최적화, Snowflake, BigQuery | 모든 방언에서 정확·고성능 SQL 작성 참조 | ✅ | ✅ |
| `statistical-analysis` | 기술 통계, 이상값 탐지, 가설 검정, 상관관계 | 통계적 방법론·해석 가이드 참조 | ✅ | ✅ |
| `theme-factory` | 테마 적용, 색상/폰트 통일, 프레젠테이션 스타일 | 10가지 전문 테마 팔레트 적용 툴킷 | ✅ | ✅ |
| `web-artifacts-builder` | React, Tailwind, shadcn/ui, 복잡한 HTML 아티팩트 | 다중 컴포넌트 Claude 아티팩트 빌드 도구 | ✅ | ✅ |

---

## 전역 vs 프로젝트 등록 기준

| 기준 | 전역 등록 | 프로젝트만 |
|------|----------|----------|
| 어느 프로젝트에서나 쓸 수 있는가 | ✅ 전역 | — |
| 특정 환경(Cowork, Slack)에서만 동작 | — | ✅ 프로젝트 |
| 창작/예술 특화라 일반 업무 불필요 | — | ✅ 프로젝트 |
| 특정 데이터 파이프라인에만 해당 | — | ✅ 프로젝트 |

| 스킬명 | 전역 Commands | 전역 Skills | 이유 |
|--------|:------------:|:-----------:|------|
| translate-plugin | ✅ | — | 플러그인 작업 시 범용 |
| road-name-merge | ✅ | — | 한국 도로명 작업 시 범용 |
| skill-creator | ✅ | — | 모든 프로젝트에서 스킬 생성 필요 |
| schedule | ✅ | — | 예약 작업은 범용 |
| analyze | ✅ | — | 데이터 분석은 범용 |
| build-dashboard | ✅ | — | 대시보드 생성은 범용 |
| create-viz | ✅ | — | 시각화는 범용 |
| explore-data | ✅ | — | 데이터 탐색은 범용 |
| validate | ✅ | — | 분석 검증은 범용 |
| write-query | ✅ | — | SQL 작성은 범용 |
| pdf | — | ✅ | PDF는 어느 프로젝트에서나 등장 |
| docx | — | ✅ | Word 문서는 범용 |
| pptx | — | ✅ | 프레젠테이션은 범용 |
| xlsx | — | ✅ | 스프레드시트는 범용 |
| mcp-builder | — | ✅ | MCP 개발은 Claude 프로젝트에서 범용 |
| brand-guidelines | — | ✅ | 디자인 작업 시 범용 |
| doc-coauthoring | — | ✅ | 문서 작성은 범용 |
| internal-comms | — | ✅ | 사내 커뮤니케이션은 범용 |
| sql-queries | — | ✅ | SQL은 범용 |
| statistical-analysis | — | ✅ | 통계는 범용 |
| data-visualization | — | ✅ | 시각화는 범용 |
| theme-factory | — | ✅ | 테마는 범용 |
| data-exploration | — | ✅ | 데이터 탐색은 범용 |
| data-validation | — | ✅ | 데이터 검증은 범용 |
| web-artifacts-builder | — | ✅ | Claude 아티팩트 개발은 범용 |
| data-context-extractor | — | ⚠️ 선택 | 특정 데이터팀에서만 필요 |
| algorithmic-art | — | ❌ | 창작 프로젝트 전용 |
| canvas-design | — | ❌ | 창작 프로젝트 전용 |
| cowork-plugin-customizer | — | ❌ | Cowork 환경 전용 |
| create-cowork-plugin | — | ❌ | Cowork 환경 전용 |
| slack-gif-creator | — | ❌ | Slack 관련 프로젝트 전용 |
| interactive-dashboard-builder | — | ❌ | 대시보드 집중 프로젝트 전용 |
| archive-workspace | — | ❌ | WORKSPACE.md 기반 프로젝트 전용 |

---

## 현재 배치 현황

### 전역 (`~/.claude/`)

| 위치 | 등록된 스킬 |
|------|-----------|
| `commands/` | translate-plugin, road-name-merge (도로명통합 포함), skill-creator, schedule, analyze, build-dashboard, create-viz, explore-data, validate, write-query |
| `skills/` | pdf, docx, pptx, xlsx, mcp-builder, brand-guidelines, doc-coauthoring, internal-comms, sql-queries, statistical-analysis, data-visualization, theme-factory, data-exploration, data-validation, web-artifacts-builder |

### 프로젝트 (`.claude/`)

| 위치 | 등록된 스킬 |
|------|-----------|
| `commands/` | translate-plugin, road-name-merge, road-name-merge-code, 도로명통합, 도로명통합-코드, 도로명편집병합-코드, skill-creator, schedule, analyze, build-dashboard, create-viz, explore-data, validate, write-query |
| `skills/` | archive-workspace, algorithmic-art, brand-guidelines, canvas-design, cowork-plugin-customizer, create-cowork-plugin, data-context-extractor, data-exploration, data-validation, data-visualization, doc-coauthoring, docx, interactive-dashboard-builder, internal-comms, mcp-builder, pdf, pptx, slack-gif-creator, sql-queries, statistical-analysis, theme-factory, web-artifacts-builder, xlsx |

---

## 스킬 vs 훅 구분 원칙

| 구분 | 훅 | 스킬 |
|------|----|------|
| 트리거 | 자동 (도구 이벤트) | 사용자 명시적 호출 또는 키워드 자동 |
| 용도 | 규칙 강제, 알림 | 판단이 필요한 작업 |
| 가이드 | `hooks/HOOK_GUIDE.md` | `skills/SKILL_GUIDE.md` |

---

## 새 프로젝트 적용 절차

1. `.claude/` 폴더 전체를 새 프로젝트로 복사
2. 이 파일(`SKILL_GUIDE.md`)을 읽고 각 스킬 재사용 여부 검토
3. 프로젝트 성격에 맞지 않는 스킬은 `.claude/skills/`에서 제거 (소스 라이브러리는 유지)
4. 새 프로젝트에서 만든 스킬은 이 목록에 추가
5. 전역 등록이 필요한 스킬은 `~/.claude/commands/` 또는 `~/.claude/skills/`에 복사

---

## 소스 라이브러리 경로

`C:\Users\admin\Project\.Plug-in-Library\` 각 스킬 폴더 → `SKILL.md`
