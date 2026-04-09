# notion MCP

## 용도
Notion 페이지 읽기/쓰기/검색 자동화.
Claude가 직접 Notion 데이터베이스 조회, 페이지 생성, 내용 업데이트 가능.

## 적합한 프로젝트
- Notion 기반 문서 관리 프로젝트
- 회의록, 작업 일지 자동화
- 데이터베이스 기반 정보 관리

## API 키
**필요** — Notion Integration Token
- 발급: https://www.notion.so/my-integrations → New integration
- 생성 후 사용할 페이지/DB에 Integration 연결 필수

## 현재 검증 버전
`@notionhq/notion-mcp-server@latest`

## 설정값 복사

```json
"notionApi": {
  "command": "npx",
  "args": [
    "-y",
    "@notionhq/notion-mcp-server"
  ],
  "env": {
    "NOTION_TOKEN": "YOUR_NOTION_TOKEN"
  }
}
```

## 주의사항
- `command`가 `npx` 직접 호출 (cmd /c 래퍼 없음) — Windows 환경에서 PATH 설정 확인 필요
- 필요한 페이지에만 Integration 연결 권장 (전체 워크스페이스 접근 지양)
- claude.ai Notion MCP 사용 중이라면 **중복 등록 주의**

## 대안
Claude Desktop의 claude.ai Notion MCP 인증 사용 시 이 파일 불필요

## 업데이트 이력
- 초기 등록: 2025-03-13
