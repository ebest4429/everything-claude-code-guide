# 08. MCP 서버

Model Context Protocol(MCP)을 통해 외부 도구와 데이터를 Claude Code에 통합합니다.

## 주요 기능

- **도구(Tools)**: Claude가 실행할 수 있는 함수(예: Google Search, SQL Query)
- **리소스(Resources)**: Claude가 읽을 수 있는 데이터(예: 로드된 파일, API 문서)
- **프롬프트(Prompts)**: 재사용 가능한 템플릿

## MCP 서버 관리 명령어

- `/mcp list`: 현재 활성화된 MCP 서버 목록 확인
- `/mcp get <name>`: 특정 서버의 상세 정보 및 사용 가능한 도구 확인
- `/mcp remove <name>`: MCP 서버 제거

## 설정 파일 구조

`claude.json` 파일 내에 `mcpServers` 객체를 정의하여 서버를 구성합니다.

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everything"]
    }
  }
}
```
