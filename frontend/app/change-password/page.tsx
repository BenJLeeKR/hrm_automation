'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Boxes, Lock, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { apiPost, ApiError } from '@/lib/api'
import { isAuthenticated, requiresPasswordChange, clearPasswordChangeRequirement } from '@/lib/auth'

// 최초 로그인 강제 비밀번호 변경 화면 (설계서 §5.3.9 "PWD_CHG_YN", §8 큐 1-5) — 사용자
// 요청에 따라 기존 "비밀번호 변경" 모달(§9-1, `components/layout/change-password-modal.tsx`)
// 대신 로그인 화면(`app/login/page.tsx`)과 동일한 전체 화면 스타일로 구현한다. 자율적
// 비밀번호 변경(모달)과 백엔드 API(`POST /api/v1/auth/change-password`)는 동일하게 재사용.
export default function ChangePasswordPage() {
  const router = useRouter()
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace('/login')
      return
    }
    // 강제 변경 대상이 아닌데(URL 직접 접근 등) 들어온 경우 대시보드로 돌려보낸다.
    if (!requiresPasswordChange()) {
      router.replace('/dashboard')
    }
  }, [router])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')

    if (!currentPassword.trim()) {
      setError('임시 비밀번호를 입력하세요.')
      return
    }
    if (newPassword !== confirmPassword) {
      setError('새 비밀번호가 일치하지 않습니다.')
      return
    }

    setLoading(true)
    try {
      await apiPost('/api/v1/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      })
      clearPasswordChangeRequirement()
      router.push('/dashboard')
    } catch (err) {
      setError(err instanceof ApiError ? err.message : '비밀번호 변경 중 오류가 발생했습니다. 잠시 후 다시 시도하세요.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-nav px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center text-center">
          <div className="mb-4 flex size-14 items-center justify-center rounded-lg bg-primary text-primary-foreground shadow-lg">
            <Boxes className="size-7" />
          </div>
          <h1 className="text-2xl font-bold text-nav-foreground">
            비밀번호 변경이 필요합니다
          </h1>
          <p className="mt-1 text-sm text-nav-muted">
            임시 비밀번호로 로그인했습니다. 계속하려면 새 비밀번호를 설정하세요.
          </p>
        </div>

        <div className="rounded-xl border border-border bg-card p-6 shadow-2xl">
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <label htmlFor="currentPassword" className="text-xs font-medium text-foreground/80">
                임시 비밀번호
              </label>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  id="currentPassword"
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="••••••••"
                  className="pl-9"
                  autoComplete="current-password"
                />
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <label htmlFor="newPassword" className="text-xs font-medium text-foreground/80">
                새 비밀번호
              </label>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  id="newPassword"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="8자 이상, 영문+숫자+특수문자"
                  className="pl-9"
                  autoComplete="new-password"
                />
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <label htmlFor="confirmPassword" className="text-xs font-medium text-foreground/80">
                새 비밀번호 확인
              </label>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••"
                  className="pl-9"
                  autoComplete="new-password"
                />
              </div>
            </div>

            {error && (
              <div className="flex items-center gap-2 rounded-lg bg-[#fde8e8] px-3 py-2 text-xs text-[#c0392b]">
                <AlertCircle className="size-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <Button type="submit" size="lg" className="mt-1 w-full" disabled={loading}>
              {loading ? '변경 중입니다...' : '비밀번호 변경'}
            </Button>
          </form>
        </div>

        <p className="mt-6 text-center text-xs text-nav-muted">
          © 2025 Blueward. All rights reserved.
        </p>
      </div>
    </div>
  )
}
