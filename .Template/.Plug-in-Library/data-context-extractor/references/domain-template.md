# 도메인 참조 파일 템플릿

특정 데이터 도메인(예: 매출, 사용자, 마케팅)의 참조 파일을 생성할 때 이 템플릿을 사용하세요.

---

```markdown
# [DOMAIN_NAME] 테이블

이 문서는 [domain] 관련 테이블, 지표 및 쿼리 패턴을 포함합니다.

---

## 빠른 참조

### 비즈니스 컨텍스트

[이 도메인이 다루는 내용과 핵심 개념을 2~3문장으로 설명]

### 엔티티 명확화

**"[AMBIGUOUS_TERM]"의 의미:**
- **[MEANING_1]**: [DEFINITION] ([TABLE]: [ID_FIELD])
- **[MEANING_2]**: [DEFINITION] ([TABLE]: [ID_FIELD])

쿼리 전에 어느 것을 의미하는지 항상 명확히 하세요.

### 표준 필터

[domain] 쿼리 시 항상 적용:
```sql
WHERE [STANDARD_FILTER_1]
  AND [STANDARD_FILTER_2]
```

---

## 주요 테이블

### [TABLE_1_NAME]
**위치**: `[project.dataset.table]` 또는 `[schema.table]`
**설명**: [이 테이블에 포함된 내용, 사용 시점]
**기본 키**: [COLUMN(S)]
**갱신 주기**: [일별/시간별/실시간] ([LAG] 지연)
**파티션 기준**: [PARTITION_COLUMN] (해당하는 경우)

| 컬럼 | 유형 | 설명 | 비고 |
|------|------|------|------|
| **[column_1]** | [TYPE] | [DESCRIPTION] | [GOTCHA_OR_CONTEXT] |
| **[column_2]** | [TYPE] | [DESCRIPTION] | |
| **[column_3]** | [TYPE] | [DESCRIPTION] | Nullable |

**관계**:
- `[OTHER_TABLE]`과 `[JOIN_KEY]`로 조인
- `[FOREIGN_KEY]`를 통해 `[CHILD_TABLE]`의 부모

**중첩/구조체 필드** (해당하는 경우):
- `[struct_name].[field_1]`: [DESCRIPTION]
- `[struct_name].[field_2]`: [DESCRIPTION]

---

### [TABLE_2_NAME]
[위 형식 반복]

---

## 주요 지표

| 지표 | 정의 | 테이블 | 공식 | 비고 |
|------|------|--------|------|------|
| [METRIC_1] | [DEFINITION] | [TABLE] | `[FORMULA]` | [CAVEATS] |
| [METRIC_2] | [DEFINITION] | [TABLE] | `[FORMULA]` | |

---

## 샘플 쿼리

### [QUERY_PURPOSE_1]
```sql
-- [이 쿼리가 하는 일에 대한 간단한 설명]
SELECT
    [columns]
FROM [table]
WHERE [standard_filters]
GROUP BY [grouping]
ORDER BY [ordering]
```

### [QUERY_PURPOSE_2]
```sql
[ANOTHER_COMMON_QUERY]
```

### [QUERY_PURPOSE_3]: [더 복잡한 패턴]
```sql
WITH [cte_name] AS (
    [CTE_LOGIC]
)
SELECT
    [final_columns]
FROM [cte_name]
[joins_and_filters]
```

---

## 흔한 함정

1. **[GOTCHA_1]**: [EXPLANATION]
   - 잘못된 예: `[INCORRECT_APPROACH]`
   - 올바른 예: `[CORRECT_APPROACH]`

2. **[GOTCHA_2]**: [EXPLANATION]

---

## 관련 대시보드 (해당하는 경우)

| 대시보드 | 링크 | 용도 |
|----------|------|------|
| [DASHBOARD_1] | [URL] | [DESCRIPTION] |
| [DASHBOARD_2] | [URL] | [DESCRIPTION] |
```

---

## 도메인 파일 작성 팁

1. **가장 자주 쿼리되는 테이블부터 시작** — 모든 것을 문서화하려 하지 말 것
2. **중요한 컬럼에만 컬럼 수준 상세 정보 포함** — `created_at` 같은 명확한 것은 생략
3. **추상적 설명보다 실제 쿼리 예시** — 설명하지 말고 보여줄 것
4. **함정을 눈에 띄게 문서화** — 가장 시간을 아껴주는 부분
5. **샘플 쿼리는 실행 가능하게** — 실제 테이블/컬럼명 사용
6. **중첩/구조체 필드를 명시적으로 기재** — 사람들이 많이 실수하는 부분

## 추천 도메인 파일

일반적으로 문서화할 도메인 (각각 별도 파일로 생성):

- `revenue.md` — 청구, 구독, ARR, 거래
- `users.md` — 계정, 인증, 사용자 속성
- `product.md` — 기능 사용, 이벤트, 세션
- `growth.md` — DAU/WAU/MAU, 리텐션, 활성화
- `sales.md` — CRM, 파이프라인, 기회
- `marketing.md` — 캠페인, 어트리뷰션, 리드
- `support.md` — 티켓, CSAT, 응답 시간
