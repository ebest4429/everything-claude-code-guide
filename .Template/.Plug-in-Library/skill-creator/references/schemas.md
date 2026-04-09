# JSON 스키마 (JSON Schemas)

이 문서는 skill-creator에서 사용하는 JSON 스키마를 정의합니다.

---

## evals.json

스킬의 평가(eval)를 정의합니다. 스킬 디렉토리 내 `evals/evals.json`에 위치합니다.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "사용자의 예시 프롬프트",
      "expected_output": "예상 결과 설명",
      "files": ["evals/files/sample1.pdf"],
      "expectations": [
        "출력에 X가 포함됨",
        "스킬이 스크립트 Y를 사용했음"
      ]
    }
  ]
}
```

**필드:**
- `skill_name`: 스킬의 프런트매터와 일치하는 이름
- `evals[].id`: 고유한 정수 식별자
- `evals[].prompt`: 실행할 작업
- `evals[].expected_output`: 성공에 대한 사람이 읽을 수 있는 설명
- `evals[].files`: 선택적 입력 파일 경로 목록 (스킬 루트에 대한 상대 경로)
- `evals[].expectations`: 검증 가능한 진술 목록

---

## history.json

개선 모드에서 버전 진행 상황을 추적합니다. 워크스페이스 루트에 위치합니다.

```json
{
  "started_at": "2026-01-15T10:30:00Z",
  "skill_name": "pdf",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "expectation_pass_rate": 0.65,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v1",
      "parent": "v0",
      "expectation_pass_rate": 0.75,
      "grading_result": "won",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "expectation_pass_rate": 0.85,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```

**필드:**
- `started_at`: 개선 시작 시각의 ISO 타임스탬프
- `skill_name`: 개선 중인 스킬 이름
- `current_best`: 최고 성능 버전 식별자
- `iterations[].version`: 버전 식별자 (v0, v1, ...)
- `iterations[].parent`: 이것이 파생된 부모 버전
- `iterations[].expectation_pass_rate`: 채점의 통과율
- `iterations[].grading_result`: "baseline", "won", "lost", 또는 "tie"
- `iterations[].is_current_best`: 현재 최고 버전인지 여부

---

## grading.json

그레이더 에이전트의 출력입니다. `<run-dir>/grading.json`에 위치합니다.

```json
{
  "expectations": [
    {
      "text": "출력에 'John Smith'라는 이름이 포함됨",
      "passed": true,
      "evidence": "트랜스크립트 3단계에서 발견: '추출된 이름: John Smith, Sarah Johnson'"
    },
    {
      "text": "스프레드시트의 B10 셀에 SUM 수식이 있음",
      "passed": false,
      "evidence": "스프레드시트가 생성되지 않았음. 출력은 텍스트 파일임."
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  },
  "execution_metrics": {
    "tool_calls": {
      "Read": 5,
      "Write": 2,
      "Bash": 8
    },
    "total_tool_calls": 15,
    "total_steps": 6,
    "errors_encountered": 0,
    "output_chars": 12450,
    "transcript_chars": 3200
  },
  "timing": {
    "executor_duration_seconds": 165.0,
    "grader_duration_seconds": 26.0,
    "total_duration_seconds": 191.0
  },
  "claims": [
    {
      "claim": "양식에 12개의 채울 수 있는 필드가 있다",
      "type": "factual",
      "verified": true,
      "evidence": "field_info.json에서 12개 필드 확인"
    }
  ],
  "user_notes_summary": {
    "uncertainties": ["2023년 데이터 사용, 오래됐을 수 있음"],
    "needs_review": [],
    "workarounds": ["채울 수 없는 필드에 텍스트 오버레이로 대체"]
  },
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "출력에 'John Smith'라는 이름이 포함됨",
        "reason": "환각된 문서도 통과될 수 있음"
      }
    ],
    "overall": "어서션이 존재 여부만 확인하고 정확성은 확인하지 않음."
  }
}
```

**필드:**
- `expectations[]`: 증거가 있는 채점된 어서션
- `summary`: 집계 통과/실패 수
- `execution_metrics`: 실행자의 metrics.json에서 복사한 도구 사용 및 출력 크기
- `timing`: timing.json의 벽시계 타이밍
- `claims`: 출력에서 추출하고 검증된 클레임
- `user_notes_summary`: 실행자가 표시한 이슈
- `eval_feedback`: (선택적) eval 개선 제안, 그레이더가 가치 있는 이슈를 발견할 때만

---

## metrics.json

실행자 에이전트의 출력입니다. `<run-dir>/outputs/metrics.json`에 위치합니다.

```json
{
  "tool_calls": {
    "Read": 5,
    "Write": 2,
    "Bash": 8,
    "Edit": 1,
    "Glob": 2,
    "Grep": 0
  },
  "total_tool_calls": 18,
  "total_steps": 6,
  "files_created": ["filled_form.pdf", "field_values.json"],
  "errors_encountered": 0,
  "output_chars": 12450,
  "transcript_chars": 3200
}
```

**필드:**
- `tool_calls`: 도구 유형별 수
- `total_tool_calls`: 모든 도구 호출의 합계
- `total_steps`: 주요 실행 단계 수
- `files_created`: 생성된 출력 파일 목록
- `errors_encountered`: 실행 중 오류 수
- `output_chars`: 출력 파일의 총 문자 수
- `transcript_chars`: 트랜스크립트의 문자 수

---

## timing.json

실행의 벽시계 타이밍입니다. `<run-dir>/timing.json`에 위치합니다.

**캡처 방법:** 서브에이전트 작업이 완료되면 작업 알림에 `total_tokens`와 `duration_ms`가 포함됩니다. 즉시 저장하세요 — 다른 곳에는 저장되지 않으며 나중에 복구할 수 없습니다.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "executor_start": "2026-01-15T10:30:00Z",
  "executor_end": "2026-01-15T10:32:45Z",
  "executor_duration_seconds": 165.0,
  "grader_start": "2026-01-15T10:32:46Z",
  "grader_end": "2026-01-15T10:33:12Z",
  "grader_duration_seconds": 26.0
}
```

---

## benchmark.json

벤치마크 모드의 출력입니다. `benchmarks/<timestamp>/benchmark.json`에 위치합니다.

```json
{
  "metadata": {
    "skill_name": "pdf",
    "skill_path": "/path/to/pdf",
    "executor_model": "claude-sonnet-4-20250514",
    "analyzer_model": "most-capable-model",
    "timestamp": "2026-01-15T10:30:00Z",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 3
  },

  "runs": [
    {
      "eval_id": 1,
      "eval_name": "Ocean",
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.85,
        "passed": 6,
        "failed": 1,
        "total": 7,
        "time_seconds": 42.5,
        "tokens": 3800,
        "tool_calls": 18,
        "errors": 0
      },
      "expectations": [
        {"text": "...", "passed": true, "evidence": "..."}
      ],
      "notes": [
        "2023년 데이터 사용, 오래됐을 수 있음",
        "채울 수 없는 필드에 텍스트 오버레이로 대체"
      ]
    }
  ],

  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05, "min": 0.80, "max": 0.90},
      "time_seconds": {"mean": 45.0, "stddev": 12.0, "min": 32.0, "max": 58.0},
      "tokens": {"mean": 3800, "stddev": 400, "min": 3200, "max": 4100}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.35, "stddev": 0.08, "min": 0.28, "max": 0.45},
      "time_seconds": {"mean": 32.0, "stddev": 8.0, "min": 24.0, "max": 42.0},
      "tokens": {"mean": 2100, "stddev": 300, "min": 1800, "max": 2500}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+13.0",
      "tokens": "+1700"
    }
  },

  "notes": [
    "'출력이 PDF 파일'이라는 어서션이 양쪽 구성에서 100% 통과 — 스킬 가치를 차별화하지 않을 수 있음",
    "Eval 3에서 높은 변동성 (50% ± 40%) — 플레이키이거나 모델 의존적일 수 있음",
    "스킬 없는 실행이 테이블 추출 어서션에서 일관되게 실패",
    "스킬은 평균 13초 추가 실행 시간을 요구하지만 통과율을 50% 개선"
  ]
}
```

**필드:**
- `metadata`: 벤치마크 실행에 대한 정보
  - `skill_name`: 스킬 이름
  - `timestamp`: 벤치마크가 실행된 시각
  - `evals_run`: eval 이름 또는 ID 목록
  - `runs_per_configuration`: 구성당 실행 수 (예: 3)
- `runs[]`: 개별 실행 결과
  - `eval_id`: 숫자 eval 식별자
  - `eval_name`: 사람이 읽을 수 있는 eval 이름 (뷰어에서 섹션 헤더로 사용)
  - `configuration`: 반드시 `"with_skill"` 또는 `"without_skill"`이어야 함 (뷰어가 이 정확한 문자열을 그룹화 및 색상 코딩에 사용)
  - `run_number`: 정수 실행 번호 (1, 2, 3...)
  - `result`: `pass_rate`, `passed`, `total`, `time_seconds`, `tokens`, `errors`가 포함된 중첩 객체
- `run_summary`: 구성별 통계 집계
  - `with_skill` / `without_skill`: 각각 `mean`과 `stddev` 필드를 가진 `pass_rate`, `time_seconds`, `tokens` 객체 포함
  - `delta`: `"+0.50"`, `"+13.0"`, `"+1700"` 같은 차이 문자열
- `notes`: 분석가의 자유형식 관찰

**중요:** 뷰어는 이 필드 이름을 정확히 읽습니다. `configuration` 대신 `config`를 사용하거나 `pass_rate`를 run의 `result` 아래가 아닌 최상위에 두면 뷰어에서 빈/0 값이 표시됩니다. benchmark.json을 수동으로 생성할 때 항상 이 스키마를 참조하세요.

---

## comparison.json

블라인드 비교 에이전트의 출력입니다. `<grading-dir>/comparison-N.json`에 위치합니다.

```json
{
  "winner": "A",
  "reasoning": "출력 A는 적절한 형식과 모든 필수 필드를 갖춘 완전한 솔루션을 제공합니다.",
  "rubric": {
    "A": {
      "content": {"correctness": 5, "completeness": 5, "accuracy": 4},
      "structure": {"organization": 4, "formatting": 5, "usability": 4},
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": {"correctness": 3, "completeness": 2, "accuracy": 3},
      "structure": {"organization": 3, "formatting": 2, "usability": 3},
      "content_score": 2.7,
      "structure_score": 2.7,
      "overall_score": 5.4
    }
  },
  "output_quality": {
    "A": {
      "score": 9,
      "strengths": ["완전한 솔루션", "잘 형식화됨"],
      "weaknesses": ["사소한 스타일 불일치"]
    },
    "B": {
      "score": 5,
      "strengths": ["가독성 있는 출력"],
      "weaknesses": ["날짜 필드 없음", "형식 불일치"]
    }
  },
  "expectation_results": {
    "A": {
      "passed": 4,
      "total": 5,
      "pass_rate": 0.80,
      "details": [{"text": "출력에 이름 포함", "passed": true}]
    },
    "B": {
      "passed": 3,
      "total": 5,
      "pass_rate": 0.60,
      "details": [{"text": "출력에 이름 포함", "passed": true}]
    }
  }
}
```

---

## analysis.json

사후 분석 에이전트의 출력입니다. `<grading-dir>/analysis.json`에 위치합니다.

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "승자 스킬 경로",
    "loser_skill": "패자 스킬 경로",
    "comparator_reasoning": "비교 에이전트가 승자를 선택한 이유 요약"
  },
  "winner_strengths": [
    "다중 페이지 문서 처리를 위한 명확한 단계별 지침",
    "형식 오류를 포착한 검증 스크립트 포함"
  ],
  "loser_weaknesses": [
    "'문서를 적절히 처리하세요'라는 모호한 지침이 일관성 없는 행동으로 이어짐",
    "검증 스크립트 없어 에이전트가 즉흥적으로 처리"
  ],
  "instruction_following": {
    "winner": {"score": 9, "issues": ["사소함: 선택적 로깅 단계 건너뜀"]},
    "loser": {
      "score": 6,
      "issues": [
        "스킬의 형식 템플릿을 사용하지 않음",
        "3단계를 따르는 대신 자체 접근 방식 발명"
      ]
    }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "'문서를 적절히 처리하세요'를 명시적 단계로 교체",
      "expected_impact": "일관성 없는 행동을 초래한 모호성 제거"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "스킬 읽기 → 5단계 프로세스 따르기 → 검증 스크립트 사용",
    "loser_execution_pattern": "스킬 읽기 → 접근 방식 불명확 → 3가지 방법 시도"
  }
}
```
