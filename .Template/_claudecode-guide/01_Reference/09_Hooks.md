# 09. 훅 (Hooks)

특정 이벤트가 발생할 때 자동으로 실행되는 스크립트를 정의합니다.

## 주요 이벤트 유형

- **pre-task**: 작업 시작 전 실행
- **post-task**: 작업 완료 후 실행
- **on-error**: 오류 발생 시 실행

## 설정 예시

```json
{
  "hooks": {
    "pre-task": "echo 'Starting new task...'",
    "post-task": "git status"
  }
}
```

## 활용 사례

- 작업 전 의존성 체크
- 완료 후 테스트 자동 실행
- 빌드 결과물 정리 및 알림 송신
