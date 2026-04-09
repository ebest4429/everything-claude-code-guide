# sequential-thinking MCP

## 용도
복잡한 문제를 단계별로 분해해 순차적으로 추론. 다단계 계획, 로직 설계, 복잡한 디버깅 시 자동 활용.

## 적합한 프로젝트
- 복잡한 알고리즘 설계
- 멀티스텝 워크플로우 구현
- 아키텍처 설계
- 모든 프로젝트 범용 적용 가능

## API 키
불필요

## 현재 검증 버전
`@latest` — 공식 Anthropic 패키지, 버전 고정 불필요

## 설정값 복사

```json
"sequential-thinking": {
  "type": "stdio",
  "command": "cmd",
  "args": [
    "/c",
    "npx",
    "-y",
    "@modelcontextprotocol/server-sequential-thinking"
  ],
  "env": {},
  "disabled": false
}
```

## 주의사항
- `"disabled": false` 명시 — 필요시 `true`로 임시 비활성화 가능
- Thinking mode와 함께 사용 시 추론 품질 극대화

## 업데이트 이력
- 초기 등록: 2025-03-13
