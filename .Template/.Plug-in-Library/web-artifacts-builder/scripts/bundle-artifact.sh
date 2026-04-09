#!/bin/bash
# ============================================================
# [bundle-artifact.sh]
# ====================
# [역할] React 앱을 단일 HTML 아티팩트 파일로 번들링합니다
#
# [주요 기능]
#   - Parcel을 사용하여 프로젝트 빌드
#   - html-inline으로 모든 에셋을 단일 HTML 파일로 인라인 처리
#   - bundle.html 출력 생성 (JavaScript, CSS, 의존성 모두 포함)
#
# [사용법]
#   프로젝트 루트 디렉토리에서 실행:
#   bash scripts/bundle-artifact.sh
#
#   출력: bundle.html (자기 완결형 HTML 아티팩트)
#   이 파일을 Claude 대화에서 아티팩트로 직접 공유할 수 있습니다.
# ============================================================
set -e

echo "📦 React 앱을 단일 HTML 아티팩트로 번들링 중..."

# Check if we're in a project directory
if [ ! -f "package.json" ]; then
  echo "❌ 오류: package.json을 찾을 수 없습니다. 프로젝트 루트에서 이 스크립트를 실행하세요."
  exit 1
fi

# Check if index.html exists
if [ ! -f "index.html" ]; then
  echo "❌ 오류: 프로젝트 루트에서 index.html을 찾을 수 없습니다."
  echo "   이 스크립트는 index.html 진입점이 필요합니다."
  exit 1
fi

# Install bundling dependencies
echo "📦 번들링 의존성 설치 중..."
pnpm add -D parcel @parcel/config-default parcel-resolver-tspaths html-inline

# Create Parcel config with tspaths resolver
if [ ! -f ".parcelrc" ]; then
  echo "🔧 경로 별칭 지원이 포함된 Parcel 설정 생성 중..."
  cat > .parcelrc << 'EOF'
{
  "extends": "@parcel/config-default",
  "resolvers": ["parcel-resolver-tspaths", "..."]
}
EOF
fi

# Clean previous build
echo "🧹 이전 빌드 정리 중..."
rm -rf dist bundle.html

# Build with Parcel
echo "🔨 Parcel로 빌드 중..."
pnpm exec parcel build index.html --dist-dir dist --no-source-maps

# Inline everything into single HTML
echo "🎯 모든 에셋을 단일 HTML 파일로 인라인 처리 중..."
pnpm exec html-inline dist/index.html > bundle.html

# Get file size
FILE_SIZE=$(du -h bundle.html | cut -f1)

echo ""
echo "✅ 번들링 완료!"
echo "📄 출력: bundle.html ($FILE_SIZE)"
echo ""
echo "이 단일 HTML 파일을 Claude 대화에서 아티팩트로 사용할 수 있습니다."
echo "로컬에서 테스트하려면: 브라우저에서 bundle.html을 열어보세요"
