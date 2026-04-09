# MCP Builder 스킬 사용가이드

> 이 가이드는 `mcp-builder` 스킬을 처음 사용하는 분들을 위한 실전 안내서입니다.
> 원본 문서의 번역은 각 파일을 참조하세요.

---

## 이 스킬은 언제 쓰나요?

다음 상황에서 이 스킬을 사용하세요:

- 외부 API(Slack, GitHub, Jira 등)를 Claude가 도구로 사용할 수 있게 연결하고 싶을 때
- MCP 서버를 처음 만들어보는데 구조와 패턴을 잡고 싶을 때
- 기존 MCP 서버의 품질을 높이고 싶을 때
- MCP 서버가 실제로 잘 동작하는지 평가하고 싶을 때

---

## 전체 흐름 한눈에 보기

```
1단계 [연구/계획]
  └─ MCP 프로토콜 이해 → API 분석 → 도구 목록 작성
        ↓
2단계 [구현]
  └─ 프로젝트 구조 → 공통 인프라 → 도구 하나씩 구현
        ↓
3단계 [검토/테스트]
  └─ 코드 품질 검토 → 빌드 확인 → Inspector로 테스트
        ↓
4단계 [평가]
  └─ 평가 질문 10개 생성 → 직접 검증 → 자동 평가 실행
```

각 단계에서 참조해야 할 파일이 다릅니다. **필요한 시점에만** 해당 파일을 읽으세요.

| 단계 | 참조 파일 |
|------|-----------|
| 1단계 시작 전 | `reference/mcp_best_practices.md` |
| 2단계 (TypeScript) | `reference/node_mcp_server.md` |
| 2단계 (Python) | `reference/python_mcp_server.md` |
| 4단계 | `reference/evaluation.md` |

---

## TypeScript vs Python, 뭘 선택해야 하나요?

| 상황 | 선택 |
|------|------|
| 타입 안전성이 중요하고 대규모 서버를 만들 때 | **TypeScript** |
| 빠르게 프로토타입을 만들고 싶을 때 | **Python** |
| 여러 환경(클라우드 등)에 배포할 때 | **TypeScript** |
| 데이터 처리나 ML 관련 서비스를 연동할 때 | **Python** |
| 잘 모르겠다면 | **TypeScript** (공식 권장) |

**서버 이름 규칙을 반드시 지키세요:**
- TypeScript: `{서비스}-mcp-server` (예: `github-mcp-server`)
- Python: `{서비스}_mcp` (예: `github_mcp`)

---

## 도구 하나를 만들 때 체크할 것들

도구 하나를 구현할 때마다 아래 항목을 확인하세요.

**이름**
- `{서비스}_{동작}_{대상}` 형태인가? (예: `slack_send_message`)
- 다른 MCP 서버와 이름이 겹치지 않는가?

**설명 (description)**
- 기능이 명확히 기술되어 있는가?
- 입력 매개변수, 반환값 형식, 사용 예시, 오류 처리가 포함되어 있는가?

**입력 검증**
- TypeScript: Zod 스키마에 `.strict()` 적용했는가?
- Python: Pydantic BaseModel에 `extra='forbid'` 설정했는가?

**어노테이션**
- `readOnlyHint` / `destructiveHint` / `idempotentHint` / `openWorldHint` 가 올바르게 설정되어 있는가?

**응답**
- JSON과 Markdown 두 형식을 모두 지원하는가?
- 결과가 25,000자를 초과할 경우 잘림 처리가 되어 있는가?
- 페이지네이션 (`has_more`, `next_offset`, `total`) 이 구현되어 있는가?

---

## 자주 하는 실수와 주의사항

### ❌ 오류 메시지를 허술하게 작성하는 경우
```typescript
// 나쁜 예
return { content: [{ type: "text", text: "오류가 발생했습니다" }] };

// 좋은 예
return { content: [{ type: "text", text: "오류: 리소스를 찾을 수 없습니다. ID가 올바른지 확인하세요." }] };
```
에이전트가 오류 메시지를 보고 다음 행동을 결정합니다. 구체적으로 작성하세요.

---

### ❌ 서비스 접두사 없이 도구 이름을 짓는 경우
```
# 나쁜 예
search_users
create_issue

# 좋은 예
github_search_users
github_create_issue
```
여러 MCP 서버를 함께 사용할 때 이름이 충돌합니다.

---

### ❌ API 키를 코드에 직접 작성하는 경우
```typescript
// 절대 금지
const API_KEY = "sk-abc1234...";

// 올바른 방법
const API_KEY = process.env.MY_SERVICE_API_KEY;
if (!API_KEY) {
  console.error("오류: MY_SERVICE_API_KEY 환경 변수가 필요합니다");
  process.exit(1);
}
```

---

### ❌ 비권장 API를 사용하는 경우 (TypeScript)
```typescript
// 나쁜 예 (구버전)
server.tool("tool_name", ...);
server.setRequestHandler(ListToolsRequestSchema, ...);

// 좋은 예 (최신)
server.registerTool("tool_name", ...);
```

---

### ❌ 모든 결과를 한 번에 불러오는 경우
```python
# 나쁜 예 - 메모리 문제 유발
all_items = fetch_all_items()  # 수천 개를 한번에

# 좋은 예 - 페이지네이션 적용
items = fetch_items(limit=20, offset=params.offset)
```

---

### ❌ 빌드 확인 없이 완료로 처리하는 경우 (TypeScript)
TypeScript는 반드시 빌드가 성공해야 완성입니다.
```bash
npm run build   # 이게 오류 없이 통과해야 합니다
```

---

## 평가 질문 만들 때 핵심 원칙

좋은 평가 질문의 조건을 한 줄씩 기억하세요:

| 조건 | 핵심 |
|------|------|
| **독립적** | 다른 질문의 답을 몰라도 풀 수 있어야 함 |
| **읽기 전용** | 데이터를 생성/수정/삭제하지 않아야 함 |
| **안정적** | 시간이 지나도 답이 바뀌지 않아야 함 |
| **검증 가능** | 문자열 비교 한 번으로 정답 확인 가능해야 함 |
| **어려워야 함** | 키워드 검색 한 번으로 풀리면 안 됨 |

**답변 형식은 질문 안에 명시하세요:**
> "YYYY/MM/DD 형식으로 답하세요", "True 또는 False로만 답하세요"

---

## 평가 실행 명령어 요약

```bash
# 의존성 설치
pip install -r scripts/requirements.txt

# API 키 설정
export ANTHROPIC_API_KEY=your_key_here

# Python 서버 평가
python scripts/evaluation.py -t stdio -c python -a my_server.py evaluation.xml

# Node 서버 평가
python scripts/evaluation.py -t stdio -c node -a dist/index.js evaluation.xml

# 결과 파일로 저장
python scripts/evaluation.py -t stdio -c python -a my_server.py -o report.md evaluation.xml
```

---

## 참조 파일 구조

```
mcp-builder/
├── 사용가이드.md                  ← 지금 읽고 있는 파일
├── SKILL.md                       ← 전체 워크플로우 (메인 진입점)
├── reference/
│   ├── mcp_best_practices.md      ← 이름/응답형식/보안 규칙 (1단계)
│   ├── node_mcp_server.md         ← TypeScript 구현 상세 (2단계)
│   ├── python_mcp_server.md       ← Python 구현 상세 (2단계)
│   └── evaluation.md              ← 평가 생성 및 실행 (4단계)
└── scripts/
    ├── evaluation.py              ← 평가 실행 스크립트
    ├── connections.py             ← 연결 관리
    ├── example_evaluation.xml     ← 평가 예제
    └── requirements.txt           ← Python 의존성
```
