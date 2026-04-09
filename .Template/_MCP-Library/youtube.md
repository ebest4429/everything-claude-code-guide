# youtube MCP

## 용도
YouTube Data API 연동. 영상 검색, 메타데이터 조회, 자막(트랜스크립트) 추출.
Claude가 직접 YouTube 콘텐츠 분석 가능.

## 적합한 프로젝트
- Youtube-WebDown 프로젝트
- 영상 콘텐츠 분석/정리 프로젝트
- 자막 기반 요약, 번역 작업

## API 키
**필요** — Google YouTube Data API v3 키
- 발급: https://console.cloud.google.com → API 및 서비스 → YouTube Data API v3 활성화

## 현재 검증 버전
`youtube-data-mcp-server@latest`

## 설정값 복사

```json
"youtube": {
  "command": "npx",
  "args": [
    "-y",
    "youtube-data-mcp-server"
  ],
  "env": {
    "YOUTUBE_API_KEY": "YOUR_YOUTUBE_API_KEY",
    "YOUTUBE_TRANSCRIPT_LANG": "ko"
  }
}
```

## cmd 래퍼 적용 버전 (Windows 권장)

```json
"youtube": {
  "command": "cmd",
  "args": [
    "/c",
    "npx",
    "-y",
    "youtube-data-mcp-server"
  ],
  "env": {
    "YOUTUBE_API_KEY": "YOUR_YOUTUBE_API_KEY",
    "YOUTUBE_TRANSCRIPT_LANG": "ko"
  }
}
```

## 주의사항
- YouTube Data API는 **일일 할당량(Quota)** 존재 — 대량 요청 시 한도 초과 주의
- `YOUTUBE_TRANSCRIPT_LANG`: `ko` (한국어), `en` (영어) 등 언어 코드 지정

## 업데이트 이력
- 초기 등록: 2025-03-13
