import Accordion from '../components/Accordion'

export default function Menus() {
  return (
    <div className="max-w-3xl">
      <h2 className="text-[22px] font-bold text-white mb-2">메뉴별 소개</h2>
      <p className="text-[#888] mb-6">슬래시 커맨드, 설정 메뉴 등 각 메뉴를 상세히 안내합니다.</p>

      <Accordion title="슬래시 커맨드 (/)" defaultOpen>
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="설정 메뉴">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="키보드 단축키">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
      <Accordion title="퍼미션 시스템">
        <p>콘텐츠 준비 중...</p>
      </Accordion>
    </div>
  )
}
