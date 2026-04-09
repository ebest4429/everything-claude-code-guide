import { NavLink } from 'react-router-dom'
import { mainNavItems, detailNavItems } from '../data/nav'
import type { NavItem } from '../data/nav'

interface Props {
  searchQuery: string
}

export default function Sidebar({ searchQuery }: Props) {
  const q = searchQuery.toLowerCase()

  const filter = (items: NavItem[]) =>
    q
      ? items.filter(
          i =>
            i.label.toLowerCase().includes(q) ||
            i.description.toLowerCase().includes(q)
        )
      : items

  const filteredMain = filter(mainNavItems)
  const filteredDetail = filter(detailNavItems)
  const hasResults = filteredMain.length > 0 || filteredDetail.length > 0

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `flex flex-col px-4 py-3 rounded-lg mx-2 mb-1 transition-colors duration-150 ${
      isActive
        ? 'bg-[#7c3aed] text-white'
        : 'text-[#a0a0a0] hover:bg-[#1e1e1e] hover:text-[#e5e5e5]'
    }`

  return (
    <nav className="flex-1 overflow-y-auto py-4">
      {filteredMain.map(item => (
        <NavLink key={item.path} to={item.path} className={linkClass}>
          <span className="text-[15px] font-medium leading-snug">{item.label}</span>
          <span className="text-xs text-[#666] mt-0.5 leading-tight">{item.description}</span>
        </NavLink>
      ))}

      {filteredDetail.length > 0 && (
        <>
          <div className="mx-4 my-3 border-t border-[#2a2a2a]" />
          {filteredDetail.map(item => (
            <NavLink key={item.path} to={item.path} className={linkClass}>
              <span className="text-[15px] font-medium leading-snug">{item.label}</span>
              <span className="text-xs text-[#666] mt-0.5 leading-tight">{item.description}</span>
            </NavLink>
          ))}
        </>
      )}

      {!hasResults && (
        <p className="px-6 text-[#555] text-sm">검색 결과 없음</p>
      )}
    </nav>
  )
}
