'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Boxes, Lock, User, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { login } from '@/lib/auth'

export default function LoginPage() {
  const router = useRouter()
  const [loginId, setLoginId] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')

    if (!loginId.trim()) {
      setError('로그인 ID를 입력하세요.')
      return
    }
    if (!password.trim()) {
      setError('비밀번호를 입력하세요.')
      return
    }

    setLoading(true)
    const result = await login(loginId, password)
    setLoading(false)

    if (!result.ok) {
      setError(result.error ?? '로그인에 실패했습니다.')
      return
    }
    // 임시 비밀번호 상태(PWD_CHG_YN=TRUE)면 다른 화면으로 보내지 않고 비밀번호 변경
    // 화면으로 강제 이동시킨다(설계서 §5.3.9, §8 큐 1-5).
    router.push(result.pwdChgYn ? '/change-password' : '/dashboard')
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-nav px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center text-center">
          <div className="mb-4 flex size-14 items-center justify-center rounded-lg bg-primary text-primary-foreground shadow-lg">
            <Boxes className="size-7" />
          </div>
          <h1 className="text-2xl font-bold text-nav-foreground">
            HRM 자동화 시스템
          </h1>
          <p className="mt-1 text-sm text-nav-muted">
            인력 리소스 관리 자동화 플랫폼
          </p>
        </div>

        <div className="rounded-xl border border-border bg-card p-6 shadow-2xl">
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <label htmlFor="loginId" className="text-xs font-medium text-foreground/80">
                로그인 ID
              </label>
              <div className="relative">
                <User className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  id="loginId"
                  value={loginId}
                  onChange={(e) => setLoginId(e.target.value)}
                  placeholder="admin"
                  className="pl-9"
                  autoComplete="username"
                />
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <label htmlFor="password" className="text-xs font-medium text-foreground/80">
                비밀번호
              </label>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="pl-9"
                  autoComplete="current-password"
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
              {loading ? '로그인 중입니다...' : '로그인'}
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
