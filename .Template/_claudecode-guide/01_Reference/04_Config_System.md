# 04. 설정 시스템

**설정 파일 위치**

- **사용자(Global)**: `~/.claude-code/settings.json`
- **프로젝트(Local)**: `./.claude-code/settings.json`

**설정 우선순위**

- 관리자(System) > 프로젝트(Local) > 사용자(Global)

**주요 설정 항목**

- `permissions`: 각 도구(Bash, FileSystem 등)에 대한 허용/거부 규칙.
- `env`: 세션 내에서 사용할 환경 변수.
- `sandboxPathPrefix`: 접근 디렉토리 범위 제한.
