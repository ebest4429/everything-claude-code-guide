import Accordion from '../components/Accordion'

export default function Usage() {
  return (
    <div className="max-w-3xl">
      <h2 className="text-[22px] font-bold text-white mb-2">사용법</h2>
      <p className="text-[#888] mb-6">기본 사용법과 주요 워크플로우를 안내합니다.</p>

      <Accordion title="첫 실행" defaultOpen>
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="대화 방식">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="파일 작업">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="코드 작업">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
    </div>
  )
}
