'use client'

import { useState } from 'react'
import { PageHeader } from '@/components/common/page-header'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs } from '@/components/ui/tabs'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { UsersTable } from '@/components/settings/users-table'
import { AuditLogTable } from '@/components/settings/audit-log-table'

const OVER_ALLOC_OPTIONS = [
  { value: 'WARN', label: '경고 표시' },
  { value: 'BLOCK', label: '배정 차단' },
  { value: 'OFF', label: '미사용' },
]

export default function SettingsPage() {
  const [tab, setTab] = useState('GENERAL')
  const [orgName, setOrgName] = useState('비더블유웨어(주)')
  const [threshold, setThreshold] = useState('100')
  const [overAlloc, setOverAlloc] = useState('WARN')

  return (
    <div>
      <PageHeader
        title="설정"
        description="시스템 정책, 사용자 계정, 감사 로그를 관리합니다."
      />

      <div className="mb-6">
        <Tabs
          value={tab}
          onValueChange={setTab}
          tabs={[
            { value: 'GENERAL', label: '일반 설정' },
            { value: 'USERS', label: '사용자 관리' },
            { value: 'AUDIT', label: '감사 로그' },
          ]}
        />
      </div>

      {tab === 'GENERAL' && (
        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>조직 정보</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="org-name">회사명</Label>
                <Input
                  id="org-name"
                  value={orgName}
                  onChange={(e) => setOrgName(e.target.value)}
                />
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="org-domain">이메일 도메인</Label>
                <Input id="org-domain" defaultValue="bwware.co.kr" />
              </div>
              <Separator />
              <div className="flex justify-end">
                <Button>저장</Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>가동률 정책</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="threshold">공수 초과 기준 (%)</Label>
                <Input
                  id="threshold"
                  type="number"
                  value={threshold}
                  onChange={(e) => setThreshold(e.target.value)}
                />
                <p className="text-xs text-muted-foreground">
                  투입률 합계가 이 값을 초과하면 초과 배정으로 판정합니다.
                </p>
              </div>
              <div className="flex flex-col gap-1.5">
                <Label>초과 배정 처리 방식</Label>
                <Select
                  value={overAlloc}
                  onValueChange={setOverAlloc}
                  options={OVER_ALLOC_OPTIONS}
                />
              </div>
              <Separator />
              <div className="flex justify-end">
                <Button>저장</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

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
    </div>
  )
}
