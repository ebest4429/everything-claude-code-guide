# magic-21st MCP (@21st-dev/magic)

## 용도
21st.dev Magic UI 생성 도구. AI 기반 UI 컴포넌트 자동 생성.
프롬프트로 React 컴포넌트를 즉시 생성하는 "UI Copilot" 역할.

## 적합한 프로젝트
- 빠른 UI 프로토타이핑
- React 프론트엔드 프로젝트
- 디자인 시스템 구축 초기 단계

## API 키
**필요** — 21st.dev 계정에서 발급
- 발급: https://21st.dev → 계정 설정 → API Keys

## 현재 검증 버전
`@21st-dev/magic@latest`

## 설정값 복사

```json
"magic": {
  "command": "npx",
  "args": [
    "-y",
    "@21st-dev/magic@latest"
  ],
  "env": {
    "MAGIC_API_KEY": "YOUR_MAGIC_API_KEY"
  }
}
```

## cmd 래퍼 적용 버전 (Windows 권장)

```json
"magic": {
  "command": "cmd",
  "args": [
    "/c",
    "npx",
    "-y",
    "@21st-dev/magic@latest"
  ],
  "env": {
    "MAGIC_API_KEY": "YOUR_MAGIC_API_KEY"
  }
}
```

## 주의사항
- shadcn MCP, magicui MCP와 함께 사용 시 UI 생성 커버리지 최대화
- API 키 Git 노출 주의

## 유사 MCP 비교

| MCP | 특징 |
|-----|------|
| shadcn | shadcn/ui 컴포넌트 설치/조회 |
| magicui | Magic UI 애니메이션 컴포넌트 |
| magic (이 파일) | AI로 UI 컴포넌트 직접 생성 |

## 업데이트 이력
- 초기 등록: 2025-03-13
