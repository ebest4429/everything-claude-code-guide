# shadcn MCP

## 용도
shadcn/ui 컴포넌트 설치, 조회, 문서 참조 자동화.
Claude가 직접 컴포넌트 목록 확인 및 설치 명령 실행 가능.

## 적합한 프로젝트
- shadcn/ui 기반 프론트엔드 프로젝트
- React + Tailwind CSS 프로젝트
- **전역 등록 비권장 — 프론트엔드 프로젝트 로컬에만 추가**

## API 키
불필요

## 현재 검증 버전
`shadcn@latest` — 버전 고정 시 shadcn 업데이트와 불일치 가능, latest 유지 권장

## 설정값 복사

```json
"shadcn": {
  "command": "cmd",
  "args": [
    "/c",
    "npx",
    "-y",
    "shadcn@latest",
    "mcp"
  ]
}
```

## 주의사항
- 비프론트엔드 프로젝트에 등록 시 불필요한 컨텍스트 부하 발생
- `@latest`로 인한 초기 로딩 지연 있을 수 있음

## 업데이트 이력
- 초기 등록: 2025-03-13
