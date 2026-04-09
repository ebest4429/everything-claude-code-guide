# Node/TypeScript MCP 서버 구현 가이드

## 개요

MCP TypeScript SDK를 사용한 MCP 서버 구현의 Node/TypeScript 특화 모범 사례와 예제를 제공합니다. 프로젝트 구조, 서버 설정, 도구 등록 패턴, Zod를 사용한 입력 검증, 오류 처리, 완전한 작동 예제를 다룹니다.

---

## 빠른 참조

### 핵심 임포트
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import express from "express";
import { z } from "zod";
```

### 서버 초기화
```typescript
const server = new McpServer({
  name: "service-mcp-server",
  version: "1.0.0"
});
```

### 도구 등록 패턴
```typescript
server.registerTool(
  "tool_name",
  {
    title: "도구 표시 이름",
    description: "도구가 하는 일",
    inputSchema: { param: z.string() },
    outputSchema: { result: z.string() }
  },
  async ({ param }) => {
    const output = { result: `처리됨: ${param}` };
    return {
      content: [{ type: "text", text: JSON.stringify(output) }],
      structuredContent: output // 구조화된 데이터를 위한 최신 패턴
    };
  }
);
```

---

## MCP TypeScript SDK

공식 MCP TypeScript SDK가 제공하는 기능:
- 서버 초기화를 위한 `McpServer` 클래스
- 도구 등록을 위한 `registerTool` 메서드
- 런타임 입력 검증을 위한 Zod 스키마 통합
- 타입 안전한 도구 핸들러 구현

**중요 - 최신 API만 사용:**
- **사용할 것**: `server.registerTool()`, `server.registerResource()`, `server.registerPrompt()`
- **사용하지 말 것**: 이전 비권장 API인 `server.tool()`, `server.setRequestHandler(ListToolsRequestSchema, ...)`, 수동 핸들러 등록 등
- `register*` 메서드는 더 나은 타입 안전성, 자동 스키마 처리를 제공하며 권장되는 접근 방식

SDK 문서에서 전체 세부사항을 확인하세요.

## 서버 이름 규칙

Node/TypeScript MCP 서버는 다음 이름 패턴을 따라야 합니다:
- **형식**: `{서비스}-mcp-server` (소문자 + 하이픈)
- **예**: `github-mcp-server`, `jira-mcp-server`, `stripe-mcp-server`

이름은:
- 일반적이어야 함 (특정 기능에 종속되지 않음)
- 통합되는 서비스/API를 설명적으로 나타내야 함
- 작업 설명에서 쉽게 추론 가능해야 함
- 버전 번호나 날짜를 포함하지 않아야 함

## 프로젝트 구조

Node/TypeScript MCP 서버에 다음 구조를 만드세요:

```
{서비스}-mcp-server/
├── package.json
├── tsconfig.json
├── README.md
├── src/
│   ├── index.ts          # McpServer 초기화가 포함된 메인 진입점
│   ├── types.ts          # TypeScript 타입 정의 및 인터페이스
│   ├── tools/            # 도구 구현 (도메인별 파일 하나씩)
│   ├── services/         # API 클라이언트 및 공유 유틸리티
│   ├── schemas/          # Zod 검증 스키마
│   └── constants.ts      # 공유 상수 (API_URL, CHARACTER_LIMIT 등)
└── dist/                 # 빌드된 JavaScript 파일 (진입점: dist/index.js)
```

## 도구 구현

### 도구 이름 지정

도구 이름에는 snake_case를 사용하고 (예: "search_users", "create_project", "get_channel_info") 명확하고 동작 중심적인 이름을 사용하세요.

**이름 충돌 방지**: 겹치는 것을 방지하기 위해 서비스 컨텍스트를 포함하세요:
- `send_message` 대신 `slack_send_message`
- `create_issue` 대신 `github_create_issue`
- `list_tasks` 대신 `asana_list_tasks`

### 도구 구조

도구는 `registerTool` 메서드를 사용하여 다음 요구사항으로 등록됩니다:
- 런타임 입력 검증 및 타입 안전성을 위해 Zod 스키마 사용
- `description` 필드는 명시적으로 제공해야 함 - JSDoc 주석은 자동으로 추출되지 않음
- `title`, `description`, `inputSchema`, `annotations`를 명시적으로 제공
- `inputSchema`는 Zod 스키마 객체여야 함 (JSON 스키마 아님)
- 모든 매개변수와 반환 값을 명시적으로 타입 지정

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "example-mcp",
  version: "1.0.0"
});

// 입력 검증을 위한 Zod 스키마
const UserSearchInputSchema = z.object({
  query: z.string()
    .min(2, "쿼리는 최소 2자 이상이어야 합니다")
    .max(200, "쿼리는 200자를 초과할 수 없습니다")
    .describe("이름/이메일과 매칭할 검색 문자열"),
  limit: z.number()
    .int()
    .min(1)
    .max(100)
    .default(20)
    .describe("반환할 최대 결과 수"),
  offset: z.number()
    .int()
    .min(0)
    .default(0)
    .describe("페이지네이션을 위해 건너뛸 결과 수"),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("출력 형식: 사람이 읽기 위한 'markdown' 또는 기계 처리용 'json'")
}).strict();

// Zod 스키마에서 타입 정의
type UserSearchInput = z.infer<typeof UserSearchInputSchema>;

server.registerTool(
  "example_search_users",
  {
    title: "Example 사용자 검색",
    description: `이름, 이메일 또는 팀으로 Example 시스템의 사용자를 검색합니다.

이 도구는 Example 플랫폼의 모든 사용자 프로필을 검색하며, 부분 일치와 다양한 검색 필터를 지원합니다.
사용자를 생성하거나 수정하지 않으며, 기존 사용자만 검색합니다.

Args:
  - query (string): 이름/이메일 매칭 검색 문자열
  - limit (number): 반환할 최대 결과 수, 1-100 (기본: 20)
  - offset (number): 페이지네이션을 위해 건너뛸 결과 수 (기본: 0)
  - response_format ('markdown' | 'json'): 출력 형식 (기본: 'markdown')

Returns:
  JSON 형식의 경우:
  {
    "total": number,           // 찾은 총 일치 수
    "count": number,           // 이 응답의 결과 수
    "offset": number,          // 현재 페이지네이션 오프셋
    "users": [
      {
        "id": string,          // 사용자 ID (예: "U123456789")
        "name": string,        // 이름 (예: "홍길동")
        "email": string,       // 이메일 주소
        "team": string,        // 팀 이름 (선택 사항)
        "active": boolean      // 사용자 활성 여부
      }
    ],
    "has_more": boolean,       // 추가 결과 존재 여부
    "next_offset": number      // 다음 페이지 오프셋 (has_more가 true인 경우)
  }

Examples:
  - 사용: "마케팅 팀원 모두 찾기" -> query="team:marketing"
  - 사용: "John 계정 검색" -> query="john"
  - 미사용: 사용자를 생성해야 할 때 (example_create_user 사용)

Error Handling:
  - 요청이 너무 많으면 "오류: 요청 한도 초과" 반환 (429 상태)
  - 검색 결과가 없으면 "'{query}'와 일치하는 사용자 없음" 반환`,
    inputSchema: UserSearchInputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true
    }
  },
  async (params: UserSearchInput) => {
    try {
      const data = await makeApiRequest<any>(
        "users/search",
        "GET",
        undefined,
        { q: params.query, limit: params.limit, offset: params.offset }
      );

      const users = data.users || [];
      const total = data.total || 0;

      if (!users.length) {
        return {
          content: [{ type: "text", text: `'${params.query}'와 일치하는 사용자가 없습니다` }]
        };
      }

      const output = {
        total,
        count: users.length,
        offset: params.offset,
        users: users.map((user: any) => ({
          id: user.id,
          name: user.name,
          email: user.email,
          ...(user.team ? { team: user.team } : {}),
          active: user.active ?? true
        })),
        has_more: total > params.offset + users.length,
        ...(total > params.offset + users.length ? {
          next_offset: params.offset + users.length
        } : {})
      };

      let textContent: string;
      if (params.response_format === ResponseFormat.MARKDOWN) {
        const lines = [`# 사용자 검색 결과: '${params.query}'`, "",
          `총 ${total}명 발견 (${users.length}명 표시)`, ""];
        for (const user of users) {
          lines.push(`## ${user.name} (${user.id})`);
          lines.push(`- **이메일**: ${user.email}`);
          if (user.team) lines.push(`- **팀**: ${user.team}`);
          lines.push("");
        }
        textContent = lines.join("\n");
      } else {
        textContent = JSON.stringify(output, null, 2);
      }

      return {
        content: [{ type: "text", text: textContent }],
        structuredContent: output
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: handleApiError(error) }]
      };
    }
  }
);
```

## Zod 스키마를 사용한 입력 검증

Zod는 런타임 타입 검증을 제공합니다:

```typescript
import { z } from "zod";

// 검증이 포함된 기본 스키마
const CreateUserSchema = z.object({
  name: z.string()
    .min(1, "이름은 필수입니다")
    .max(100, "이름은 100자를 초과할 수 없습니다"),
  email: z.string()
    .email("유효하지 않은 이메일 형식"),
  age: z.number()
    .int("나이는 정수여야 합니다")
    .min(0, "나이는 음수가 될 수 없습니다")
    .max(150, "나이는 150을 초과할 수 없습니다")
}).strict();  // .strict()로 추가 필드 금지

// 열거형
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

const SearchSchema = z.object({
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("출력 형식")
});

// 기본값이 있는 선택적 필드
const PaginationSchema = z.object({
  limit: z.number()
    .int()
    .min(1)
    .max(100)
    .default(20)
    .describe("반환할 최대 결과 수"),
  offset: z.number()
    .int()
    .min(0)
    .default(0)
    .describe("건너뛸 결과 수")
});
```

## 응답 형식 옵션

유연성을 위해 여러 출력 형식을 지원하세요:

```typescript
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

const inputSchema = z.object({
  query: z.string(),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("출력 형식: 사람이 읽기 위한 'markdown' 또는 기계 처리용 'json'")
});
```

**Markdown 형식**:
- 헤더, 목록, 서식을 사용하여 명확하게
- 타임스탬프를 사람이 읽을 수 있는 형식으로 변환
- 표시 이름과 함께 ID를 괄호 안에 표시
- 상세한 메타데이터 생략
- 관련 정보를 논리적으로 그룹화

**JSON 형식**:
- 프로그래밍 처리에 적합한 완전한 구조화된 데이터 반환
- 사용 가능한 모든 필드와 메타데이터 포함
- 일관된 필드 이름과 타입 사용

## 페이지네이션 구현

리소스를 나열하는 도구의 경우:

```typescript
const ListSchema = z.object({
  limit: z.number().int().min(1).max(100).default(20),
  offset: z.number().int().min(0).default(0)
});

async function listItems(params: z.infer<typeof ListSchema>) {
  const data = await apiRequest(params.limit, params.offset);

  const response = {
    total: data.total,
    count: data.items.length,
    offset: params.offset,
    items: data.items,
    has_more: data.total > params.offset + data.items.length,
    next_offset: data.total > params.offset + data.items.length
      ? params.offset + data.items.length
      : undefined
  };

  return JSON.stringify(response, null, 2);
}
```

## 문자 제한 및 잘림 처리

응답이 너무 길어지는 것을 방지하기 위해 CHARACTER_LIMIT 상수를 추가하세요:

```typescript
// constants.ts에서 모듈 수준으로
export const CHARACTER_LIMIT = 25000;  // 최대 응답 크기 (문자 수)

async function searchTool(params: SearchInput) {
  let result = generateResponse(data);

  // 문자 제한 확인 후 필요시 잘림
  if (result.length > CHARACTER_LIMIT) {
    const truncatedData = data.slice(0, Math.max(1, data.length / 2));
    response.data = truncatedData;
    response.truncated = true;
    response.truncation_message =
      `응답이 ${data.length}개에서 ${truncatedData.length}개 항목으로 잘렸습니다. ` +
      `'offset' 매개변수를 사용하거나 필터를 추가하여 더 많은 결과를 확인하세요.`;
    result = JSON.stringify(response, null, 2);
  }

  return result;
}
```

## 오류 처리

명확하고 실행 가능한 오류 메시지를 제공하세요:

```typescript
import axios, { AxiosError } from "axios";

function handleApiError(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.response) {
      switch (error.response.status) {
        case 404:
          return "오류: 리소스를 찾을 수 없습니다. ID가 올바른지 확인하세요.";
        case 403:
          return "오류: 접근이 거부되었습니다. 이 리소스에 대한 권한이 없습니다.";
        case 429:
          return "오류: 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요.";
        default:
          return `오류: API 요청이 상태 코드 ${error.response.status}로 실패했습니다`;
      }
    } else if (error.code === "ECONNABORTED") {
      return "오류: 요청 시간이 초과되었습니다. 다시 시도하세요.";
    }
  }
  return `오류: 예기치 않은 오류가 발생했습니다: ${error instanceof Error ? error.message : String(error)}`;
}
```

## 공유 유틸리티

재사용 가능한 함수로 공통 기능을 추출하세요:

```typescript
// 공유 API 요청 함수
async function makeApiRequest<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  data?: any,
  params?: any
): Promise<T> {
  try {
    const response = await axios({
      method,
      url: `${API_BASE_URL}/${endpoint}`,
      data,
      params,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}
```

## Async/Await 모범 사례

네트워크 요청 및 I/O 작업에 항상 async/await를 사용하세요:

```typescript
// 좋은 예: 비동기 네트워크 요청
async function fetchData(resourceId: string): Promise<ResourceData> {
  const response = await axios.get(`${API_URL}/resource/${resourceId}`);
  return response.data;
}

// 나쁜 예: 프로미스 체인 (읽기 어려움)
function fetchData(resourceId: string): Promise<ResourceData> {
  return axios.get(`${API_URL}/resource/${resourceId}`)
    .then(response => response.data);
}
```

## TypeScript 모범 사례

1. **엄격한 TypeScript 사용**: tsconfig.json에서 strict 모드 활성화
2. **인터페이스 정의**: 모든 데이터 구조에 대한 명확한 인터페이스 정의
3. **`any` 피하기**: `any` 대신 적절한 타입 또는 `unknown` 사용
4. **런타임 검증에 Zod 사용**: 외부 데이터를 검증하는 Zod 스키마 사용
5. **타입 가드**: 복잡한 타입 검사를 위한 타입 가드 함수 생성
6. **오류 처리**: 적절한 오류 타입 검사가 포함된 try-catch 항상 사용
7. **Null 안전성**: 옵셔널 체이닝 (`?.`)과 Nullish 병합 (`??`) 사용

```typescript
// 좋은 예: Zod와 인터페이스를 사용한 타입 안전성
interface UserResponse {
  id: string;
  name: string;
  email: string;
  team?: string;
  active: boolean;
}

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  team: z.string().optional(),
  active: z.boolean()
});

type User = z.infer<typeof UserSchema>;

async function getUser(id: string): Promise<User> {
  const data = await apiCall(`/users/${id}`);
  return UserSchema.parse(data);  // 런타임 검증
}

// 나쁜 예: any 사용
async function getUser(id: string): Promise<any> {
  return await apiCall(`/users/${id}`);  // 타입 안전성 없음
}
```

## 패키지 설정

### package.json

```json
{
  "name": "{서비스}-mcp-server",
  "version": "1.0.0",
  "description": "{서비스} API 통합을 위한 MCP 서버",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "clean": "rm -rf dist"
  },
  "engines": {
    "node": ">=18"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.6.1",
    "axios": "^1.7.9",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^22.10.0",
    "tsx": "^4.19.2",
    "typescript": "^5.7.2"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "allowSyntheticDefaultImports": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## 완전한 예제

```typescript
#!/usr/bin/env node
/**
 * Example 서비스를 위한 MCP 서버.
 *
 * 이 서버는 사용자 검색, 프로젝트 관리, 데이터 내보내기 기능을 포함하여
 * Example API와 상호작용하는 도구를 제공합니다.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import axios, { AxiosError } from "axios";
import express from "express";

// 상수
const API_BASE_URL = "https://api.example.com/v1";
const CHARACTER_LIMIT = 25000;

// 열거형
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

// Zod 스키마
const UserSearchInputSchema = z.object({
  query: z.string()
    .min(2, "쿼리는 최소 2자 이상이어야 합니다")
    .max(200, "쿼리는 200자를 초과할 수 없습니다")
    .describe("이름/이메일 매칭 검색 문자열"),
  limit: z.number().int().min(1).max(100).default(20)
    .describe("반환할 최대 결과 수"),
  offset: z.number().int().min(0).default(0)
    .describe("페이지네이션을 위해 건너뛸 결과 수"),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("출력 형식: 사람이 읽기 위한 'markdown' 또는 기계 처리용 'json'")
}).strict();

type UserSearchInput = z.infer<typeof UserSearchInputSchema>;

// 공유 유틸리티 함수
async function makeApiRequest<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  data?: any,
  params?: any
): Promise<T> {
  const response = await axios({
    method,
    url: `${API_BASE_URL}/${endpoint}`,
    data,
    params,
    timeout: 30000,
    headers: { "Content-Type": "application/json", "Accept": "application/json" }
  });
  return response.data;
}

function handleApiError(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.response) {
      switch (error.response.status) {
        case 404: return "오류: 리소스를 찾을 수 없습니다. ID가 올바른지 확인하세요.";
        case 403: return "오류: 접근이 거부되었습니다. 권한이 없습니다.";
        case 429: return "오류: 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요.";
        default: return `오류: API 요청이 상태 코드 ${error.response.status}로 실패했습니다`;
      }
    } else if (error.code === "ECONNABORTED") {
      return "오류: 요청 시간이 초과되었습니다. 다시 시도하세요.";
    }
  }
  return `오류: 예기치 않은 오류: ${error instanceof Error ? error.message : String(error)}`;
}

// MCP 서버 인스턴스 생성
const server = new McpServer({ name: "example-mcp", version: "1.0.0" });

// 도구 등록
server.registerTool(
  "example_search_users",
  {
    title: "Example 사용자 검색",
    description: `[위에 표시된 전체 설명]`,
    inputSchema: UserSearchInputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true
    }
  },
  async (params: UserSearchInput) => {
    // 위에 표시된 구현
  }
);

// stdio (로컬용):
async function runStdio() {
  if (!process.env.EXAMPLE_API_KEY) {
    console.error("오류: EXAMPLE_API_KEY 환경 변수가 필요합니다");
    process.exit(1);
  }
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP 서버가 stdio로 실행 중입니다");
}

// Streamable HTTP (원격용):
async function runHTTP() {
  if (!process.env.EXAMPLE_API_KEY) {
    console.error("오류: EXAMPLE_API_KEY 환경 변수가 필요합니다");
    process.exit(1);
  }
  const app = express();
  app.use(express.json());
  app.post('/mcp', async (req, res) => {
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true
    });
    res.on('close', () => transport.close());
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  });
  const port = parseInt(process.env.PORT || '3000');
  app.listen(port, () => {
    console.error(`MCP 서버가 http://localhost:${port}/mcp에서 실행 중입니다`);
  });
}

// 환경에 따라 전송 방식 선택
const transport = process.env.TRANSPORT || 'stdio';
if (transport === 'http') {
  runHTTP().catch(error => { console.error("서버 오류:", error); process.exit(1); });
} else {
  runStdio().catch(error => { console.error("서버 오류:", error); process.exit(1); });
}
```

---

## 고급 MCP 기능

### 리소스 등록

URI 기반 접근을 위해 데이터를 리소스로 노출:

```typescript
import { ResourceTemplate } from "@modelcontextprotocol/sdk/types.js";

server.registerResource(
  {
    uri: "file://documents/{name}",
    name: "문서 리소스",
    description: "이름으로 문서 접근",
    mimeType: "text/plain"
  },
  async (uri: string) => {
    const match = uri.match(/^file:\/\/documents\/(.+)$/);
    if (!match) throw new Error("유효하지 않은 URI 형식");
    const content = await loadDocument(match[1]);
    return {
      contents: [{ uri, mimeType: "text/plain", text: content }]
    };
  }
);
```

**리소스 vs 도구 사용 시기:**
- **리소스**: 간단한 URI 기반 매개변수로 데이터 접근
- **도구**: 검증과 비즈니스 로직이 필요한 복잡한 작업

### 알림 지원

서버 상태가 변경될 때 클라이언트에 알림:

```typescript
// 도구 목록 변경 시 알림
server.notification({ method: "notifications/tools/list_changed" });

// 리소스 변경 시 알림
server.notification({ method: "notifications/resources/list_changed" });
```

서버 기능이 실제로 변경될 때만 알림을 사용하세요.

---

## 코드 모범 사례

### 코드 조합성 및 재사용성

구현은 반드시 조합성과 코드 재사용을 우선시해야 합니다:

1. **공통 기능 추출**:
   - 여러 도구에서 사용되는 작업에 재사용 가능한 헬퍼 함수 생성
   - HTTP 요청을 위한 공유 API 클라이언트 구축 (코드 중복 방지)
   - 오류 처리 로직을 유틸리티 함수에 중앙화
   - 조합 가능한 전용 함수에 비즈니스 로직 추출

2. **중복 방지**:
   - 도구 간에 유사한 코드를 복사/붙여넣기 절대 금지
   - 유사한 로직을 두 번 작성하게 된다면 함수로 추출
   - 페이지네이션, 필터링, 필드 선택, 포맷팅은 공유

## 빌드 및 실행

TypeScript 코드를 실행하기 전에 항상 빌드하세요:

```bash
# 프로젝트 빌드
npm run build

# 서버 실행
npm start

# 자동 리로드 개발 모드
npm run dev
```

구현 완료 전에 `npm run build`가 성공적으로 완료되는지 항상 확인하세요.

## 품질 체크리스트

Node/TypeScript MCP 서버 구현 완료 전에 확인하세요:

### 전략적 설계
- [ ] 도구가 단순 API 엔드포인트 래퍼가 아닌 완전한 워크플로우 지원
- [ ] 도구 이름이 자연스러운 작업 세분화를 반영
- [ ] 응답 형식이 에이전트 컨텍스트 효율성에 최적화
- [ ] 오류 메시지가 에이전트를 올바른 사용법으로 안내

### 구현 품질
- [ ] 가장 중요하고 가치 있는 도구 구현
- [ ] 모든 도구가 완전한 설정으로 `registerTool` 사용
- [ ] 모든 도구에 `title`, `description`, `inputSchema`, `annotations` 포함
- [ ] Zod 스키마에 `.strict()` 적용 및 설명적 오류 메시지
- [ ] 도구 설명에 반환 값 예시와 완전한 스키마 문서

### TypeScript 품질
- [ ] 모든 데이터 구조에 TypeScript 인터페이스 정의
- [ ] tsconfig.json에서 strict 모드 활성화
- [ ] `any` 타입 사용 없음
- [ ] 모든 async 함수에 명시적 `Promise<T>` 반환 타입
- [ ] 적절한 타입 가드를 사용한 오류 처리

### 프로젝트 설정
- [ ] package.json에 모든 필요한 의존성 포함
- [ ] 빌드 스크립트가 dist/ 디렉토리에 작동하는 JavaScript 생성
- [ ] 메인 진입점이 dist/index.js로 올바르게 설정
- [ ] 서버 이름이 `{서비스}-mcp-server` 형식을 따름

### 코드 품질
- [ ] 페이지네이션 적절히 구현
- [ ] 대용량 응답이 CHARACTER_LIMIT를 확인하고 명확한 메시지로 잘림
- [ ] 잠재적으로 큰 결과 집합에 필터링 옵션 제공
- [ ] 공통 기능이 재사용 가능한 함수로 추출

### 테스트 및 빌드
- [ ] `npm run build`가 오류 없이 완료
- [ ] dist/index.js 생성 및 실행 가능
- [ ] 모든 임포트가 올바르게 해결
- [ ] 샘플 도구 호출이 예상대로 작동
