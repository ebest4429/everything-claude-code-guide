---
name: web-artifacts-builder
description: React, Tailwind CSS, shadcn/ui 등 최신 프론트엔드 웹 기술을 활용하여 복잡하고 다중 컴포넌트로 구성된 claude.ai HTML 아티팩트를 생성하는 도구 모음. 상태 관리, 라우팅, shadcn/ui 컴포넌트가 필요한 복잡한 아티팩트에 적합하며, 단순한 단일 파일 HTML/JSX 아티팩트에는 사용하지 않음.
license: 전체 조건은 LICENSE.txt 참조
---

# Web Artifacts Builder

강력한 claude.ai 프론트엔드 아티팩트를 구축하려면 다음 단계를 따르세요:
1. `scripts/init-artifact.sh`를 사용하여 프론트엔드 저장소를 초기화합니다
2. 생성된 코드를 편집하여 아티팩트를 개발합니다
3. `scripts/bundle-artifact.sh`를 사용하여 모든 코드를 단일 HTML 파일로 번들링합니다
4. 사용자에게 아티팩트를 표시합니다
5. (선택사항) 아티팩트를 테스트합니다

**스택**: React 18 + TypeScript + Vite + Parcel (번들링) + Tailwind CSS + shadcn/ui

## 디자인 및 스타일 가이드라인

매우 중요: 종종 "AI 슬롭(AI slop)"이라 불리는 것을 피하려면, 과도한 중앙 정렬 레이아웃, 보라색 그라데이션, 균일한 둥근 모서리, Inter 폰트 사용을 지양하세요.

## 빠른 시작

### 1단계: 프로젝트 초기화

초기화 스크립트를 실행하여 새 React 프로젝트를 생성합니다:
```bash
bash scripts/init-artifact.sh <프로젝트명>
cd <프로젝트명>
```

생성되는 프로젝트에는 다음이 포함됩니다:
- ✅ React + TypeScript (Vite 기반)
- ✅ shadcn/ui 테마 시스템이 포함된 Tailwind CSS 3.4.1
- ✅ 경로 별칭(`@/`) 설정 완료
- ✅ 40개 이상의 shadcn/ui 컴포넌트 사전 설치
- ✅ 모든 Radix UI 의존성 포함
- ✅ 번들링을 위한 Parcel 설정 (.parcelrc 포함)
- ✅ Node 18+ 호환성 (Vite 버전 자동 감지 및 고정)

### 2단계: 아티팩트 개발

아티팩트를 빌드하려면 생성된 파일을 편집하세요. 자세한 내용은 아래 **일반적인 개발 작업**을 참고하세요.

### 3단계: 단일 HTML 파일로 번들링

React 앱을 단일 HTML 아티팩트로 번들링하려면:
```bash
bash scripts/bundle-artifact.sh
```

`bundle.html`이 생성됩니다 — 모든 JavaScript, CSS, 의존성이 인라인으로 포함된 독립 실행형 아티팩트입니다. 이 파일은 Claude 대화에서 아티팩트로 직접 공유할 수 있습니다.

**요구사항**: 프로젝트 루트 디렉토리에 `index.html`이 있어야 합니다.

**스크립트 동작 내용**:
- 번들링 의존성 설치 (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- 경로 별칭 지원이 포함된 `.parcelrc` 설정 생성
- Parcel로 빌드 (소스 맵 없음)
- html-inline을 사용하여 모든 에셋을 단일 HTML로 인라인 처리

### 4단계: 사용자와 아티팩트 공유

마지막으로, 사용자가 아티팩트로 볼 수 있도록 번들링된 HTML 파일을 대화에서 공유하세요.

### 5단계: 아티팩트 테스트/시각화 (선택사항)

참고: 완전히 선택적인 단계입니다. 필요하거나 요청이 있을 때만 수행하세요.

아티팩트를 테스트/시각화하려면 사용 가능한 도구(다른 Skills 또는 Playwright, Puppeteer 같은 내장 도구 포함)를 활용하세요. 일반적으로 아티팩트 완성 후 사용자에게 보여주기 전에 미리 테스트하는 것은 지연을 유발하므로 피하세요. 요청이 있거나 문제가 발생한 경우 아티팩트 제시 후에 테스트하세요.

## 참고 자료

- **shadcn/ui 컴포넌트**: https://ui.shadcn.com/docs/components
