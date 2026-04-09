import Accordion from '../components/Accordion'

export default function Install() {
  return (
    <div className="max-w-3xl">
      <h2 className="text-[22px] font-bold text-white mb-2">설치</h2>
      <p className="text-[#888] mb-6">Claude CLI 설치 방법과 IDE 연동 가이드입니다.</p>

      <Accordion title="Claude CLI 설치" defaultOpen>
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="Antigravity IDE 연동">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="기타 IDE 연동">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
    </div>
  )
}
