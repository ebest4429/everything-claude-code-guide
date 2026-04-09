# MCP 검색 및 연결

플러그인 커스터마이징 중 MCP를 찾고 연결하는 방법입니다.

## 사용 가능한 도구

### `search_mcp_registry`
MCP 디렉토리에서 사용 가능한 커넥터를 검색합니다.

**입력:** `{ "keywords": ["검색", "키워드", "배열"] }`

**출력:** 최대 10개 결과, 각 결과에 포함된 정보:
- `name`: MCP 표시 이름
- `description`: 한 줄 설명
- `tools`: MCP가 제공하는 도구 이름 목록
- `url`: MCP 엔드포인트 URL (`.mcp.json`에 사용)
- `directoryUuid`: suggest_connectors에 사용할 UUID
- `connected`: 사용자가 이 MCP를 연결했는지 여부 (Boolean)

### `suggest_connectors`
사용자가 MCP를 설치/연결할 수 있도록 연결 버튼을 표시합니다.

**입력:** `{ "directoryUuids": ["uuid1", "uuid2"] }`

**출력:** 각 MCP의 연결 버튼이 있는 UI 렌더링

## 카테고리별 키워드 매핑

| 카테고리 | 검색 키워드 |
|----------|------------|
| `project-management` | `["asana", "jira", "linear", "monday", "tasks"]` |
| `software-coding` | `["github", "gitlab", "bitbucket", "code"]` |
| `chat` | `["slack", "teams", "discord"]` |
| `documents` | `["google docs", "notion", "confluence"]` |
| `calendar` | `["google calendar", "calendar"]` |
| `email` | `["gmail", "outlook", "email"]` |
| `design-graphics` | `["figma", "sketch", "design"]` |
| `analytics-bi` | `["datadog", "grafana", "analytics"]` |
| `crm` | `["salesforce", "hubspot", "crm"]` |
| `wiki-knowledge-base` | `["notion", "confluence", "outline", "wiki"]` |
| `data-warehouse` | `["bigquery", "snowflake", "redshift"]` |
| `conversation-intelligence` | `["gong", "chorus", "call recording"]` |

## 워크플로우

1. **커스터마이징 포인트 찾기**: `~~` 접두사 값 확인 (예: `~~Jira`)
2. **이전 단계 결과 확인**: 어떤 도구를 사용하는지 이미 파악했는가?
   - **예**: 해당 도구를 검색하여 `url`을 얻고 5단계로 이동
   - **아니오**: 3단계로 진행
3. **검색**: 매핑된 키워드로 `search_mcp_registry` 호출
4. **선택지 제시 및 확인**: 모든 결과를 보여주고 어떤 것을 사용하는지 확인
5. **필요 시 연결**: 연결되지 않은 경우 `suggest_connectors` 호출
6. **MCP 설정 업데이트**: 검색 결과의 `url`을 사용하여 설정 추가

## 플러그인 MCP 설정 업데이트

### 설정 파일 찾기

1. **`plugin.json`에서 `mcpServers` 필드 확인:**
   ```json
   {
     "name": "my-plugin",
     "mcpServers": "./config/servers.json"
   }
   ```
   해당 필드가 있으면 그 경로의 파일을 수정합니다.

2. **`mcpServers` 필드가 없는 경우**, 플러그인 루트의 `.mcp.json`을 사용합니다 (기본값).

3. **`mcpServers`가 `.mcpb` 파일만 가리키는 경우** (번들 서버), 플러그인 루트에 새 `.mcp.json`을 생성합니다.

### 설정 파일 형식

래핑/비래핑 형식 모두 지원됩니다:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

`search_mcp_registry` 결과의 `url` 필드를 사용합니다.

### URL이 없는 디렉토리 항목

일부 디렉토리 항목은 엔드포인트가 동적이라 `url`이 없습니다 — 관리자가 서버를 연결할 때 직접 제공합니다. 이러한 서버는 플러그인 MCP 설정에서 **이름**으로 참조할 수 있습니다: 설정의 MCP 서버 이름이 디렉토리 항목 이름과 일치하면 URL 일치와 동일하게 처리됩니다.
