'use client'

import { useState } from 'react'
import { X } from 'lucide-react'
import { Sidebar } from './sidebar'
import { TopNav } from './top-nav'
import { cn } from '@/lib/utils'

export function AppShell({ children }: { children: React.ReactNode }) {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <div className="flex min-h-screen bg-background">
      {/* 데스크톱 사이드바 (고정) */}
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 lg:block">
        <Sidebar />
      </aside>

      {/* 모바일 드로어 */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div
            className="absolute inset-0 bg-black/50"
            onClick={() => setMobileOpen(false)}
            aria-hidden
          />
          <div className="absolute inset-y-0 left-0 w-64">
            <button
              type="button"
              onClick={() => setMobileOpen(false)}
              className="absolute -right-10 top-4 rounded-lg p-2 text-white"
              aria-label="메뉴 닫기"
            >
              <X className="size-5" />
            </button>
            <Sidebar onNavigate={() => setMobileOpen(false)} />
          </div>
        </div>
      )}

      {/* 메인 영역 */}
      <div className={cn('flex min-w-0 flex-1 flex-col lg:pl-64')}>
        <TopNav onMenuClick={() => setMobileOpen(true)} />
        <main className="flex-1 px-4 py-6 lg:px-8">
          <div className="mx-auto w-full max-w-[1400px]">{children}</div>
        </main>
      </div>
    </div>
  )
}
