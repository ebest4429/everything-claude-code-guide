# 14. CLI 레퍼런스

Claude Code CLI에서 사용할 수 있는 모든 명령어와 설정 옵션입니다.

## 주요 명령어 (Commands)

- `claude`: 상호작용 모드 시작
- `claude "질문"`: 일회성 실행 (One-shot)
- `claude --model <name>`: 특정 모델 지정
- `claude --json`: 결과를 JSON 형식으로 출력

## 환경 변수 (Environment Variables)

- `ANTHROPIC_API_KEY`: 인증을 위한 API 키
- `CLAUDE_CODE_USE_GCP`: GCP 연동 활성화 여부
- `HTTPS_PROXY`: 네트워크 프록시 서버 주소

## 실무 조합 예시

```bash
# 특정 파일에 대한 코드 리뷰 수행
cat main.py | claude "이 코드의 버그를 찾아줘" --one-shot
```
