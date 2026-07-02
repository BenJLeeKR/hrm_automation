'use client'

import { useMemo, useState } from 'react'
import { UserPlus } from 'lucide-react'
import { SearchInput } from '@/components/common/search-input'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { RoleBadge } from '@/components/common/status-badge'
import { ModalForm } from '@/components/common/modal-form'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { systemUsers } from '@/lib/mock-data'
import { userRoleOptions, userStatusOptions } from '@/lib/options'
import type { RoleCode } from '@/lib/types'

const roleFormOptions = userRoleOptions.filter((o) => o.value !== 'ALL')

export function UsersTable() {
  const [keyword, setKeyword] = useState('')
  const [role, setRole] = useState('ALL')
  const [status, setStatus] = useState('ALL')
  const [openCreate, setOpenCreate] = useState(false)
  const [newLoginId, setNewLoginId] = useState('')
  const [newEmail, setNewEmail] = useState('')
  const [newRole, setNewRole] = useState<string>('VIEWER')

  const filtered = useMemo(
    () =>
      systemUsers.filter((u) => {
        if (role !== 'ALL' && u.role !== role) return false
        if (status !== 'ALL' && u.status !== status) return false
        if (
          keyword &&
          !`${u.loginId}${u.email}${u.linkedEmployee}`
            .toLowerCase()
            .includes(keyword.toLowerCase())
        )
          return false
        return true
      }),
    [keyword, role, status],
  )

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <SearchInput
          value={keyword}
          onChange={setKeyword}
          placeholder="계정 · 이메일 검색"
          className="sm:max-w-xs"
        />
        <Select
          value={role}
          onValueChange={setRole}
          options={userRoleOptions}
          className="sm:w-40"
        />
        <Select
          value={status}
          onValueChange={setStatus}
          options={userStatusOptions}
          className="sm:w-32"
        />
        <Button className="sm:ml-auto" onClick={() => setOpenCreate(true)}>
          <UserPlus className="size-4" />
          사용자 추가
        </Button>
      </div>

      <div className="overflow-hidden rounded-lg border border-border">
        <table className="w-full text-sm">
          <thead className="bg-muted/60">
            <tr>
              {['로그인 ID', '이메일', '권한', '연결 사원', '최근 접속', '상태'].map(
                (h) => (
                  <th
                    key={h}
                    className="px-3 py-2.5 text-left text-xs font-semibold text-muted-foreground"
                  >
                    {h}
                  </th>
                ),
              )}
            </tr>
          </thead>
          <tbody>
            {filtered.map((u) => (
              <tr key={u.id} className="border-t border-border">
                <td className="px-3 py-2.5 font-medium">{u.loginId}</td>
                <td className="px-3 py-2.5 text-muted-foreground">{u.email}</td>
                <td className="px-3 py-2.5">
                  <RoleBadge role={u.role as RoleCode} />
                </td>
                <td className="px-3 py-2.5 text-muted-foreground">
                  {u.linkedEmployee}
                </td>
                <td className="px-3 py-2.5 font-mono text-xs tabular-nums text-muted-foreground">
                  {u.lastLogin}
                </td>
                <td className="px-3 py-2.5">
                  <Badge variant={u.status === 'ACTIVE' ? 'success' : 'muted'}>
                    {u.status === 'ACTIVE' ? '활성' : '비활성'}
                  </Badge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <ModalForm
        open={openCreate}
        onClose={() => setOpenCreate(false)}
        title="사용자 추가"
        description="신규 시스템 사용자 계정을 생성합니다."
        submitText="생성"
        submitDisabled={!newLoginId || !newEmail}
        onSubmit={() => {
          setNewLoginId('')
          setNewEmail('')
          setNewRole('VIEWER')
          setOpenCreate(false)
        }}
      >
        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="u-login">로그인 ID</Label>
            <Input
              id="u-login"
              value={newLoginId}
              onChange={(e) => setNewLoginId(e.target.value)}
              placeholder="예: hong_gd"
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="u-email">이메일</Label>
            <Input
              id="u-email"
              type="email"
              value={newEmail}
              onChange={(e) => setNewEmail(e.target.value)}
              placeholder="user@bwware.co.kr"
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label>권한</Label>
            <Select value={newRole} onValueChange={setNewRole} options={roleFormOptions} />
          </div>
        </div>
      </ModalForm>
    </div>
  )
}
