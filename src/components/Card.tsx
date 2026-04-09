interface Props {
  title: string
  description?: string
  children?: React.ReactNode
  onClick?: () => void
}

export default function Card({ title, description, children, onClick }: Props) {
  return (
    <div
      onClick={onClick}
      className={`bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5 ${
        onClick
          ? 'cursor-pointer hover:border-[#7c3aed] hover:bg-[#1f1a2e] transition-colors duration-150'
          : ''
      }`}
    >
      <h3 className="text-[16px] font-semibold text-white mb-1">{title}</h3>
      {description && (
        <p className="text-[13px] text-[#888] mb-3 leading-relaxed">{description}</p>
      )}
      {children}
    </div>
  )
}
