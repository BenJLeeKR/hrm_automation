'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Boxes } from 'lucide-react'
import { cn } from '@/lib/utils'
import { mainNav, bottomNav } from '@/lib/nav'

interface SidebarProps {
  onNavigate?: () => void
}

export function Sidebar({ onNavigate }: SidebarProps) {
  const pathname = usePathname()

  function isActive(href: string) {
    if (href === '/dashboard') return pathname === href
    return pathname === href || pathname.startsWith(href + '/')
  }

  return (
    <div className="flex h-full flex-col bg-nav text-nav-foreground">
      {/* 로고 */}
      <div className="flex h-16 shrink-0 items-center gap-2.5 px-5">
        <div className="flex size-8 items-center justify-center rounded-lg bg-white text-nav-active-text">
          <Boxes className="size-5" />
        </div>
        <div className="leading-tight">
          <p className="text-sm font-semibold">HRM 자동화</p>
          <p className="text-[10px] text-nav-muted">Resource Mgmt</p>
        </div>
      </div>

      {/* 메인 메뉴 */}
      <nav className="flex-1 overflow-y-auto scrollbar-thin px-3 py-2">
        <ul className="flex flex-col gap-1">
          {mainNav.map((item) => {
            const active = isActive(item.href)
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  onClick={onNavigate}
                  aria-current={active ? 'page' : undefined}
                  className={cn(
                    'relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors',
                    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-nav-accent focus-visible:ring-offset-2 focus-visible:ring-offset-nav',
                    active
                      ? 'bg-nav-active-bg font-semibold text-nav-active-text shadow-md shadow-black/10'
                      : 'text-nav-foreground hover:bg-nav-hover',
                  )}
                >
                  {active && (
                    <span
                      aria-hidden
                      className="absolute left-0 top-1/2 h-6 w-1 -translate-y-1/2 rounded-r-full bg-nav-accent"
                    />
                  )}
                  <item.icon
                    className={cn(
                      'size-[18px] shrink-0',
                      active ? 'text-nav-active-text' : 'text-nav-icon',
                    )}
                  />
                  <span>{item.label}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>

      {/* 하단 메뉴 */}
      <div className="shrink-0 border-t border-nav-border px-3 py-3">
        <ul className="flex flex-col gap-1">
          {bottomNav.map((item) => (
            <li key={item.label}>
              <Link
                href={item.href}
                onClick={onNavigate}
                className="flex items-center gap-3 rounded-xl px-3 py-2 text-sm text-nav-foreground transition-colors hover:bg-nav-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-nav-accent focus-visible:ring-offset-2 focus-visible:ring-offset-nav"
              >
                <item.icon className="size-[18px] shrink-0 text-nav-icon" />
                <span>{item.label}</span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
