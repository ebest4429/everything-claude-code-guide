import Accordion from '../components/Accordion'
import Card from '../components/Card'

export default function Agents() {
  return (
    <div className="max-w-3xl">
      <h2 className="text-[22px] font-bold text-white mb-2">에이전트 가이드</h2>
      <p className="text-[#888] mb-6">에이전트별 상세 사용법을 안내합니다.</p>

      <div className="grid grid-cols-2 gap-3 mb-6">
        <Card title="executor" description="구현 작업 전담 에이전트" />
        <Card title="architect" description="구조 설계 에이전트" />
        <Card title="debugger" description="버그 분석 에이전트" />
        <Card title="code-reviewer" description="코드 리뷰 에이전트" />
      </div>

      <Accordion title="에이전트란?" defaultOpen>
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="에이전트 목록 전체">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="에이전트 활용 패턴">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
    </div>
  )
}
