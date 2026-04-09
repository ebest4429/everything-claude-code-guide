# 템플릿 예시: Image-Source-Download (참조용)

이 파일은 과거 프로젝트(`Image-Source-Download`)를 기준으로 작성된 예시입니다. 템플릿 사용 시 참고용으로만 활용하십시오.

## 1. 프로젝트 정보

- **프로젝트 명**: Image-Source-Download
- **목적**: 웹 페이지에서 이미지 소스를 추출하고 로컬로 일괄 다운로드하는 도구.

## 2. 기술 스택

- **Framework**: Next.js (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Tools**: `ytdl-core` (영상 추출 시 활용), `fs` (로컬 저장)

## 3. 프로젝트 구조 (예시)

- `/app/api/download/`: 다운로드 로직 수행 API
- `/components/`: UI 컴포넌트
- `/lib/utils/`: 공통 유틸리티 함수

## 4. 에이전트 역할 분담

- **Claude CLI**: 이미지 추출 알고리즘 구현 및 에러 처리 로직 작성.
- **Antigravity**: 다운로드 완료 후 파일 리스트 정리, 사용 가이드(`README_KR.md`) 작성, 작업 로그 기록.
