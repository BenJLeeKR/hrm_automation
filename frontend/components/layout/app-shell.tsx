'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { X } from 'lucide-react'
import { Sidebar } from './sidebar'
import { TopNav } from './top-nav'
import { cn } from '@/lib/utils'
import { isAuthenticated, getMe, requiresPasswordChange, type CurrentUser } from '@/lib/auth'

export function AppShell({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const [mobileOpen, setMobileOpen] = useState(false)
  // MVP 임시 인증 가드 — JWT API 연동 전까지 localStorage 세션 마커로 대체 (lib/auth.ts 참조).
  // 실제 서비스 전환 시 서버 미들웨어/세션 기반 검증으로 교체 필요.
  const [checked, setChecked] = useState(false)
  // 권한별 메뉴 제어(로드맵 §8) — `/auth/me`로 현재 사용자의 PERM_JSON을 조회해 사이드바에
  // 전달한다. 조회 실패 시 `null`로 두어 Sidebar가 전체 메뉴를 노출하도록 한다(권한 조회
  // 실패가 곧 메뉴 숨김으로 이어지지 않게 하기 위함 — 실제 접근 제어는 각 API의 RBAC가 담당).
  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(null)

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace('/login')
      return
    }
    // 임시 비밀번호 상태(PWD_CHG_YN=TRUE)면 URL을 직접 입력해 들어와도 다른 화면을 보지
    // 못하도록 비밀번호 변경 화면으로 강제 이동시킨다(설계서 §5.3.9, §8 큐 1-5). `/login`과
    // 동일하게 `(app)` 레이아웃 밖에 있는 `/change-password` 자체는 이 가드 대상이 아니다.
    if (requiresPasswordChange()) {
      router.replace('/change-password')
      return
    }
    setChecked(true)
    getMe().then(setCurrentUser)
  }, [router])

  if (!checked) return null

  return (
    <div className="flex min-h-screen bg-background">
      {/* 데스크톱 사이드바 (고정) */}
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 lg:block">
        <Sidebar permJson={currentUser?.PERM_JSON ?? null} />
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
            <Sidebar permJson={currentUser?.PERM_JSON ?? null} onNavigate={() => setMobileOpen(false)} />
          </div>
        </div>
      )}

      {/* 메인 영역 */}
      <div className={cn('flex min-w-0 flex-1 flex-col lg:pl-64')}>
        <TopNav onMenuClick={() => setMobileOpen(true)} currentUser={currentUser} />
        <main className="flex-1 px-4 py-6 lg:px-8">
          <div className="mx-auto w-full max-w-[1400px]">{children}</div>
        </main>
      </div>
    </div>
  )
}
