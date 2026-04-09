# SQL 방언 참조

사용자의 데이터 웨어하우스에 따라 생성된 스킬에 적절한 섹션을 포함하세요.

---

## BigQuery

```markdown
## SQL 방언: BigQuery

- **테이블 참조**: 백틱 사용: \`project.dataset.table\`
- **안전한 나눗셈**: `SAFE_DIVIDE(a, b)` — 오류 대신 NULL 반환
- **날짜 함수**:
  - `DATE_TRUNC(date_col, MONTH)`
  - `DATE_SUB(date_col, INTERVAL 1 DAY)`
  - `DATE_DIFF(end_date, start_date, DAY)`
- **컬럼 제외**: `SELECT * EXCEPT(column_to_exclude)`
- **배열**: `UNNEST(array_column)` — 평탄화
- **구조체**: 점 표기법으로 접근 `struct_col.field_name`
- **타임스탬프**: `TIMESTAMP_TRUNC()`, 기본적으로 UTC
- **문자열 매칭**: `LIKE`, `REGEXP_CONTAINS(col, r'pattern')`
- **집계의 NULL**: 대부분의 함수는 NULL 무시; `IFNULL()` 또는 `COALESCE()` 사용
```

---

## Snowflake

```markdown
## SQL 방언: Snowflake

- **테이블 참조**: `DATABASE.SCHEMA.TABLE` 또는 대소문자 구분 시 따옴표 사용: `"Column_Name"`
- **안전한 나눗셈**: `DIV0(a, b)` — 0 반환, `DIV0NULL(a, b)` — NULL 반환
- **날짜 함수**:
  - `DATE_TRUNC('MONTH', date_col)`
  - `DATEADD(DAY, -1, date_col)`
  - `DATEDIFF(DAY, start_date, end_date)`
- **컬럼 제외**: `SELECT * EXCLUDE (column_to_exclude)`
- **배열**: `FLATTEN(array_column)` — 평탄화, `value`로 접근
- **Variants/JSON**: 콜론 표기법으로 접근 `variant_col:field_name`
- **타임스탬프**: `TIMESTAMP_NTZ` (타임존 없음), `TIMESTAMP_TZ` (타임존 포함)
- **문자열 매칭**: `LIKE`, `REGEXP_LIKE(col, 'pattern')`
- **대소문자 구분**: 식별자는 기본적으로 대문자; 따옴표 없이는 대문자로 처리
```

---

## PostgreSQL / Redshift

```markdown
## SQL 방언: PostgreSQL/Redshift

- **테이블 참조**: `schema.table` (소문자 관례)
- **안전한 나눗셈**: `NULLIF(b, 0)` 패턴: `a / NULLIF(b, 0)`
- **날짜 함수**:
  - `DATE_TRUNC('month', date_col)`
  - `date_col - INTERVAL '1 day'`
  - `DATE_PART('day', end_date - start_date)`
- **컬럼 선택**: EXCEPT 없음; 컬럼을 명시적으로 나열해야 함
- **배열**: `UNNEST(array_column)` (PostgreSQL), Redshift에서는 제한적
- **JSON**: 텍스트는 `json_col->>'field_name'`, JSON은 `json_col->'field_name'`
- **타임스탬프**: 타임존 변환 시 `AT TIME ZONE 'UTC'`
- **문자열 매칭**: `LIKE`, 정규식은 `col ~ 'pattern'`
- **불리언**: 네이티브 BOOLEAN 타입; `TRUE`/`FALSE` 사용
```

---

## Databricks / Spark SQL

```markdown
## SQL 방언: Databricks/Spark SQL

- **테이블 참조**: `catalog.schema.table` (Unity Catalog) 또는 `schema.table`
- **안전한 나눗셈**: `NULLIF` 사용: `a / NULLIF(b, 0)` 또는 `TRY_DIVIDE(a, b)`
- **날짜 함수**:
  - `DATE_TRUNC('MONTH', date_col)`
  - `DATE_SUB(date_col, 1)`
  - `DATEDIFF(end_date, start_date)`
- **컬럼 제외**: `SELECT * EXCEPT (column_to_exclude)` (Databricks SQL)
- **배열**: `EXPLODE(array_column)` — 평탄화
- **구조체**: 점 표기법으로 접근 `struct_col.field_name`
- **JSON**: `json_col:field_name` 또는 `GET_JSON_OBJECT()`
- **문자열 매칭**: `LIKE`, 정규식은 `RLIKE`
- **Delta 기능**: `DESCRIBE HISTORY`, `VERSION AS OF`로 타임 트래블
```

---

## MySQL

```markdown
## SQL 방언: MySQL

- **테이블 참조**: 백틱 사용 \`database\`.\`table\`
- **안전한 나눗셈**: 수동 처리: `IF(b = 0, NULL, a / b)` 또는 `a / NULLIF(b, 0)`
- **날짜 함수**:
  - `DATE_FORMAT(date_col, '%Y-%m-01')` — 날짜 잘라내기
  - `DATE_SUB(date_col, INTERVAL 1 DAY)`
  - `DATEDIFF(end_date, start_date)`
- **컬럼 선택**: EXCEPT 없음; 컬럼을 명시적으로 나열해야 함
- **배열**: 네이티브 지원 제한; 주로 JSON으로 저장
- **JSON**: `JSON_EXTRACT(col, '$.field')` 또는 `col->>'$.field'`
- **타임스탬프**: 타임존 변환 시 `CONVERT_TZ()`
- **문자열 매칭**: `LIKE`, 정규식은 `REGEXP`
- **대소문자 구분**: 테이블명은 Linux에서 대소문자 구분, Windows에서는 구분 없음
```

---

## 방언 간 공통 패턴

| 연산 | BigQuery | Snowflake | PostgreSQL | Databricks |
|------|----------|-----------|------------|------------|
| 현재 날짜 | `CURRENT_DATE()` | `CURRENT_DATE()` | `CURRENT_DATE` | `CURRENT_DATE()` |
| 현재 타임스탬프 | `CURRENT_TIMESTAMP()` | `CURRENT_TIMESTAMP()` | `NOW()` | `CURRENT_TIMESTAMP()` |
| 문자열 연결 | `CONCAT()` 또는 `\|\|` | `CONCAT()` 또는 `\|\|` | `CONCAT()` 또는 `\|\|` | `CONCAT()` 또는 `\|\|` |
| Coalesce | `COALESCE()` | `COALESCE()` | `COALESCE()` | `COALESCE()` |
| Case when | `CASE WHEN` | `CASE WHEN` | `CASE WHEN` | `CASE WHEN` |
| 고유값 카운트 | `COUNT(DISTINCT x)` | `COUNT(DISTINCT x)` | `COUNT(DISTINCT x)` | `COUNT(DISTINCT x)` |
