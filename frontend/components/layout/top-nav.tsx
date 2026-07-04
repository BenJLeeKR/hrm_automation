'use client'

import { useRouter } from 'next/navigation'
import { Bell, Boxes, Menu, ChevronDown, LogOut, User, Settings } from 'lucide-react'
import { Avatar } from '@/components/ui/avatar'
import { Dropdown, DropdownItem } from '@/components/ui/dropdown'
import { logout } from '@/lib/auth'

interface TopNavProps {
  onMenuClick: () => void
}

export function TopNav({ onMenuClick }: TopNavProps) {
  const router = useRouter()

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-3 border-b border-nav-border bg-nav px-4 text-nav-foreground lg:px-6">
      <button
        type="button"
        onClick={onMenuClick}
        className="rounded-lg p-2 text-nav-icon transition-colors hover:bg-nav-hover hover:text-nav-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-nav-accent lg:hidden"
        aria-label="메뉴 열기"
      >
        <Menu className="size-5" />
      </button>

      {/* 로고 — 기존 사이드바에서 제거한 아이콘+텍스트를 그대로 옮겨왔다 */}
      <div className="flex items-center gap-2.5">
        <div className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-white text-nav-active-text">
          <Boxes className="size-5" />
        </div>
        <span className="hidden text-sm font-semibold text-nav-foreground sm:inline">
          HRM 자동화 시스템(Resource Mgmt)
        </span>
      </div>

      <div className="ml-auto flex items-center gap-2 sm:gap-3">
        <button
          type="button"
          className="relative rounded-lg p-2 text-nav-icon transition-colors hover:bg-nav-hover hover:text-nav-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-nav-accent"
          aria-label="알림"
        >
          <Bell className="size-5" />
          <span className="absolute right-1.5 top-1.5 size-2 rounded-full bg-nav-accent" />
        </button>

        <span className="hidden rounded-md bg-nav-active-bg px-2.5 py-1 text-xs font-semibold text-nav-active-text sm:inline-flex">
          시스템 관리자
        </span>

        <Dropdown
          trigger={
            <span className="flex items-center gap-2 rounded-lg py-1 pl-1 pr-2 transition-colors hover:bg-nav-hover">
              <Avatar name="관리자" className="size-8 bg-white text-nav-active-text" />
              <span className="hidden text-sm font-medium text-nav-foreground sm:inline">
                관리자
              </span>
              <ChevronDown className="hidden size-4 text-nav-icon sm:inline" />
            </span>
          }
        >
          <div className="px-2.5 py-2">
            <p className="text-sm font-semibold text-foreground">관리자</p>
            <p className="text-xs text-muted-foreground">admin@blueward.co.kr</p>
          </div>
          <div className="my-1 h-px bg-border" />
          <DropdownItem onClick={() => router.push('/settings/users')}>
            <User /> 내 프로필
          </DropdownItem>
          <DropdownItem onClick={() => router.push('/settings')}>
            <Settings /> 설정
          </DropdownItem>
          <div className="my-1 h-px bg-border" />
          <DropdownItem
            onClick={() => {
              void logout().then(() => router.push('/login'))
            }}
            className="text-destructive hover:bg-destructive/10 [&_svg]:text-destructive"
          >
            <LogOut /> 로그아웃
          </DropdownItem>
        </Dropdown>
      </div>
    </header>
  )
}
