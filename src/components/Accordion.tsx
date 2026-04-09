import { useState } from 'react'

interface Props {
  title: string
  children: React.ReactNode
  defaultOpen?: boolean
}

export default function Accordion({ title, children, defaultOpen = false }: Props) {
  const [open, setOpen] = useState(defaultOpen)

  return (
    <div className="border border-[#2a2a2a] rounded-lg mb-3 overflow-hidden">
      <button
        onClick={() => setOpen(prev => !prev)}
        className="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-[#1a1a1a] transition-colors duration-150"
      >
        <span className="text-[16px] font-semibold text-white">{title}</span>
        <span
          className={`text-[#555] text-xs transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
        >
          ▼
        </span>
      </button>
      {open && (
        <div className="px-5 py-4 border-t border-[#2a2a2a] text-[14px] text-[#a0a0a0] leading-relaxed">
          {children}
        </div>
      )}
    </div>
  )
}
