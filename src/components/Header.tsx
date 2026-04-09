interface Props {
  searchQuery: string
  onSearchChange: (value: string) => void
}

export default function Header({ searchQuery, onSearchChange }: Props) {
  return (
    <header className="h-[90px] flex-shrink-0 flex items-center px-6 gap-6 border-b border-[#2a2a2a] bg-[#0f0f0f]">
      <h1 className="text-[18px] font-bold text-white whitespace-nowrap tracking-tight">
        everything-claude-code
      </h1>
      <div className="flex-1 max-w-sm">
        <input
          type="search"
          value={searchQuery}
          onChange={e => onSearchChange(e.target.value)}
          placeholder="메뉴 검색..."
          className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-4 py-2 text-sm text-[#e5e5e5] placeholder-[#555] focus:outline-none focus:border-[#7c3aed] transition-colors duration-150"
        />
      </div>
    </header>
  )
}
