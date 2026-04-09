import { useState, useRef, useCallback } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'

const MIN_WIDTH = 180
const MAX_WIDTH = 420
const DEFAULT_WIDTH = 260

export default function Layout() {
  const [sidebarWidth, setSidebarWidth] = useState(DEFAULT_WIDTH)
  const [searchQuery, setSearchQuery] = useState('')
  const isResizing = useRef(false)

  const startResize = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    isResizing.current = true

    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing.current) return
      setSidebarWidth(Math.min(Math.max(e.clientX, MIN_WIDTH), MAX_WIDTH))
    }

    const handleMouseUp = () => {
      isResizing.current = false
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }

    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
  }, [])

  return (
    <div className="flex h-screen bg-[#0f0f0f] overflow-hidden select-none">
      {/* 사이드바 */}
      <div
        style={{ width: sidebarWidth }}
        className="flex-shrink-0 flex flex-col bg-[#141414] border-r border-[#2a2a2a] overflow-hidden"
      >
        <Sidebar searchQuery={searchQuery} />
      </div>

      {/* 리사이즈 핸들 */}
      <div
        onMouseDown={startResize}
        className="w-1 flex-shrink-0 cursor-col-resize bg-transparent hover:bg-[#7c3aed] transition-colors duration-150"
      />

      {/* 메인 영역 */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header searchQuery={searchQuery} onSearchChange={setSearchQuery} />
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
