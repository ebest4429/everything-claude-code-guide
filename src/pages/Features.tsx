import Accordion from '../components/Accordion'
import Card from '../components/Card'

export default function Features() {
  return (
    <div className="max-w-3xl">
      <h2 className="text-[22px] font-bold text-white mb-2">주요 기능</h2>
      <p className="text-[#888] mb-6">Claude Code의 핵심 기능들을 상세히 소개합니다.</p>

      <div className="grid grid-cols-3 gap-3 mb-6">
        <Card title="에이전트" description="자율 작업 실행" />
        <Card title="훅(Hooks)" description="이벤트 기반 자동화" />
        <Card title="MCP 서버" description="외부 도구 연동" />
        <Card title="스킬" description="재사용 가능한 프롬프트" />
        <Card title="메모리" description="컨텍스트 유지" />
        <Card title="멀티 에이전트" description="병렬 작업 처리" />
      </div>

      <Accordion title="에이전트 상세" defaultOpen>
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="훅(Hooks) 상세">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="MCP 서버 상세">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="스킬 상세">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="메모리 상세">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
    </div>
  )
}
