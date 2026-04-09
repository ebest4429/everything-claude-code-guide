# gmail MCP

## 용도
Gmail 읽기/쓰기/검색 자동화. Claude가 직접 메일 조회, 작성, 발송 가능.

## 적합한 프로젝트
- 이메일 자동화 프로젝트
- 메일 기반 업무 처리
- **전역보다 특정 프로젝트 로컬 등록 권장**

## API 키
**필요** — Google OAuth2 클라이언트 자격증명
- 발급: https://console.cloud.google.com → API 및 서비스 → 사용자 인증 정보

## 현재 검증 버전
`@gongrzhe/server-gmail-autoauth-mcp@latest`

## 설정값 복사

```json
"gmail": {
  "command": "cmd",
  "args": [
    "/c",
    "npx",
    "-y",
    "@gongrzhe/server-gmail-autoauth-mcp"
  ],
  "env": {
    "GOOGLE_CLIENT_ID": "YOUR_CLIENT_ID",
    "GOOGLE_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
    "GOOGLE_REDIRECT_URI": "http://localhost:3000/oauth2callback"
  }
}
```

## 주의사항
- OAuth 최초 실행 시 브라우저 인증 필요
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` 절대 Git 노출 금지
- claude.ai Gmail MCP와 **중복 등록 시 충돌 가능** → 둘 중 하나만 사용

## 대안
claude.ai 연동 Gmail MCP (Claude Desktop에서 인증) 사용 시 이 파일 불필요

## 업데이트 이력
- 초기 등록: 2025-03-13
