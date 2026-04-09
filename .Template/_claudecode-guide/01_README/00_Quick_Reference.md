# 00. 퀵 레퍼런스

## 시작하기 (Quick Start)

설치 → 진입 → 파악 → 규칙 설정. 5분이면 끝.

### 설치

`curl -fsSL https://claude.ai/install.sh | bash`

### 프로젝트에서 시작

`cd my-project`
`claude`

1. 먼저 프로젝트 파악: "프로젝트 구조 설명해줘"
2. 그다음 CLAUDE.md 생성 - 프로젝트 규칙을 파일로 저장: `/init`

## 매일 쓰는 시나리오 (Daily Use)

사용 빈도순: 세 글자만 기억: `/ (명령 또는 스킬)`, `! (셸 명령)`, `@ (파일 지정)`
_Claude Code는 짧게 말해도 알아듣지만, 명확할수록 결과가 좋다._

---

## 1. 코드 이해하기

- **짧게**: "이 프로젝트 뭐야", "프로젝트 구조 설명해줘"
- **파일 지정 (TS/Python/Go)**: "@src/hooks/useAuth.ts 이거 뭐하는 거야", "@app/models/user.py 모델 관계 설명해줘", "@internal/handler/auth.go 미들웨어 흐름 알려줘"
- **추적**: "login 함수 어디서 호출해?", "API 엔드포인트 전부 정리해줘", "인증 처리 흐름을 프론트엔드부터 DB까지 추적해줘"
- **길게**: "UserService의 git 히스토리 보고 이 API가 왜 이렇게 됐는지 설명해줘", "인증 시스템 아키텍처 분석하고 개선점 제안해줘"

## 2. 버그 잡기

- **에러 메시지 그대로 붙여넣기**: "이 에러 고쳐줘: TypeError: Cannot read property 'id' of undefined at UserService.getProfile (src/services/user.ts:42)"
- **테스트 기반**:
  - `!npm test` (JS/TS)
  - `!pytest -x` (Python)
  - `!go test ./...` (Go)
  - "실패한 테스트 고쳐줘, 테스트 코드는 건드리지 마"
- **위치 알 때**: "@src/api/user.ts 42번째 줄 null 에러 고쳐"
- **구체적으로**: "빌드가 이 에러로 실패해: [에러]. 근본 원인을 해결하고 빌드 성공을 확인해줘"

## 3. Claude 다루기

- **방향 전환**: "그거 말고 ...로 해" (또는 `Ctrl+C`)
- **과잉 수정 방지**: "요청한 부분만 수정해", "다른 파일 건드리지 마"
- **중간 확인**: "멈춰, 변경사항 보여줘"
- **되돌리기**: `Esc+Esc` + 되돌아감(rewind) 위치 선택
- **기존 패턴 따르게 하기**: "기존 코드 스타일 따라서 해줘", "홈페이지의 기존 위젯 구현 방식을 보고, 동일한 패턴으로 캘린더 위젯을 만들어줘"

## 4. 기능 만들기

- **한 줄이면 되는 것**: "로그아웃 버튼 추가해줘", "다크 모드 토글 넣어줘"
- **파일 지정 + 패턴 따르기**: "@src/api/users.ts에 프로필 수정 API 추가해줘. 기존 패턴 따라서", "@app/views.py에 비밀번호 변경 엔드포인트 추가. 다른 뷰 패턴 따라서"
- **큰 기능**: `/plan`, "OAuth2 로그인 추가하고 싶어", 계획 확인 -> `Shift+Tab`으로 Normal 전환 -> 구현
- **TDD**: "테스트 먼저 짜고, 통과할 때까지 구현해"
- **구체적 지시**: "validateEmail 함수 작성해줘. user@example.com -> true, invalid -> false. 테스트도 작성하고 실행해줘"

## 5. 리팩토링 & 테스트

- **범위 제한**: "@src/utils/helpers.ts ES2024 문법으로 리팩토링. 테스트 돌려서 확인하고", "@src/types/ 중복 타입 정리. 다른 파일 건드리지 마"
- **테스트 작성**: "@src/services/auth.ts 테스트 작성해줘", "@app/services/auth.py에서 로그아웃 사용자 엣지 케이스 테스트 작성. mock은 피해줘"
- **테스트 돌리고 수정**: `!npm test`, `!pytest`, `!go test`. "실패하는 거 고쳐"

## 6. 커밋 & 리뷰

- **커밋**: `/commit` 또는 `/c`, "커밋!"
- **푸시**: "커밋하고 푸시"
- **리뷰**: `/review`, "리뷰해줘", "git diff main @src/middleware/rateLimiter.ts 리뷰해줘. 레이스 컨디션 확인해줘"
- **PR**: "PR 만들어줘"
