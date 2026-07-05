'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Bell, Boxes, Menu, ChevronDown, LogOut, User, KeyRound } from 'lucide-react'
import { Avatar } from '@/components/ui/avatar'
import { Dropdown, DropdownItem } from '@/components/ui/dropdown'
import { logout, type CurrentUser } from '@/lib/auth'
import { ChangePasswordModal } from './change-password-modal'

interface TopNavProps {
  onMenuClick: () => void
  currentUser: CurrentUser | null
}

export function TopNav({ onMenuClick, currentUser }: TopNavProps) {
  const router = useRouter()
  const [changePasswordOpen, setChangePasswordOpen] = useState(false)
  // 로그인 사용자 본인 이름을 별도로 저장하지 않아(사원-계정 이름 연동은 로드맵 §8 큐
  // 진행 중) 로그인 ID를 표시명으로 대신 사용한다 — 하드코딩된 "관리자"/
  // admin@blueward.co.kr을 실제 로그인 계정 정보로 대체(§9-1 "내 프로필" 화면).
  const displayName = currentUser?.USER_LGID ?? '...'
  const displayEmail = currentUser?.EMAIL_ADDR ?? ''
  const roleLabel = currentUser?.ROLE_NM ?? ''

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

        {roleLabel && (
          <span className="hidden rounded-md bg-nav-active-bg px-2.5 py-1 text-xs font-semibold text-nav-active-text sm:inline-flex">
            {roleLabel}
          </span>
        )}

        <Dropdown
          trigger={
            <span className="flex items-center gap-2 rounded-lg py-1 pl-1 pr-2 transition-colors hover:bg-nav-hover">
              <Avatar name={displayName} className="size-8 bg-white text-nav-active-text" />
              <span className="hidden text-sm font-medium text-nav-foreground sm:inline">
                {displayName}
              </span>
              <ChevronDown className="hidden size-4 text-nav-icon sm:inline" />
            </span>
          }
        >
          <div className="px-2.5 py-2">
            <p className="text-sm font-semibold text-foreground">{displayName}</p>
            <p className="text-xs text-muted-foreground">{displayEmail}</p>
          </div>
          <div className="my-1 h-px bg-border" />
          <DropdownItem onClick={() => router.push('/profile')}>
            <User /> 내 프로필
          </DropdownItem>
          <DropdownItem onClick={() => setChangePasswordOpen(true)}>
            <KeyRound /> 비밀번호 변경
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

      <ChangePasswordModal open={changePasswordOpen} onClose={() => setChangePasswordOpen(false)} />
    </header>
  )
}
