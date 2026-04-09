# 07. 키보드 단축키

Claude Code는 터미널 기반이므로 모든 조작을 키보드로 수행할 수 있습니다.

## 일반 제어 (General)

- **Ctrl+C**: 현재 작업 취소 또는 입력 내용 삭제
- **Ctrl+D**: Claude Code 종료 (EOF)
- **Ctrl+L**: 터미널 화면 지우기
- **Ctrl+U**: (Bash 모드) 현재 줄 삭제 및 Bash 모드 종료

## 텍스트 편집 (Editing)

- **방향키**: 커서 이동
- **Home / End**: 줄의 처음/끝으로 이동
- **Ctrl+A / Ctrl+E**: 줄의 처음/끝으로 이동 (macOS/Linux 스타일)
- **Backspace / Delete**: 문자 삭제
- **Ctrl+W**: 단어 단위 삭제
- **Ctrl+K**: 커서 이후 내용 삭제

## 멀티라인 입력 (Multiline)

- **Option+Enter** (또는 Alt+Enter): 줄바꿈 (새 줄 추가)
- **Ctrl+Enter**: 메시지 전송 (멀티라인 모드에서)

## Vim 모드

설정에서 Vim 모드를 활성화하면 익숙한 키 바인딩을 사용할 수 있습니다.

- **Normal 모드**: `Esc`로 진입하여 이동 및 편집
- **Insert 모드**: `i`, `a`, `o` 등으로 진입

## 커스텀 키바인딩 (Custom Keybindings)

`~/.claude.json` 또는 프로젝트별 `.claude.json` 파일의 `keybindings` 섹션에서 단축키를 직접 정의할 수 있습니다.
