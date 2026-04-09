# 생성된 스킬 템플릿

새로운 데이터 분석 스킬을 생성할 때 이 템플릿을 사용하세요. 모든 `[PLACEHOLDER]` 값을 교체해야 합니다.

---

```markdown
---
name: [company]-data-analyst
description: "[COMPANY] 데이터 분석 스킬. [WAREHOUSE_TYPE] 쿼리를 위한 컨텍스트를 제공합니다. 엔티티 정의, 지표 계산식, 일반 쿼리 패턴 포함. [COMPANY] 데이터 분석 시 사용: (1) [PRIMARY_USE_CASE_1], (2) [PRIMARY_USE_CASE_2], (3) [PRIMARY_USE_CASE_3], 또는 [COMPANY] 특정 컨텍스트가 필요한 데이터 질문."
---

# [COMPANY] 데이터 분석

## SQL 방언: [WAREHOUSE_TYPE]

[sql-dialects.md에서 적절한 방언 섹션 삽입]

---

## 엔티티 명확화

사용자가 이 용어를 언급할 때 어떤 엔티티를 의미하는지 명확히 합니다:

[발견 내용에 따라 커스터마이징하는 예시 형식:]

**"사용자"의 의미:**
- **계정**: 개별 로그인/프로필 ([PRIMARY_TABLE]: [ID_FIELD])
- **조직**: 여러 계정을 보유할 수 있는 청구 엔티티 ([ORG_TABLE]: [ORG_ID])
- **[OTHER_TYPE]**: [DEFINITION] ([TABLE]: [ID])

**관계:**
- [ENTITY_1] → [ENTITY_2]: [RELATIONSHIP_TYPE] ([JOIN_KEY]로 조인)

---

## 비즈니스 용어

| 용어 | 정의 | 비고 |
|------|------|------|
| [TERM_1] | [DEFINITION] | [CONTEXT/GOTCHA] |
| [TERM_2] | [DEFINITION] | [CONTEXT/GOTCHA] |
| [ACRONYM] | [FULL_NAME] - [EXPLANATION] | |

---

## 표준 필터

명시적으로 다르게 지시받지 않는 한 항상 이 필터를 적용합니다:

```sql
-- 테스트/내부 데이터 제외
WHERE [TEST_FLAG_COLUMN] = FALSE
  AND [INTERNAL_FLAG_COLUMN] = FALSE

-- 유효하지 않은/사기 데이터 제외
  AND [STATUS_COLUMN] != '[EXCLUDED_STATUS]'

-- [기타 표준 제외 항목]
```

**재정의 시점:**
- [SCENARIO_1]: [CONDITION]인 경우 [NORMALLY_EXCLUDED] 포함

---

## 핵심 지표

### [METRIC_1_NAME]
- **정의**: [평이한 언어로 설명]
- **공식**: `[EXACT_CALCULATION]`
- **소스**: `[TABLE_NAME].[COLUMN_NAME]`
- **시간 단위**: [일별/주별/월별]
- **주의사항**: [엣지 케이스 또는 함정]

### [METRIC_2_NAME]
[위 형식 반복]

---

## 데이터 최신성

| 테이블 | 갱신 주기 | 일반 지연 |
|--------|-----------|-----------|
| [TABLE_1] | [FREQUENCY] | [LAG] |
| [TABLE_2] | [FREQUENCY] | [LAG] |

데이터 최신성 확인:
```sql
SELECT MAX([DATE_COLUMN]) as latest_data FROM [TABLE]
```

---

## 지식 베이스 탐색

상세 테이블 문서는 다음 참조 파일을 사용하세요:

| 도메인 | 참조 파일 | 용도 |
|--------|-----------|------|
| [DOMAIN_1] | `references/[domain1].md` | [BRIEF_DESCRIPTION] |
| [DOMAIN_2] | `references/[domain2].md` | [BRIEF_DESCRIPTION] |
| 엔티티 | `references/entities.md` | 엔티티 정의 및 관계 |
| 지표 | `references/metrics.md` | KPI 계산식 및 공식 |

---

## 일반 쿼리 패턴

### [PATTERN_1_NAME]
```sql
[SAMPLE_QUERY]
```

### [PATTERN_2_NAME]
```sql
[SAMPLE_QUERY]
```

---

## 문제 해결

### 흔한 실수
- **[MISTAKE_1]**: [EXPLANATION] → [CORRECT_APPROACH]
- **[MISTAKE_2]**: [EXPLANATION] → [CORRECT_APPROACH]

### 접근 권한 문제
- `[TABLE]`에서 권한 오류가 발생하는 경우: [WORKAROUND]
- PII 제한 컬럼의 경우: [ALTERNATIVE_APPROACH]

### 성능 팁
- `[PARTITION_COLUMN]` 기준으로 먼저 필터링하여 스캔 데이터 감소
- 대형 테이블은 탐색 시 `LIMIT` 사용
- 가능하면 `[RAW_TABLE]` 대신 `[AGGREGATED_TABLE]` 사용
```

---

## 커스터마이징 참고사항

스킬 생성 시:

1. **모든 플레이스홀더 채우기** — `[PLACEHOLDER]` 텍스트를 남기지 말 것
2. **사용하지 않는 섹션 제거** — 대시보드가 없으면 해당 섹션 제거
3. **구체성 추가** — 일반적인 조언보다 특정 컬럼명과 값이 더 유용
4. **실제 예시 포함** — 샘플 쿼리는 실제 테이블/컬럼명 사용
5. **훑어보기 쉽게** — 표와 코드 블록을 충분히 활용
