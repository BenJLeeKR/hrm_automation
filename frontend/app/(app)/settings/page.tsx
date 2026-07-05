'use client'

import { useState } from 'react'
import { PageHeader } from '@/components/common/page-header'
import { Card, CardContent } from '@/components/ui/card'
import { Tabs } from '@/components/ui/tabs'
import { UsersTable } from '@/components/settings/users-table'
import { AuditLogTable } from '@/components/settings/audit-log-table'
import { NotificationSettingsForm } from '@/components/settings/notification-settings'

export default function SettingsPage() {
  const [tab, setTab] = useState('USERS')

  return (
    <div>
      <PageHeader
        title="설정"
        description="사용자 계정, 감사 로그, 알림 채널을 관리합니다."
      />

      <div className="mb-6">
        <Tabs
          value={tab}
          onValueChange={setTab}
          tabs={[
            { value: 'USERS', label: '사용자 관리' },
            { value: 'AUDIT', label: '감사 로그' },
            { value: 'NOTIFICATION', label: '알림 채널' },
          ]}
        />
      </div>

      {tab === 'USERS' && (
        <Card>
          <CardContent className="pt-6">
            <UsersTable />
          </CardContent>
        </Card>
      )}

      {tab === 'AUDIT' && (
        <Card>
          <CardContent className="pt-6">
            <AuditLogTable />
          </CardContent>
        </Card>
      )}

      {tab === 'NOTIFICATION' && <NotificationSettingsForm />}
    </div>
  )
}
