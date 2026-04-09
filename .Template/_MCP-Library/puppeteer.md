# puppeteer MCP

## 용도
Chromium 브라우저 자동화. 웹 스크래핑, 스크린샷 캡처, 폼 자동 입력, SPA 크롤링.
JavaScript 렌더링이 필요한 동적 페이지 처리 가능.

## 적합한 프로젝트
- 웹 스크래핑/크롤링 프로젝트
- 자동화 테스트
- 웹 데이터 수집 (부동산, 상권 데이터 등)
- Image-Source-Download, Youtube-WebDown 류 프로젝트

## API 키
불필요

## 현재 검증 버전
`@modelcontextprotocol/server-puppeteer@latest`

## 설정값 복사

```json
"puppeteer": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-puppeteer"
  ]
}
```

## 주의사항
- `command`가 `npx` 직접 호출 — Windows 환경에서 필요 시 `cmd /c` 래퍼 추가
- Chromium 첫 실행 시 자동 다운로드 (수백 MB) — 시간 소요
- 헤드리스 환경(서버)에서는 추가 설정 필요할 수 있음

## cmd 래퍼 적용 버전 (Windows 권장)

```json
"puppeteer": {
  "command": "cmd",
  "args": [
    "/c",
    "npx",
    "-y",
    "@modelcontextprotocol/server-puppeteer"
  ]
}
```

## 업데이트 이력
- 초기 등록: 2025-03-13
