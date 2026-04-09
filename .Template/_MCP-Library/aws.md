# aws MCP (awslabs.aws-api-mcp-server)

## 용도
AWS 서비스 API 직접 호출. S3, EC2, Lambda, DynamoDB 등 AWS 리소스 조회 및 관리.
Claude가 AWS CLI 수준의 작업을 직접 수행 가능.

## 적합한 프로젝트
- AWS 인프라 관리 프로젝트
- 서버리스 아키텍처 프로젝트
- 클라우드 리소스 자동화

## API 키
**필요** — AWS IAM Access Key
- 발급: AWS Console → IAM → 사용자 → 보안 자격증명 → 액세스 키 생성
- 필요 권한: 작업 범위에 맞는 최소 권한 IAM 정책 적용

## 현재 검증 버전
`awslabs.aws-api-mcp-server@latest`
- `uvx` 실행 방식 (pip 기반, npx와 다름)
- Python 환경 필요

## 설정값 복사

```json
"awslabs.aws-api-mcp-server": {
  "command": "uvx",
  "args": [
    "--from",
    "awslabs.aws-api-mcp-server@latest",
    "awslabs.aws-api-mcp-server"
  ],
  "env": {
    "AWS_REGION": "ap-northeast-2",
    "AWS_ACCESS_KEY_ID": "YOUR_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY": "YOUR_SECRET_ACCESS_KEY"
  }
}
```

## 주의사항
- `uvx` 실행 → **Python + uv 패키지 매니저 설치 필요**
  - 설치: `pip install uv` 또는 `winget install astral-sh.uv`
- AWS 리전 기본값: `ap-northeast-2` (서울) — 필요에 따라 변경
- IAM 키는 **최소 권한 원칙** 적용 필수
- 액세스 키 Git 노출 절대 금지 → `.gitignore`에 `.mcp.json` 추가 권장
- Windows에서 `uvx.exe` 경로 문제 발생 시 전체 경로 지정 필요

## Windows 호환 버전

```json
"awslabs.aws-api-mcp-server": {
  "command": "cmd",
  "args": [
    "/c",
    "uvx",
    "--from",
    "awslabs.aws-api-mcp-server@latest",
    "awslabs.aws-api-mcp-server.exe"
  ],
  "env": {
    "AWS_REGION": "ap-northeast-2",
    "AWS_ACCESS_KEY_ID": "YOUR_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY": "YOUR_SECRET_ACCESS_KEY"
  }
}
```

## 업데이트 이력
- 초기 등록: 2025-03-13
