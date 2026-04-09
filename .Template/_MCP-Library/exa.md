# exa MCP

## 용도
Exa AI 기반 시맨틱 웹 검색. 기본 웹서치보다 코드·기술 문서·학술 자료 검색에 특화.
의미 기반 검색으로 관련도 높은 결과 반환.

## 적합한 프로젝트
- 기술 리서치가 필요한 프로젝트
- 최신 정보 수집이 중요한 프로젝트
- 전역 등록 권장

## API 키
**필요** — Exa 대시보드에서 발급
- 발급: https://dashboard.exa.ai/api-keys

## 현재 검증 버전
`exa-mcp-server@latest`

## 설정값 복사

```json
"exa": {
  "type": "stdio",
  "command": "cmd",
  "args": [
    "/c",
    "npx",
    "-y",
    "exa-mcp-server"
  ],
  "env": {
    "EXA_API_KEY": "YOUR_EXA_API_KEY"
  }
}
```

## 주의사항
- API 키를 `.claude.json` 또는 `.mcp.json`에 직접 기재 시 **Git 커밋에 노출 주의**
- `.gitignore`에 해당 파일 포함 여부 반드시 확인

## 업데이트 이력
- 초기 등록: 2025-03-13
