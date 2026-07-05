'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { apiGet, apiPut, apiPost, ApiError } from '@/lib/api'

// 백엔드 알림 채널 설정 API(SCR-017, `app/api/v1/settings_notification.py`) 응답/요청
// 타입 — 필드명은 `app/schemas/sys_config.py`와 동일하게 유지한다. `smtp_password`는
// 값이 있으면 "*****"로 마스킹되어 내려온다.
interface NotificationSettings {
  teams_webhook_url: string
  smtp_host: string
  smtp_port: string
  smtp_user: string
  smtp_password: string
  email_from: string
}

const MASK = '*****'

export function NotificationSettingsForm() {
  const [settings, setSettings] = useState<NotificationSettings | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [saveMessage, setSaveMessage] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)
  const [testMessage, setTestMessage] = useState<Record<string, string>>({})
  const [testing, setTesting] = useState<Record<string, boolean>>({})

  async function reload() {
    setError(null)
    try {
      setSettings(await apiGet<NotificationSettings>('/api/v1/settings/notification'))
    } catch (err) {
      setError(err instanceof ApiError ? err.message : '알림 채널 설정을 불러오지 못했습니다.')
    }
  }

  useEffect(() => {
    reload()
  }, [])

  function update<K extends keyof NotificationSettings>(key: K, value: NotificationSettings[K]) {
    setSettings((prev) => (prev ? { ...prev, [key]: value } : prev))
  }

  async function handleSave() {
    if (!settings) return
    setSaving(true)
    setSaveMessage(null)
    setError(null)
    try {
      // 비밀번호 필드가 마스킹 값("*****") 그대로면 변경 의도가 없는 것으로 보고 전송하지
      // 않는다 — 서버가 필드를 생략(None) 취급해 기존 암호화 값을 유지한다.
      const payload = {
        ...settings,
        smtp_password: settings.smtp_password === MASK ? undefined : settings.smtp_password,
      }
      const result = await apiPut<NotificationSettings>('/api/v1/settings/notification', payload)
      setSettings(result)
      setSaveMessage('알림 채널 설정이 저장되었습니다.')
    } catch (err) {
      setError(err instanceof ApiError ? err.message : '저장에 실패했습니다.')
    } finally {
      setSaving(false)
    }
  }

  async function handleTest(channel: 'teams' | 'email') {
    setTesting((prev) => ({ ...prev, [channel]: true }))
    setTestMessage((prev) => ({ ...prev, [channel]: '' }))
    try {
      const result = await apiPost<{ sent: boolean; message: string }>(
        '/api/v1/settings/notification/test',
        { channel },
      )
      setTestMessage((prev) => ({ ...prev, [channel]: result.message }))
    } catch (err) {
      setTestMessage((prev) => ({
        ...prev,
        [channel]: err instanceof ApiError ? err.message : '발송 실패: 알 수 없는 오류',
      }))
    } finally {
      setTesting((prev) => ({ ...prev, [channel]: false }))
    }
  }

  if (error && !settings) {
    return <p className="text-sm text-destructive">{error}</p>
  }
  if (!settings) {
    return <p className="text-sm text-muted-foreground">불러오는 중...</p>
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Teams 알림</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="teams-webhook-url">Webhook URL</Label>
            <Input
              id="teams-webhook-url"
              value={settings.teams_webhook_url}
              placeholder="https://outlook.office.com/webhook/..."
              onChange={(e) => update('teams_webhook_url', e.target.value)}
            />
          </div>
          <Separator />
          <div className="flex flex-col items-end gap-1">
            <Button variant="outline" disabled={testing.teams} onClick={() => handleTest('teams')}>
              테스트 발송
            </Button>
            {testMessage.teams && <p className="text-xs text-muted-foreground">{testMessage.teams}</p>}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>이메일 알림 (SMTP)</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="smtp-host">SMTP 호스트</Label>
            <Input id="smtp-host" value={settings.smtp_host} onChange={(e) => update('smtp_host', e.target.value)} />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="smtp-port">SMTP 포트</Label>
            <Input
              id="smtp-port"
              type="number"
              value={settings.smtp_port}
              placeholder="587"
              onChange={(e) => update('smtp_port', e.target.value)}
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="smtp-user">SMTP 사용자 ID</Label>
            <Input id="smtp-user" value={settings.smtp_user} onChange={(e) => update('smtp_user', e.target.value)} />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="smtp-password">SMTP 비밀번호</Label>
            <Input
              id="smtp-password"
              type="password"
              value={settings.smtp_password}
              onChange={(e) => update('smtp_password', e.target.value)}
            />
            <p className="text-xs text-muted-foreground">비밀번호는 암호화 저장됩니다. 빈칸으로 두면 기존 값이 유지됩니다.</p>
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="email-from">발신 이메일</Label>
            <Input
              id="email-from"
              type="email"
              value={settings.email_from}
              onChange={(e) => update('email_from', e.target.value)}
            />
          </div>
          <Separator />
          <div className="flex flex-col items-end gap-1">
            <Button variant="outline" disabled={testing.email} onClick={() => handleTest('email')}>
              테스트 발송
            </Button>
            {testMessage.email && <p className="text-xs text-muted-foreground">{testMessage.email}</p>}
          </div>
        </CardContent>
      </Card>

      <div className="col-span-full flex flex-col items-end gap-1">
        {error && <p className="text-sm text-destructive">{error}</p>}
        {saveMessage && <p className="text-sm text-muted-foreground">{saveMessage}</p>}
        <Button disabled={saving} onClick={handleSave}>
          저장
        </Button>
      </div>
    </div>
  )
}
