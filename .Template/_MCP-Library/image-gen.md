# image-gen MCP

## 용도
Google Gemini API 기반 이미지 생성. Claude가 직접 이미지 생성 요청 가능.
텍스트 프롬프트로 이미지 생성 및 저장.

## 적합한 프로젝트
- 이미지 에셋 자동 생성이 필요한 프로젝트
- 콘텐츠 제작 자동화
- 프로토타입 UI 목업 이미지 생성

## API 키
**필요** — Google AI Studio (Gemini) API 키
- 발급: https://aistudio.google.com/app/apikey

## 현재 검증 버전
`image-generation-mcp@latest`

## 설정값 복사

```json
"image-gen": {
  "command": "npx",
  "args": [
    "-y",
    "image-generation-mcp"
  ],
  "env": {
    "GOOGLE_API_KEY": "YOUR_GOOGLE_API_KEY"
  }
}
```

## cmd 래퍼 적용 버전 (Windows 권장)

```json
"image-gen": {
  "command": "cmd",
  "args": [
    "/c",
    "npx",
    "-y",
    "image-generation-mcp"
  ],
  "env": {
    "GOOGLE_API_KEY": "YOUR_GOOGLE_API_KEY"
  }
}
```

## 주의사항
- Gemini 이미지 생성은 **무료 티어 한도** 존재 — 대량 생성 시 비용 발생
- 생성된 이미지 저장 경로 사전 확인 필요
- API 키 Git 노출 주의

## 업데이트 이력
- 초기 등록: 2025-03-13
