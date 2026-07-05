'use client'

import { useEffect, useState } from 'react'
import { PageHeader } from '@/components/common/page-header'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { apiGet, apiPatch, ApiError } from '@/lib/api'

// 백엔드 `GET/PATCH /api/v1/auth/me`(`app/api/v1/auth.py`, §9-1 "내 프로필" 화면) 응답
// 타입 — 필드명은 `app/schemas/auth.py`의 `MeOut`과 동일하게 유지한다.
interface MeOut {
  USER_ID: string
  USER_LGID: string
  EMAIL_ADDR: string
  ROLE_CD: string
  ROLE_NM: string
}

export default function ProfilePage() {
  const [me, setMe] = useState<MeOut | null>(null)
  const [email, setEmail] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [saveMessage, setSaveMessage] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  async function reload() {
    setError(null)
    try {
      const result = await apiGet<MeOut>('/api/v1/auth/me')
      setMe(result)
      setEmail(result.EMAIL_ADDR)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : '내 프로필 정보를 불러오지 못했습니다.')
    }
  }

  useEffect(() => {
    reload()
  }, [])

  async function handleSave() {
    setSaving(true)
    setSaveMessage(null)
    setError(null)
    try {
      const result = await apiPatch<MeOut>('/api/v1/auth/me', { EMAIL_ADDR: email })
      setMe(result)
      setSaveMessage('내 정보가 저장되었습니다.')
    } catch (err) {
      setError(err instanceof ApiError ? err.message : '저장에 실패했습니다.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div>
      <PageHeader title="내 프로필" description="로그인 계정의 기본 정보를 조회·수정합니다." />

      {error && !me && <p className="text-sm text-destructive">{error}</p>}

      {me && (
        <Card className="max-w-xl">
          <CardHeader>
            <CardTitle>계정 정보</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="profile-login-id">로그인 ID</Label>
              <Input id="profile-login-id" value={me.USER_LGID} disabled />
              <p className="text-xs text-muted-foreground">로그인 ID는 수정할 수 없습니다.</p>
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="profile-role">역할</Label>
              <Input id="profile-role" value={me.ROLE_NM} disabled />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="profile-email">이메일</Label>
              <Input
                id="profile-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <Separator />
            <div className="flex flex-col items-end gap-1">
              {error && <p className="text-sm text-destructive">{error}</p>}
              {saveMessage && <p className="text-sm text-muted-foreground">{saveMessage}</p>}
              <Button disabled={saving} onClick={handleSave}>
                저장
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
