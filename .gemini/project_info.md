# 프로젝트 기본 설계 가이드 (Template)

새로운 프로젝트 시작 시 이 파일을 복사하여 실제 내용으로 채워 넣으십시오.

## 1. 프로젝트 정보 (Project Overview)

- **프로젝트 명**: [이름을 입력하세요]
- **목적**: [프로젝트의 핵심 달성 목표]
- **주요 사용자**: [누구를 위한 프로젝트인가]

## 2. 기술 스택 (Tech Stack)

- **Frontend**: [예: Next.js, React, Tailwind CSS]
- **Backend/API**: [예: Node.js, Express, MCP Servers]
- **Database**: [예: SQLite, Prisma]
- **Infrastructure**: [예: Cloudflare Tunnel, Vercel]

## 3. 핵심 규칙 (Core Rules)

- **코드 스타일**: [예: Prettier 설정, ESLint 규칙]
- **문서화 원칙**: 본 프로젝트의 모든 주요 결정 사항은 `/.gemini/docs/main_plan.md`에 기록되어야 함.
- **보안**: API Key 및 개인 정보는 반드시 `.env`에서 관리하고 Git에 포함하지 않음.

## 4. 디렉토리 구조 (Directory Structure)

- `/.gemini/`: Antigravity 에이전트 설정 및 문서
- `/.claude/`: Claude CLI 전용 설정
- `/app/`: 메인 어플리케이션 로직
- `/public/`: 정적 에셋

## 5. 검증 및 테스트 (Verification)

- **테스트 도구**: [예: Jest, Playwright]
- **검증 절차**: 구현 완료 후 반드시 `main_walkthrough.md`를 통해 사용자 승인을 득함.

## 6. 기타 특이사항 (Others)

- [기타 프로젝트 고유의 제약 사항이나 참고 사항]
