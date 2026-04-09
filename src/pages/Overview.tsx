import Accordion from '../components/Accordion'
import Card from '../components/Card'

export default function Overview() {
  return (
    <div className="max-w-3xl">
      <h2 className="text-[22px] font-bold text-white mb-2">개요</h2>
      <p className="text-[#888] mb-6">Claude Code란 무엇인지, 특징과 장점을 소개합니다.</p>

      <div className="grid grid-cols-2 gap-3 mb-6">
        <Card title="Claude Code란?" description="Anthropic이 만든 CLI 기반 AI 코딩 도구" />
        <Card title="주요 특징" description="에이전트, 훅, MCP, 스킬 등 확장 가능한 구조" />
      </div>

      <Accordion title="Claude Code 소개" defaultOpen>
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="다른 도구와의 차이점">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
    </div>
  )
}
