# 13. CI/CD 통합

엔터프라이즈 환경에서의 배포와 자동화를 위한 가이드입니다.

## 엔터프라이즈 배포 개요

- **API 키 관리**: 가상 환경 및 팀 단위에서의 보안 권한 설정.
- **비용 및 청구**: 사용량 모니터링 및 한도 설정.
- **SSO 연동**: 기업용 계정 통합.

## 배포 옵션 (BYOM - Bring Your Own Model)

- **AWS Bedrock**: AWS 인프라 내에서의 모델 연동.
- **Google Vertex AI**: GCP 환경에서의 통합.
- **Azure AI Foundry**: MS Azure 모델 활용.

## GitHub Actions 통합

`anthropic/claude-code-action`을 사용하여 CI 파이프라인에서 자동 코드 리뷰를 수행합니다.

## 보안 및 네트워크

- **Safe CI Permissions**: CI 환경용 제한적 권한 구성.
- **프록시 설정**: `HTTPS_PROXY` 환경 변수를 통한 사내망 연동.
