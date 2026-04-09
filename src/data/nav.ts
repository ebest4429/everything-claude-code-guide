export interface NavItem {
  label: string
  path: string
  description: string
}

export const mainNavItems: NavItem[] = [
  { label: '개요', path: '/overview', description: 'Claude Code란? 특징과 장점' },
  { label: '설치', path: '/install', description: 'Claude CLI 설치 및 IDE 연동' },
  { label: '사용법', path: '/usage', description: '기본 사용법과 주요 워크플로우' },
  { label: '주요 기능', path: '/features', description: '에이전트, 훅, MCP, 스킬, 메모리' },
  { label: '메뉴별 소개', path: '/menus', description: '슬래시 커맨드, 설정 메뉴 상세' },
]

export const detailNavItems: NavItem[] = [
  { label: '스킬 가이드', path: '/skills', description: '스킬별 상세 사용법' },
  { label: '에이전트 가이드', path: '/agents', description: '에이전트별 상세 사용법' },
]
