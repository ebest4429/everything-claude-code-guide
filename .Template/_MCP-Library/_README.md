# MCP 라이브러리

필요할 때 `.mcp.json`에 복사해서 사용하는 MCP 설정 보관함.

---

## 파일 목록

| 파일 | MCP 이름 | API 키 | 용도 요약 |
|------|----------|--------|-----------|
| `sequential-thinking.md` | sequential-thinking | 불필요 | 단계적 추론, 복잡한 문제 분해 |
| `context7.md` | context7 | 불필요 | 라이브러리 최신 공식 문서 실시간 제공 |
| `memory.md` | memory | 불필요 | 세션 간 장기 기억 저장 |
| `exa.md` | exa | **필요** | 시맨틱 웹 검색 |
| `gmail.md` | gmail | **필요** | Gmail 읽기/쓰기 자동화 |
| `shadcn.md` | shadcn | 불필요 | shadcn/ui 컴포넌트 관리 |
| `github.md` | github | **필요** | GitHub 이슈/PR/코드 관리 |
| `notion.md` | notionApi | **필요** | Notion 페이지/DB 연동 |
| `puppeteer.md` | puppeteer | 불필요 | 웹 브라우저 자동화, 스크래핑 |
| `magicui.md` | @magicuidesign/mcp | 불필요 | Magic UI 컴포넌트 연동 |
| `youtube.md` | youtube | **필요** | YouTube 영상 검색, 자막 추출 |
| `magic-21st.md` | magic | **필요** | AI 기반 UI 컴포넌트 자동 생성 |
| `aws.md` | awslabs.aws-api-mcp-server | **필요** | AWS 서비스 API 직접 호출 |
| `image-gen.md` | image-gen | **필요** | Google Gemini 이미지 생성 |

---

## 사용 방법

1. 필요한 MCP의 `.md` 파일 열기
2. `## 설정값 복사` 섹션의 JSON 코드 블록 복사
3. 프로젝트의 `.mcp.json` → `"mcpServers"` 안에 붙여넣기
4. API 키 필요 시 `YOUR_XXX_KEY` 부분을 실제 키로 교체

---

## 프로젝트 유형별 추천 조합

### 프론트엔드 프로젝트
```
context7 + shadcn + magicui + magic-21st
```

### 데이터 수집/크롤링 프로젝트
```
puppeteer + exa + youtube (해당 시)
```

### 백엔드/인프라 프로젝트
```
github + aws
```

### 문서/협업 프로젝트
```
notion + gmail + memory
```

### 범용 (모든 프로젝트 기본)
```
sequential-thinking + context7 + memory
→ 단, sequential-thinking과 memory는 전역(.claude.json) 등록 권장
```

---

## 주의사항

- API 키가 포함된 `.mcp.json`은 **절대 Git 커밋 금지**
- `.gitignore`에 `.mcp.json` 추가 권장
- Windows 환경에서 `command: "npx"` 직접 호출 시 오류 발생하면 `cmd /c` 래퍼 버전 사용

---

*마지막 업데이트: 2025-03-13*
