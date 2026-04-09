import Accordion from '../components/Accordion'
import Card from '../components/Card'

export default function Skills() {
  return (
    <div className="max-w-3xl">
      <h2 className="text-[22px] font-bold text-white mb-2">스킬 가이드</h2>
      <p className="text-[#888] mb-6">스킬별 상세 사용법을 안내합니다.</p>

      <div className="grid grid-cols-2 gap-3 mb-6">
        <Card title="analyze" description="데이터 분석 스킬" />
        <Card title="build-dashboard" description="대시보드 생성 스킬" />
        <Card title="skill-creator" description="스킬 생성·개선 스킬" />
        <Card title="translate-plugin" description="플러그인 번역 스킬" />
      </div>

      <Accordion title="스킬이란?" defaultOpen>
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="스킬 목록 전체">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="커스텀 스킬 만들기">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
    </div>
  )
}
