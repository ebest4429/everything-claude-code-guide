# 02. 설치 및 설정

**시스템 요구사항 (Requirements)**

- **OS**: macOS 13.0+, Windows 10 1809+, Ubuntu 20.04+, Debian 10+, Alpine Linux 3.19+
- **RAM**: 4GB 이상
- **네트워크**: 인터넷 연결 필요
- **Shell**: Bash, Zsh, PowerShell, CMD (Windows에서는 Git for Windows 필수)

**설치 방법 (Install)**

- **Windows**: `winget install Anthropic.ClaudeCode`

**인증 및 첫 실행 (Auth)**

- 터미널에서 `claude` 명령어를 입력하여 실행합니다.
- 콘솔에 표시되는 링크를 통해 Anthropic 계정으로 로그인하고 인증 코드를 입력해야 합니다.

**업데이트 (Update)**

- `claude update` 명령어로 수동 업데이트가 가능합니다.
- `DISABLE_AUTOUPDATER: "1"` 환경 변수로 자동 업데이트를 끌 수 있습니다.
