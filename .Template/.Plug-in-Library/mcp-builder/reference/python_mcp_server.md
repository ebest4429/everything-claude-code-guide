# Python MCP 서버 구현 가이드

## 개요

MCP Python SDK를 사용한 MCP 서버 구현의 Python 특화 모범 사례와 예제를 제공합니다. 서버 설정, 도구 등록 패턴, Pydantic을 사용한 입력 검증, 오류 처리, 완전한 작동 예제를 다룹니다.

---

## 빠른 참조

### 핵심 임포트
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
```

### 서버 초기화
```python
mcp = FastMCP("service_mcp")
```

### 도구 등록 패턴
```python
@mcp.tool(name="tool_name", annotations={...})
async def tool_function(params: InputModel) -> str:
    # 구현
    pass
```

---

## MCP Python SDK와 FastMCP

공식 MCP Python SDK의 FastMCP는 MCP 서버 구축을 위한 고수준 프레임워크입니다:
- 함수 시그니처와 독스트링에서 자동으로 설명 및 inputSchema 생성
- 입력 검증을 위한 Pydantic 모델 통합
- `@mcp.tool` 데코레이터 기반 도구 등록

**전체 SDK 문서는 WebFetch로 로드하세요:**
`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`

## 서버 이름 규칙

Python MCP 서버는 다음 이름 패턴을 따라야 합니다:
- **형식**: `{서비스}_mcp` (소문자 + 밑줄)
- **예**: `github_mcp`, `jira_mcp`, `stripe_mcp`

이름은:
- 일반적이어야 함 (특정 기능에 종속되지 않음)
- 통합되는 서비스/API를 설명적으로 나타내야 함
- 작업 설명에서 쉽게 추론 가능해야 함
- 버전 번호나 날짜를 포함하지 않아야 함

## 도구 구현

### 도구 이름 지정

도구 이름에는 snake_case를 사용하고 (예: "search_users", "create_project", "get_channel_info") 명확하고 동작 중심적인 이름을 사용하세요.

**이름 충돌 방지**: 겹치는 것을 방지하기 위해 서비스 컨텍스트를 포함하세요:
- `send_message` 대신 `slack_send_message`
- `create_issue` 대신 `github_create_issue`
- `list_tasks` 대신 `asana_list_tasks`

### FastMCP를 사용한 도구 구조

도구는 Pydantic 모델을 사용한 입력 검증과 함께 `@mcp.tool` 데코레이터를 사용하여 정의합니다:

```python
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# MCP 서버 초기화
mcp = FastMCP("example_mcp")

# 입력 검증을 위한 Pydantic 모델 정의
class ServiceToolInput(BaseModel):
    '''서비스 도구 작업을 위한 입력 모델.'''
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 문자열 공백 자동 제거
        validate_assignment=True,    # 할당 시 검증
        extra='forbid'              # 추가 필드 금지
    )

    param1: str = Field(..., description="첫 번째 매개변수 설명 (예: 'user123', 'project-abc')", min_length=1, max_length=100)
    param2: Optional[int] = Field(default=None, description="선택적 정수 매개변수 (제약 조건 포함)", ge=0, le=1000)
    tags: Optional[List[str]] = Field(default_factory=list, description="적용할 태그 목록", max_items=10)

@mcp.tool(
    name="service_tool_name",
    annotations={
        "title": "사람이 읽을 수 있는 도구 제목",
        "readOnlyHint": True,     # 도구가 환경을 수정하지 않음
        "destructiveHint": False,  # 도구가 파괴적 작업을 수행하지 않음
        "idempotentHint": True,    # 반복 호출이 추가 효과 없음
        "openWorldHint": False     # 도구가 외부 엔티티와 상호작용하지 않음
    }
)
async def service_tool_name(params: ServiceToolInput) -> str:
    '''도구 설명이 자동으로 'description' 필드가 됩니다.

    이 도구는 서비스에서 특정 작업을 수행합니다. 처리하기 전에
    ServiceToolInput Pydantic 모델로 모든 입력을 검증합니다.

    Args:
        params (ServiceToolInput): 검증된 입력 매개변수:
            - param1 (str): 첫 번째 매개변수 설명
            - param2 (Optional[int]): 기본값이 있는 선택적 매개변수
            - tags (Optional[List[str]]): 태그 목록

    Returns:
        str: 작업 결과가 포함된 JSON 형식의 응답
    '''
    # 구현
    pass
```

## Pydantic v2 핵심 기능

- 중첩된 `Config` 클래스 대신 `model_config` 사용
- 비권장된 `validator` 대신 `field_validator` 사용
- 비권장된 `dict()` 대신 `model_dump()` 사용
- 검증기에 `@classmethod` 데코레이터 필요
- 검증기 메서드에 타입 힌트 필요

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict

class CreateUserInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    name: str = Field(..., description="사용자 이름", min_length=1, max_length=100)
    email: str = Field(..., description="이메일 주소", pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., description="나이", ge=0, le=150)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("이메일은 비어있을 수 없습니다")
        return v.lower()
```

## 응답 형식 옵션

유연성을 위해 여러 출력 형식을 지원하세요:

```python
from enum import Enum

class ResponseFormat(str, Enum):
    '''도구 응답의 출력 형식.'''
    MARKDOWN = "markdown"
    JSON = "json"

class UserSearchInput(BaseModel):
    query: str = Field(..., description="검색 쿼리")
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="출력 형식: 사람이 읽기 위한 'markdown' 또는 기계 처리용 'json'"
    )
```

**Markdown 형식**:
- 헤더, 목록, 서식을 사용하여 명확하게
- 타임스탬프를 사람이 읽을 수 있는 형식으로 변환 (에포크 대신 "2024-01-15 10:30:00 UTC")
- 표시 이름과 함께 ID를 괄호 안에 표시 (예: "@홍길동 (U123456)")
- 상세한 메타데이터 생략
- 관련 정보를 논리적으로 그룹화

**JSON 형식**:
- 프로그래밍 처리에 적합한 완전한 구조화된 데이터 반환
- 사용 가능한 모든 필드와 메타데이터 포함
- 일관된 필드 이름과 타입 사용

## 페이지네이션 구현

리소스를 나열하는 도구의 경우:

```python
class ListInput(BaseModel):
    limit: Optional[int] = Field(default=20, description="반환할 최대 결과 수", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="페이지네이션을 위해 건너뛸 결과 수", ge=0)

async def list_items(params: ListInput) -> str:
    data = await api_request(limit=params.limit, offset=params.offset)

    response = {
        "total": data["total"],
        "count": len(data["items"]),
        "offset": params.offset,
        "items": data["items"],
        "has_more": data["total"] > params.offset + len(data["items"]),
        "next_offset": params.offset + len(data["items"]) if data["total"] > params.offset + len(data["items"]) else None
    }
    return json.dumps(response, indent=2)
```

## 오류 처리

명확하고 실행 가능한 오류 메시지를 제공하세요:

```python
def _handle_api_error(e: Exception) -> str:
    '''모든 도구에서 일관된 오류 포맷팅.'''
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "오류: 리소스를 찾을 수 없습니다. ID가 올바른지 확인하세요."
        elif e.response.status_code == 403:
            return "오류: 접근이 거부되었습니다. 이 리소스에 대한 권한이 없습니다."
        elif e.response.status_code == 429:
            return "오류: 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요."
        return f"오류: API 요청이 상태 코드 {e.response.status_code}로 실패했습니다"
    elif isinstance(e, httpx.TimeoutException):
        return "오류: 요청 시간이 초과되었습니다. 다시 시도하세요."
    return f"오류: 예기치 않은 오류 발생: {type(e).__name__}"
```

## 공유 유틸리티

재사용 가능한 함수로 공통 기능을 추출하세요:

```python
# 공유 API 요청 함수
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    '''모든 API 호출에 사용하는 재사용 가능한 함수.'''
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            timeout=30.0,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
```

## Async/Await 모범 사례

네트워크 요청 및 I/O 작업에 항상 async/await를 사용하세요:

```python
# 좋은 예: 비동기 네트워크 요청
async def fetch_data(resource_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/resource/{resource_id}")
        response.raise_for_status()
        return response.json()

# 나쁜 예: 동기 요청 (차단됨)
def fetch_data(resource_id: str) -> dict:
    response = requests.get(f"{API_URL}/resource/{resource_id}")
    return response.json()
```

## 도구 독스트링

모든 도구는 명시적 타입 정보가 포함된 포괄적 독스트링이 필수입니다:

```python
async def search_users(params: UserSearchInput) -> str:
    '''
    이름, 이메일 또는 팀으로 Example 시스템의 사용자를 검색합니다.

    이 도구는 Example 플랫폼의 모든 사용자 프로필을 검색하며,
    부분 일치와 다양한 검색 필터를 지원합니다. 사용자를
    생성하거나 수정하지 않으며, 기존 사용자만 검색합니다.

    Args:
        params (UserSearchInput): 검증된 입력 매개변수:
            - query (str): 이름/이메일 매칭 검색 문자열
            - limit (Optional[int]): 최대 반환 결과 수, 1-100 (기본: 20)
            - offset (Optional[int]): 페이지네이션을 위한 건너뛸 결과 수 (기본: 0)

    Returns:
        str: 다음 스키마를 가진 JSON 형식 문자열:

        성공 응답:
        {
            "total": int,           # 총 일치 수
            "count": int,           # 이 응답의 결과 수
            "offset": int,          # 현재 페이지네이션 오프셋
            "users": [
                {
                    "id": str,      # 사용자 ID (예: "U123456789")
                    "name": str,    # 이름 (예: "홍길동")
                    "email": str,   # 이메일 (예: "hong@example.com")
                    "team": str     # 팀 이름 (선택 사항)
                }
            ]
        }

        오류 응답:
        "오류: <오류 메시지>" 또는 "'{query}'와 일치하는 사용자 없음"

    Examples:
        - 사용: "마케팅 팀원 모두 찾기" -> query="team:marketing"
        - 사용: "홍길동 계정 검색" -> query="홍길동"
        - 미사용: 사용자를 생성해야 할 때 (example_create_user 사용)
        - 미사용: 사용자 ID가 있고 전체 세부 정보가 필요할 때 (example_get_user 사용)

    Error Handling:
        - 입력 검증 오류는 Pydantic 모델이 처리
        - 요청이 너무 많으면 "오류: 요청 한도 초과" 반환 (429 상태)
        - API 키가 유효하지 않으면 "오류: API 인증 실패" 반환 (401 상태)
    '''
```

## 완전한 예제

```python
#!/usr/bin/env python3
'''
Example 서비스를 위한 MCP 서버.

이 서버는 사용자 검색, 프로젝트 관리, 데이터 내보내기 기능을 포함하여
Example API와 상호작용하는 도구를 제공합니다.
'''

from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
import json
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# MCP 서버 초기화
mcp = FastMCP("example_mcp")

# 상수
API_BASE_URL = "https://api.example.com/v1"

# 열거형
class ResponseFormat(str, Enum):
    '''도구 응답의 출력 형식.'''
    MARKDOWN = "markdown"
    JSON = "json"

# 입력 검증을 위한 Pydantic 모델
class UserSearchInput(BaseModel):
    '''사용자 검색 작업을 위한 입력 모델.'''
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    query: str = Field(..., description="이름/이메일 매칭 검색 문자열", min_length=2, max_length=200)
    limit: Optional[int] = Field(default=20, description="반환할 최대 결과 수", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="페이지네이션을 위해 건너뛸 결과 수", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="출력 형식")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("쿼리는 비어있거나 공백만 있을 수 없습니다")
        return v.strip()

# 공유 유틸리티 함수
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    '''모든 API 호출에 사용하는 재사용 가능한 함수.'''
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method, f"{API_BASE_URL}/{endpoint}", timeout=30.0, **kwargs
        )
        response.raise_for_status()
        return response.json()

def _handle_api_error(e: Exception) -> str:
    '''모든 도구에서 일관된 오류 포맷팅.'''
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "오류: 리소스를 찾을 수 없습니다. ID가 올바른지 확인하세요."
        elif e.response.status_code == 403:
            return "오류: 접근이 거부되었습니다. 권한이 없습니다."
        elif e.response.status_code == 429:
            return "오류: 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요."
        return f"오류: API 요청이 상태 코드 {e.response.status_code}로 실패했습니다"
    elif isinstance(e, httpx.TimeoutException):
        return "오류: 요청 시간이 초과되었습니다. 다시 시도하세요."
    return f"오류: 예기치 않은 오류 발생: {type(e).__name__}"

# 도구 정의
@mcp.tool(
    name="example_search_users",
    annotations={
        "title": "Example 사용자 검색",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def example_search_users(params: UserSearchInput) -> str:
    '''이름, 이메일 또는 팀으로 Example 시스템의 사용자를 검색합니다.

    [위에 표시된 전체 독스트링]
    '''
    try:
        data = await _make_api_request(
            "users/search",
            params={"q": params.query, "limit": params.limit, "offset": params.offset}
        )

        users = data.get("users", [])
        total = data.get("total", 0)

        if not users:
            return f"'{params.query}'와 일치하는 사용자가 없습니다"

        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# 사용자 검색 결과: '{params.query}'", ""]
            lines.append(f"총 {total}명 발견 (${len(users)}명 표시)")
            lines.append("")
            for user in users:
                lines.append(f"## {user['name']} ({user['id']})")
                lines.append(f"- **이메일**: {user['email']}")
                if user.get('team'):
                    lines.append(f"- **팀**: {user['team']}")
                lines.append("")
            return "\n".join(lines)
        else:
            response = {
                "total": total,
                "count": len(users),
                "offset": params.offset,
                "users": users
            }
            return json.dumps(response, indent=2, ensure_ascii=False)

    except Exception as e:
        return _handle_api_error(e)

if __name__ == "__main__":
    mcp.run()
```

---

## 고급 FastMCP 기능

### Context 매개변수 주입

FastMCP는 로깅, 진행 보고, 리소스 읽기, 사용자 상호작용을 위한 `Context` 매개변수를 자동으로 주입할 수 있습니다:

```python
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("example_mcp")

@mcp.tool()
async def advanced_search(query: str, ctx: Context) -> str:
    '''로깅과 진행 상황을 위한 컨텍스트 접근이 가능한 고급 도구.'''

    # 긴 작업의 진행 상황 보고
    await ctx.report_progress(0.25, "검색 시작 중...")

    # 디버깅을 위한 로깅
    await ctx.log_info("쿼리 처리 중", {"query": query})

    results = await search_api(query)
    await ctx.report_progress(0.75, "결과 포맷팅 중...")

    return format_results(results)

@mcp.tool()
async def interactive_tool(resource_id: str, ctx: Context) -> str:
    '''사용자로부터 추가 입력을 요청할 수 있는 도구.'''
    api_key = await ctx.elicit(
        prompt="API 키를 입력해주세요:",
        input_type="password"
    )
    return await api_call(resource_id, api_key)
```

**Context 기능:**
- `ctx.report_progress(progress, message)` - 긴 작업의 진행 보고
- `ctx.log_info(message, data)` / `ctx.log_error()` / `ctx.log_debug()` - 로깅
- `ctx.elicit(prompt, input_type)` - 사용자 입력 요청
- `ctx.fastmcp.name` - 서버 설정 접근
- `ctx.read_resource(uri)` - MCP 리소스 읽기

### 리소스 등록

URI 기반 접근을 위해 데이터를 리소스로 노출:

```python
@mcp.resource("file://documents/{name}")
async def get_document(name: str) -> str:
    '''문서를 MCP 리소스로 노출.'''
    document_path = f"./docs/{name}"
    with open(document_path, "r") as f:
        return f.read()

@mcp.resource("config://settings/{key}")
async def get_setting(key: str, ctx: Context) -> str:
    '''설정을 컨텍스트가 있는 리소스로 노출.'''
    settings = await load_settings()
    return json.dumps(settings.get(key, {}))
```

**리소스 vs 도구 사용 시기:**
- **리소스**: 간단한 URI 기반 매개변수로 데이터 접근
- **도구**: 검증과 비즈니스 로직이 필요한 복잡한 작업

### 구조화된 출력 타입

FastMCP는 문자열 외에도 여러 반환 타입을 지원합니다:

```python
from typing import TypedDict
from pydantic import BaseModel

# 구조화된 반환을 위한 TypedDict
class UserData(TypedDict):
    id: str
    name: str
    email: str

@mcp.tool()
async def get_user_typed(user_id: str) -> UserData:
    '''구조화된 데이터 반환 - FastMCP가 직렬화 처리.'''
    return {"id": user_id, "name": "홍길동", "email": "hong@example.com"}
```

### Lifespan 관리 (수명 주기 관리)

요청 간에 유지되는 리소스 초기화:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan():
    '''서버 수명 동안 유지되는 리소스 관리.'''
    db = await connect_to_database()
    config = load_configuration()
    yield {"db": db, "config": config}  # 모든 도구에서 사용 가능
    await db.close()  # 종료 시 정리

mcp = FastMCP("example_mcp", lifespan=app_lifespan)

@mcp.tool()
async def query_data(query: str, ctx: Context) -> str:
    '''컨텍스트를 통해 lifespan 리소스에 접근.'''
    db = ctx.request_context.lifespan_state["db"]
    results = await db.query(query)
    return format_results(results)
```

### 전송 옵션

```python
# stdio 전송 (로컬 도구용) - 기본값
if __name__ == "__main__":
    mcp.run()

# Streamable HTTP 전송 (원격 서버용)
if __name__ == "__main__":
    mcp.run(transport="streamable_http", port=8000)
```

---

## 코드 모범 사례

### 코드 조합성 및 재사용성

구현은 반드시 조합성과 코드 재사용을 우선시해야 합니다:

1. **공통 기능 추출**:
   - 여러 도구에서 사용되는 작업에 재사용 가능한 헬퍼 함수 생성
   - HTTP 요청을 위한 공유 API 클라이언트 구축
   - 오류 처리 로직을 유틸리티 함수에 중앙화
   - Markdown 또는 JSON 필드 선택 및 포맷팅 기능을 공유

2. **중복 방지**:
   - 도구 간에 유사한 코드를 복사/붙여넣기 절대 금지
   - 유사한 로직을 두 번 작성하게 된다면 함수로 추출
   - 페이지네이션, 필터링, 필드 선택, 포맷팅은 공유
   - 인증/권한 로직 중앙화

### Python 특화 모범 사례

1. **타입 힌트 사용**: 함수 매개변수와 반환 값에 항상 타입 어노테이션 포함
2. **Pydantic 모델**: 모든 입력 검증에 명확한 Pydantic 모델 정의
3. **수동 검증 피하기**: Pydantic이 제약 조건으로 입력 검증을 처리하게 함
4. **적절한 임포트**: 임포트 그룹화 (표준 라이브러리, 서드파티, 로컬)
5. **오류 처리**: 특정 예외 타입 사용 (일반 Exception 대신 httpx.HTTPStatusError)
6. **Async 컨텍스트 관리자**: 정리가 필요한 리소스에 `async with` 사용
7. **상수**: 모듈 수준에서 UPPER_CASE로 상수 정의

## 품질 체크리스트

Python MCP 서버 구현 완료 전에 확인하세요:

### 전략적 설계
- [ ] 도구가 단순 API 엔드포인트 래퍼가 아닌 완전한 워크플로우 지원
- [ ] 도구 이름이 자연스러운 작업 세분화를 반영
- [ ] 응답 형식이 에이전트 컨텍스트 효율성에 최적화
- [ ] 오류 메시지가 에이전트를 올바른 사용법으로 안내

### 구현 품질
- [ ] 가장 중요하고 가치 있는 도구 구현
- [ ] 모든 도구에 설명적 이름과 문서 있음
- [ ] 비슷한 작업 간에 반환 타입 일관성 있음
- [ ] 모든 외부 호출에 오류 처리 구현
- [ ] 서버 이름이 `{서비스}_mcp` 형식을 따름
- [ ] 모든 네트워크 작업이 async/await 사용
- [ ] 공통 기능이 재사용 가능한 함수로 추출
- [ ] 오류 메시지가 명확하고 실행 가능하며 교육적

### 도구 설정
- [ ] 모든 도구에 데코레이터에서 'name'과 'annotations' 구현
- [ ] 어노테이션 올바르게 설정
- [ ] 모든 도구가 Field() 정의와 함께 Pydantic BaseModel을 입력 검증에 사용
- [ ] 모든 Pydantic Field에 명시적 타입과 설명 + 제약 조건
- [ ] 포괄적 독스트링 + 명시적 입출력 타입

### 고급 기능 (해당되는 경우)
- [ ] 로깅, 진행 상황, 사용자 입력에 Context 주입 사용
- [ ] 적절한 데이터 엔드포인트에 리소스 등록
- [ ] 영구적 연결에 Lifespan 관리 구현
- [ ] 적절한 전송 설정 (stdio 또는 Streamable HTTP)

### 코드 품질
- [ ] 파일에 적절한 임포트 포함 (Pydantic 임포트 포함)
- [ ] 페이지네이션 적절히 구현
- [ ] 잠재적으로 큰 결과 집합에 필터링 옵션 제공
- [ ] 모든 async 함수가 `async def`로 올바르게 정의
- [ ] HTTP 클라이언트 사용이 async 패턴과 적절한 컨텍스트 관리자 사용
- [ ] 코드 전체에 타입 힌트 사용
- [ ] 상수가 모듈 수준에서 UPPER_CASE로 정의

### 테스트
- [ ] 서버가 성공적으로 실행됨: `python your_server.py --help`
- [ ] 모든 임포트가 올바르게 해결
- [ ] 샘플 도구 호출이 예상대로 작동
- [ ] 오류 시나리오가 정상적으로 처리됨
