# github MCP

## 용도
GitHub 저장소 조회, 이슈 생성/관리, PR 생성, 코드 검색 자동화.
Claude가 직접 GitHub API와 상호작용 가능.

## 적합한 프로젝트
- GitHub 기반 협업 프로젝트
- 이슈/PR 자동화가 필요한 프로젝트
- CI/CD 워크플로우 관리

## API 키
**필요** — GitHub Personal Access Token
- 발급: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- 필요 권한: `repo`, `issues`, `pull_requests`

## 현재 검증 버전
`@modelcontextprotocol/server-github@latest`

## 설정값 복사

```json
"github": {
  "command": "cmd",
  "args": [
    "/c",
    "npx",
    "-y",
    "@modelcontextprotocol/server-github"
  ],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_TOKEN"
  }
}
```

## 주의사항
- Token 권한은 **최소 필요 범위만** 부여 (보안 원칙)
- Token 만료일 설정 권장 (무기한 토큰 지양)
- `.mcp.json` Git 커밋 시 토큰 노출 절대 금지

## 업데이트 이력
- 초기 등록: 2025-03-13
