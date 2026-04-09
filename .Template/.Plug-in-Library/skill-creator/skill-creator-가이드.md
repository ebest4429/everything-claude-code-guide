# Skill Creator 완전 가이드

> skill-creator 플러그인의 전체 구조, 작동 방식, 사용법을 한국어로 설명합니다.

---

## 목차

1. [개요](#개요)
2. [디렉토리 구조](#디렉토리-구조)
3. [핵심 파일 설명](#핵심-파일-설명)
4. [스킬 제작 전체 워크플로우](#스킬-제작-전체-워크플로우)
5. [스킬 파일(SKILL.md) 작성법](#스킬-파일skillmd-작성법)
6. [테스트 & 평가 시스템](#테스트--평가-시스템)
7. [에이전트 서브시스템](#에이전트-서브시스템)
8. [스크립트 레퍼런스](#스크립트-레퍼런스)
9. [JSON 스키마 참조](#json-스키마-참조)
10. [설명 최적화](#설명-최적화)
11. [환경별 주의사항](#환경별-주의사항)
12. [자주 묻는 질문 (FAQ)](#자주-묻는-질문-faq)

---

## 개요

**Skill Creator**는 Claude가 새로운 "스킬"을 만들고 반복적으로 개선할 수 있도록 도와주는 메타-스킬입니다. 스킬이란 Claude에게 특정 작업 방법을 가르치는 일종의 전문 지침서(prompt + 리소스 묶음)입니다.

### 스킬이란?

스킬은 `SKILL.md` 파일과 선택적인 보조 리소스(스크립트, 참조 문서, 에셋)로 구성됩니다. Claude는 사용자의 요청을 분석해 적합한 스킬을 자동으로 선택하고, 해당 스킬의 지침을 따라 작업을 수행합니다.

```
my-skill/
├── SKILL.md          ← 스킬의 핵심. 항상 필요.
├── scripts/          ← 반복 작업 자동화 스크립트
├── references/       ← 참조 문서 (필요 시 로드)
└── assets/           ← 템플릿, 폰트, 아이콘 등
```

### Skill Creator가 하는 일

1. 사용자의 의도를 파악하고 스킬을 설계
2. SKILL.md 초안 작성
3. 테스트 케이스 생성 및 실행
4. 결과를 정성적·정량적으로 평가
5. 피드백을 반영해 스킬 개선
6. 설명(description) 최적화로 트리거 정확도 향상
7. 완성된 스킬을 `.skill` 파일로 패키징

---

## 디렉토리 구조

```
skill-creator/
│
├── SKILL.md                      ← 메인 스킬 지침 (이 가이드의 핵심)
├── LICENSE.txt                   ← Apache 2.0 라이선스
│
├── agents/                       ← 특수 서브에이전트 지침
│   ├── grader.md                 ← 채점 에이전트: eval 결과 채점 방법
│   ├── comparator.md             ← 비교 에이전트: 블라인드 A/B 비교
│   └── analyzer.md               ← 분석 에이전트: 패턴 분석 및 개선 제안
│
├── references/
│   └── schemas.md                ← JSON 스키마 정의 (evals, grading, benchmark 등)
│
├── scripts/                      ← Python 자동화 스크립트
│   ├── __init__.py
│   ├── utils.py                  ← SKILL.md 파싱 유틸리티
│   ├── quick_validate.py         ← 스킬 유효성 빠른 검사
│   ├── package_skill.py          ← 스킬을 .skill 파일로 패키징
│   ├── aggregate_benchmark.py    ← 벤치마크 결과 집계
│   ├── run_eval.py               ← 트리거 평가 실행
│   ├── run_loop.py               ← 평가+개선 루프 실행
│   ├── improve_description.py    ← Claude로 설명 개선
│   └── generate_report.py        ← HTML 리포트 생성
│
├── eval-viewer/
│   ├── generate_review.py        ← eval 결과 뷰어 생성 스크립트
│   └── viewer.html               ← eval 뷰어 HTML 템플릿
│
└── assets/
    └── eval_review.html          ← 트리거 eval 리뷰 HTML 템플릿
```

---

## 핵심 파일 설명

### `SKILL.md` — 스킬의 두뇌

Skill Creator의 주 지침서. Claude가 스킬 제작 전체 과정을 안내받는 문서입니다. 크게 다음 섹션으로 구성됩니다:

| 섹션 | 역할 |
|------|------|
| 의도 파악 | 사용자가 원하는 것 명확화 |
| 인터뷰 & 조사 | 엣지 케이스, 형식, 의존성 파악 |
| SKILL.md 작성 | 실제 스킬 문서 초안 |
| 테스트 실행 | eval 실행 (서브에이전트 병렬 스폰) |
| 평가 | 채점, 집계, 뷰어 생성 |
| 개선 | 피드백 반영한 스킬 수정 |
| 반복 | 만족할 때까지 반복 |
| 설명 최적화 | 트리거 정확도 개선 |
| 패키징 | .skill 파일로 배포 |

---

### `agents/grader.md` — 채점 에이전트

서브에이전트로 실행됩니다. 각 eval 실행의 출력을 채점합니다.

**입력:**
- 어서션 목록 (검증할 진술들)
- 트랜스크립트 경로
- 출력 파일 디렉토리

**출력 (`grading.json`):**
- 각 어서션에 대한 PASS/FAIL + 증거
- 집계 통과율
- 실행 지표 (도구 호출 수, 오류 등)
- 타이밍 데이터
- Eval 개선 제안 (필요시)

**핵심 원칙:** 표면적 준수가 아닌 진정한 작업 완료를 검증합니다. 예를 들어 파일이 존재하더라도 내용이 비어있으면 FAIL.

---

### `agents/comparator.md` — 블라인드 비교 에이전트

두 출력을 "어느 스킬이 만들었는지 모르는 상태"로 비교합니다. 편향 없는 품질 판단을 위한 것입니다.

**평가 기준:**
- 내용 루브릭: 정확성, 완전성, 정밀도 (각 1-5점)
- 구조 루브릭: 구성, 형식, 사용성 (각 1-5점)
- 전체 점수: 두 루브릭 평균 (1-10점)

**출력 (`comparison.json`):** 승자, 추론, 루브릭 점수, 강점/약점

---

### `agents/analyzer.md` — 분석 에이전트

두 가지 역할을 합니다:

1. **블라인드 비교 후 사후 분석**: 승자가 이긴 이유, 패자 개선 방법을 구체적으로 분석
2. **벤치마크 결과 분석**: 집계 통계가 숨기는 패턴 발견 (플레이키 eval, 비차별적 어서션 등)

---

### `references/schemas.md` — JSON 스키마 정의

모든 JSON 파일의 구조를 정의합니다:

| 파일 | 위치 | 내용 |
|------|------|------|
| `evals.json` | `evals/evals.json` | 테스트 케이스 정의 |
| `grading.json` | `<run-dir>/grading.json` | 채점 결과 |
| `metrics.json` | `<run-dir>/outputs/metrics.json` | 실행 지표 |
| `timing.json` | `<run-dir>/timing.json` | 타이밍 데이터 |
| `benchmark.json` | `<iteration-dir>/benchmark.json` | 집계 벤치마크 |
| `comparison.json` | `<grading-dir>/comparison-N.json` | 블라인드 비교 결과 |
| `analysis.json` | `<grading-dir>/analysis.json` | 사후 분석 결과 |
| `history.json` | 워크스페이스 루트 | 버전 진행 기록 |

---

## 스킬 제작 전체 워크플로우

```
사용자 요청
    │
    ▼
┌─────────────────────────────┐
│  1단계: 의도 파악            │
│  - 스킬이 무엇을 해야 하나?  │
│  - 언제 트리거되어야 하나?   │
│  - 예상 출력 형식은?        │
│  - 테스트 케이스 필요한가?  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  2단계: 인터뷰 & 조사        │
│  - 엣지 케이스 질문          │
│  - 예시 파일 요청            │
│  - 의존성 확인               │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  3단계: SKILL.md 초안 작성   │
│  - name, description 정의   │
│  - 지침 작성 (이유 포함)     │
│  - 예시 패턴 포함            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  4단계: 테스트 케이스 작성   │
│  - 2~3개 현실적인 프롬프트  │
│  - evals/evals.json에 저장  │
│  - 사용자와 검토             │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────────────────────────┐
│  5단계: 병렬 실행 (같은 턴에!)                   │
│                                                  │
│  [with_skill] ←→ [without_skill (기준선)]        │
│  eval-0/              eval-0/                    │
│  eval-1/              eval-1/                    │
│  eval-2/              eval-2/                    │
│                                                  │
│  실행 중: 어서션 초안 작성                        │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────┐
│  6단계: 채점 & 집계          │
│  - grader 에이전트 실행      │
│  - aggregate_benchmark.py   │
│  - 분석가 검토               │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  7단계: eval 뷰어 생성       │ ← 반드시 여기서 사람이 먼저 검토!
│  generate_review.py 실행    │
│  (--static 옵션: Cowork용)  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  8단계: 사용자 피드백 읽기   │
│  feedback.json 확인          │
└──────────────┬──────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
만족?                  개선 필요?
    │                     │
    ▼                     ▼
설명 최적화          9단계: 스킬 개선
패키징               iteration-N+1/ 생성
                     → 5단계로 돌아감
```

---

## 스킬 파일(SKILL.md) 작성법

### 기본 구조

```markdown
---
name: my-skill-name
description: >
  이 스킬이 무엇을 하는지, 언제 사용해야 하는지 설명합니다.
  사용자가 X, Y, Z를 언급할 때 반드시 이 스킬을 사용하세요.
---

# 스킬 이름

## 개요
스킬의 목적과 작동 방식 설명.

## 단계별 지침
1. 첫 번째 단계
2. 두 번째 단계
...
```

### 프런트매터 규칙

| 필드 | 필수 | 제약 |
|------|------|------|
| `name` | ✅ | 케밥 케이스, 최대 64자, 영소문자·숫자·하이픈만 |
| `description` | ✅ | 최대 1024자, 꺾쇠괄호 불가 |
| `compatibility` | ❌ | 최대 500자 |
| `license` | ❌ | 선택적 |
| `allowed-tools` | ❌ | 선택적 |
| `metadata` | ❌ | 선택적 |

### Description 작성 팁

Description은 Claude가 스킬을 트리거할지 결정하는 **가장 중요한** 요소입니다.

**좋은 description 예시:**
```
Excel 스프레드시트 생성 및 편집 스킬. 사용자가 .xlsx 파일,
스프레드시트, 데이터 표, 예산, 수식, 차트 생성을 언급할 때
반드시 이 스킬을 사용하세요. "표로 만들어줘", "엑셀로 정리해줘",
"데이터를 시각화해줘"같은 요청에도 이 스킬이 적합합니다.
```

**나쁜 description 예시:**
```
Excel 파일을 만드는 방법.
```

**핵심 원칙:**
- 명령형으로 작성 ("사용하세요", "트리거하세요")
- 구현 세부사항보다 사용자 의도에 집중
- 다른 스킬과 차별화되도록 독특하게
- 과소 트리거를 방지하기 위해 약간 적극적으로

### 3단계 로딩 시스템 활용

```
1단계: 메타데이터 (항상 컨텍스트에)
   → name + description (~100단어)
   → Claude가 스킬 선택 시 이것만 봄

2단계: SKILL.md 본문 (스킬 트리거 시)
   → 상세 지침 (<500줄 권장)
   → 복잡한 워크플로우, 예시 패턴

3단계: 번들 리소스 (필요할 때만)
   → scripts/, references/, assets/
   → 크기 제한 없음
```

---

## 테스트 & 평가 시스템

### evals.json 구조

```json
{
  "skill_name": "내-스킬",
  "evals": [
    {
      "id": 1,
      "prompt": "사용자가 실제로 입력할 법한 프롬프트",
      "expected_output": "성공적인 결과 설명",
      "files": [],
      "expectations": [
        "출력 파일이 .xlsx 형식임",
        "A열에 날짜, B열에 금액이 있음",
        "SUM 수식이 B열 마지막에 있음"
      ]
    }
  ]
}
```

### 좋은 어서션 vs. 나쁜 어서션

| 나쁜 어서션 | 좋은 어서션 |
|------------|------------|
| "파일이 생성됨" | "파일이 .xlsx 형식이고 3개 이상의 행이 있음" |
| "출력이 있음" | "월별 합계 행에 SUM 수식이 사용됨" |
| "'John'이라는 이름 포함" | "John Smith가 주요 연락처로 전화번호 및 이메일과 함께 포함됨" |

### 워크스페이스 디렉토리 구조

```
my-skill-workspace/
├── skill-snapshot/          ← 기존 스킬 개선 시 원본 스냅샷
│
├── iteration-1/
│   ├── benchmark.json       ← 집계 결과
│   ├── benchmark.md         ← 읽기 쉬운 요약
│   │
│   ├── eval-0-form-filling/
│   │   ├── eval_metadata.json
│   │   ├── with_skill/
│   │   │   ├── outputs/     ← 스킬을 사용해 생성된 파일들
│   │   │   └── grading.json ← 채점 결과
│   │   └── without_skill/
│   │       ├── outputs/
│   │       └── grading.json
│   │
│   └── eval-1-data-extraction/
│       ├── eval_metadata.json
│       ├── with_skill/
│       └── without_skill/
│
└── iteration-2/
    └── ...
```

---

## 에이전트 서브시스템

### 그레이더 에이전트 실행 방법

```
이 작업을 수행하세요:
- agents/grader.md를 읽으세요
- expectations: ["출력이 PDF임", "이름 필드가 채워짐"]
- transcript_path: /path/to/transcript.md
- outputs_dir: /path/to/outputs/
- grading.json을 outputs_dir/../grading.json에 저장하세요
```

### 블라인드 비교 실행 방법

```
이 작업을 수행하세요:
- agents/comparator.md를 읽으세요
- output_a_path: /path/to/with_skill/outputs/
- output_b_path: /path/to/without_skill/outputs/
- eval_prompt: "원래 사용자 요청"
- expectations: ["어서션1", "어서션2"]
- comparison.json을 저장하세요
```

### 분석가 에이전트 실행 방법

```
이 작업을 수행하세요:
- agents/analyzer.md의 "Analyzing Benchmark Results" 섹션을 읽으세요
- benchmark_data_path: /path/to/benchmark.json
- skill_path: /path/to/skill/
- output_path: /path/to/notes.json
```

---

## 스크립트 레퍼런스

### `aggregate_benchmark.py` — 벤치마크 집계

```bash
# 기본 사용
python -m scripts.aggregate_benchmark <워크스페이스>/iteration-1 --skill-name my-skill

# 출력 경로 지정
python -m scripts.aggregate_benchmark <워크스페이스>/iteration-1 \
  --skill-name my-skill \
  --output /custom/path/benchmark.json
```

**생성 파일:**
- `benchmark.json`: 구조화된 집계 데이터
- `benchmark.md`: 사람이 읽을 수 있는 요약

---

### `package_skill.py` — 스킬 패키징

```bash
# 현재 디렉토리에 .skill 파일 생성
python -m scripts.package_skill /path/to/my-skill

# 특정 디렉토리에 저장
python -m scripts.package_skill /path/to/my-skill ./dist
```

**패키징 시 제외되는 것:**
- `__pycache__/`, `node_modules/`, `*.pyc`
- `.DS_Store`
- `evals/` 디렉토리 (스킬 루트에서)

---

### `quick_validate.py` — 유효성 검사

```bash
python -m scripts.quick_validate /path/to/my-skill
```

**검사 항목:**
- SKILL.md 존재 여부
- YAML 프런트매터 형식
- 필수 필드 (name, description) 존재
- name: 케밥 케이스, 64자 이내
- description: 1024자 이내, 꺾쇠괄호 없음
- 허용되지 않은 프런트매터 키 없음

---

### `run_eval.py` — 트리거 평가 실행

스킬 description이 올바르게 트리거되는지 테스트합니다.

```bash
python -m scripts.run_eval \
  --eval-set /path/to/trigger_evals.json \
  --skill-path /path/to/skill \
  --model claude-sonnet-4-6 \
  --runs-per-query 3 \
  --verbose
```

**eval set JSON 형식:**
```json
[
  {"query": "상사가 엑셀 파일 분석 부탁했어요", "should_trigger": true},
  {"query": "파이썬으로 피보나치 수열 짜줘", "should_trigger": false}
]
```

---

### `run_loop.py` — 설명 최적화 루프

```bash
python -m scripts.run_loop \
  --eval-set /path/to/trigger_evals.json \
  --skill-path /path/to/skill \
  --model claude-sonnet-4-6 \
  --max-iterations 5 \
  --holdout 0.4 \
  --verbose
```

**작동 방식:**
1. eval set을 훈련(60%)과 테스트(40%)로 분할
2. 현재 description 평가 (각 쿼리 3회 실행)
3. 실패 케이스를 Claude에게 보내 개선 요청
4. 새 description 재평가
5. 5회까지 반복
6. 테스트 점수 기준으로 최고 description 선택

**출력 JSON:**
```json
{
  "best_description": "개선된 설명 텍스트",
  "best_score": "18/20",
  "iterations_run": 4,
  "history": [...]
}
```

---

### `generate_review.py` — Eval 뷰어 생성

```bash
# 브라우저에서 서버로 열기 (Claude Code / 로컬 환경)
nohup python eval-viewer/generate_review.py \
  <workspace>/iteration-1 \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-1/benchmark.json \
  > /dev/null 2>&1 &

# 정적 HTML 파일 생성 (Cowork / 헤드리스 환경)
python eval-viewer/generate_review.py \
  <workspace>/iteration-1 \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-1/benchmark.json \
  --static /path/to/review.html

# 이전 반복과 비교
python eval-viewer/generate_review.py \
  <workspace>/iteration-2 \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-2/benchmark.json \
  --previous-workspace <workspace>/iteration-1 \
  --static /path/to/review.html
```

**뷰어에서 볼 수 있는 것:**

"출력(Outputs)" 탭:
- 프롬프트, 생성된 파일 (인라인 렌더링)
- 이전 반복 출력 (접혀 있음)
- 어서션 채점 결과 (접혀 있음)
- 피드백 텍스트박스 (자동 저장)

"벤치마크(Benchmark)" 탭:
- 통과율, 타이밍, 토큰 통계
- with_skill vs without_skill 비교
- 분석가 메모

---

## JSON 스키마 참조

### `evals.json` (테스트 케이스 정의)

```json
{
  "skill_name": "my-skill",
  "evals": [{
    "id": 1,
    "prompt": "사용자 요청",
    "expected_output": "기대 결과 설명",
    "files": ["evals/files/sample.pdf"],
    "expectations": ["어서션1", "어서션2"]
  }]
}
```

### `grading.json` (채점 결과)

```json
{
  "expectations": [{
    "text": "어서션 텍스트",
    "passed": true,
    "evidence": "구체적인 증거"
  }],
  "summary": {"passed": 3, "failed": 1, "total": 4, "pass_rate": 0.75},
  "execution_metrics": {"total_tool_calls": 15, "errors_encountered": 0},
  "timing": {"total_duration_seconds": 45.0}
}
```

### `benchmark.json` (집계 벤치마크)

핵심 필드 (뷰어가 정확한 이름을 요구함):

```json
{
  "runs": [{
    "eval_id": 1,
    "eval_name": "설명적인-이름",
    "configuration": "with_skill",   ← 반드시 이 정확한 문자열
    "run_number": 1,
    "result": {
      "pass_rate": 0.85,
      "time_seconds": 42.0,
      "tokens": 3800
    },
    "expectations": [{"text": "...", "passed": true, "evidence": "..."}]
  }],
  "run_summary": {
    "with_skill": {"pass_rate": {"mean": 0.85, "stddev": 0.05}},
    "without_skill": {"pass_rate": {"mean": 0.35, "stddev": 0.08}},
    "delta": {"pass_rate": "+0.50"}
  }
}
```

---

## 설명 최적화

스킬 완성 후 description을 최적화해 트리거 정확도를 높이는 과정입니다.

### 전체 흐름

```
1. 트리거 eval 쿼리 20개 생성
   - should_trigger: true  (8~10개)
   - should_trigger: false (8~10개)
   ↓
2. HTML 뷰어로 사용자와 쿼리 검토
   (assets/eval_review.html 사용)
   ↓
3. run_loop.py 백그라운드 실행
   - 자동으로 60/40 분할
   - 5회 반복 개선
   - 최고 점수 description 선택
   ↓
4. 결과 SKILL.md에 적용
```

### 좋은 트리거 쿼리 예시

**should_trigger: true (트리거해야 함):**
- 명시적: "Q4 판매 데이터를 엑셀로 정리해줘"
- 암묵적: "상사가 숫자들을 표로 보고 싶어하는데..."
- 구어체: "얘 xlsx인데 열이 좀 이상한거 같음"
- 엣지 케이스: "구글 시트 대신 오피스 형식으로"

**should_trigger: false (트리거하면 안 됨):**
- 유사하지만 다른: "PDF에서 표를 추출해서 분석해줘" (→ PDF 스킬)
- 맥락 없음: "데이터 분석해줘" (너무 일반적)
- 다른 도메인: "슬라이드에 차트 넣어줘" (→ PPTX 스킬)

---

## 환경별 주의사항

### Claude Code (터미널)

- 서브에이전트 사용 가능 → 병렬 실행 권장
- 브라우저 열기 가능 → eval 뷰어 서버 모드 사용
- `claude -p` 사용 가능 → 설명 최적화 가능
- 모든 기능 사용 가능

### Claude.ai (웹/모바일)

- 서브에이전트 없음 → 순차적으로 직접 실행
- 브라우저 열기 불가 → 대화에서 직접 결과 공유
- `claude -p` 없음 → 설명 최적화 건너뜀
- 정량 벤치마킹 건너뜀

### Cowork (데스크탑)

- 서브에이전트 있음 ✅ (타임아웃 시 순차 실행으로 전환)
- 브라우저/디스플레이 없음 → `--static` 옵션 사용
- 설명 최적화 가능 ✅ (`claude -p` 사용)
- 피드백 파일 수동 접근 필요

```bash
# Cowork에서 eval 뷰어 생성
python eval-viewer/generate_review.py \
  workspace/iteration-1 \
  --static /path/to/review.html   ← 이 옵션 필수!
```

---

## 자주 묻는 질문 (FAQ)

### Q: 스킬과 일반 Claude 지침의 차이는?

스킬은 **점진적 공개**와 **재사용성**이 핵심입니다. 일반 지침은 매 대화에 포함되지만, 스킬은 관련 상황에서만 로드됩니다. 또한 스크립트, 참조 문서, 에셋을 번들로 포함할 수 있어 복잡한 워크플로우를 표준화할 수 있습니다.

### Q: SKILL.md가 너무 길어지면?

500줄을 초과하면 계층 구조를 추가하세요. 상세 내용은 `references/` 파일로 이동하고, SKILL.md에서 "언제, 어떻게 이 파일을 읽어야 하는지" 명확히 안내하세요.

### Q: 어서션을 몇 개나 만들어야 하나?

테스트 케이스당 3~5개가 적당합니다. 너무 적으면 스킬의 실제 효과를 알기 어렵고, 너무 많으면 관리가 힘들어집니다. **차별화가 핵심**: "출력 파일이 존재함"처럼 스킬 없이도 통과되는 어서션은 가치가 없습니다.

### Q: 기존 스킬을 업데이트할 때 이름을 바꿔야 하나?

절대 안 됩니다. 스킬 디렉토리 이름과 SKILL.md의 `name` 필드를 그대로 유지하세요. 수정은 `/tmp/skill-name/`에 복사한 후 거기서 작업하세요 (원본이 읽기 전용일 수 있음).

### Q: 설명 최적화는 언제 해야 하나?

스킬의 기능 개발이 완료되고 사용자가 만족한 후에 하세요. 스킬이 계속 바뀌는 동안에는 최적화해도 소용없습니다.

### Q: 블라인드 비교는 언제 사용하나?

"새 버전이 정말 더 나은가?"를 객관적으로 검증하고 싶을 때입니다. 일반적인 사람 검토 루프로도 충분하므로 선택 사항입니다.

### Q: timing.json은 왜 중요한가?

서브에이전트 완료 알림에서만 얻을 수 있는 데이터입니다. 나중에 복구 불가능하므로 알림을 받는 즉시 저장해야 합니다.

### Q: `--static` 옵션과 일반 실행의 차이는?

`--static`은 로컬 웹 서버 없이 독립 실행 HTML 파일을 생성합니다. 사용자는 이 파일을 브라우저로 열어 검토하고, "모든 리뷰 제출" 버튼으로 `feedback.json`을 다운로드합니다. Cowork 같은 헤드리스 환경에서 필수입니다.

---

## 라이선스

이 스킬은 Apache License 2.0 하에 배포됩니다. 자세한 내용은 `LICENSE.txt`를 참조하세요.

---

*이 가이드는 skill-creator 플러그인의 모든 파일을 분석하여 작성된 한국어 완전 레퍼런스입니다.*
