'use client'

import { useEffect, useMemo, useState } from 'react'
import { Pencil, UserPlus, UserX } from 'lucide-react'
import { SearchInput } from '@/components/common/search-input'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { RoleBadge } from '@/components/common/status-badge'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { ConfirmDialog } from '@/components/common/confirm-dialog'
import { Input } from '@/components/ui/input'
import { apiGet, apiDelete, apiPatch, apiPost, ApiError } from '@/lib/api'
import type { RoleCode } from '@/lib/types'

// 백엔드 사용자 관리 API(로드맵 §8 "설정 화면 구현", SCR-015) 응답 타입 — 필드명은
// backend/app/schemas/sys_user_mst.py, sys_role_mst.py와 동일하게 유지한다.
interface SysUserOut {
  USER_ID: string
  EMPL_ID: string | null
  USER_LGID: string
  EMAIL_ADDR: string
  ROLE_ID: string
  USE_YN: boolean
  LAST_LGN_DTTM: string | null
}
interface RoleOut {
  ROLE_ID: string
  ROLE_CD: string
  ROLE_NM: string
}

export function UsersTable() {
  const [keyword, setKeyword] = useState('')
  const [roleFilter, setRoleFilter] = useState('ALL')
  const [statusFilter, setStatusFilter] = useState('ALL')
  const [users, setUsers] = useState<SysUserOut[]>([])
  const [roles, setRoles] = useState<RoleOut[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [openCreate, setOpenCreate] = useState(false)
  const [editTarget, setEditTarget] = useState<SysUserOut | null>(null)
  const [deactivateTarget, setDeactivateTarget] = useState<SysUserOut | null>(null)
  const [deactivating, setDeactivating] = useState(false)
  const [deactivateError, setDeactivateError] = useState<string | null>(null)

  async function handleDeactivate() {
    if (!deactivateTarget) return
    setDeactivating(true)
    setDeactivateError(null)
    try {
      await apiDelete(`/api/v1/users/${deactivateTarget.USER_ID}`)
      reload()
    } catch (err) {
      setDeactivateError(err instanceof ApiError ? err.message : '계정 비활성화에 실패했습니다. 잠시 후 다시 시도하세요.')
    } finally {
      setDeactivating(false)
    }
  }

  function reload() {
    setLoading(true)
    Promise.all([apiGet<SysUserOut[]>('/api/v1/users'), apiGet<RoleOut[]>('/api/v1/users/roles')])
      .then(([usersRes, rolesRes]) => {
        setUsers(usersRes)
        setRoles(rolesRes)
        setError(null)
      })
      .catch(() => setError('사용자 목록을 불러오지 못했습니다. 잠시 후 다시 시도하세요.'))
      .finally(() => setLoading(false))
  }

  useEffect(reload, [])

  const roleById = useMemo(() => new Map(roles.map((r) => [r.ROLE_ID, r])), [roles])
  const roleFilterOptions = useMemo(
    () => [{ label: '전체', value: 'ALL' }, ...roles.map((r) => ({ label: r.ROLE_NM, value: r.ROLE_ID }))],
    [roles],
  )
  const statusOptions = [
    { label: '전체', value: 'ALL' },
    { label: '활성', value: 'true' },
    { label: '비활성', value: 'false' },
  ]

  const filtered = useMemo(
    () =>
      users.filter((u) => {
        if (roleFilter !== 'ALL' && u.ROLE_ID !== roleFilter) return false
        if (statusFilter !== 'ALL' && String(u.USE_YN) !== statusFilter) return false
        if (keyword && !`${u.USER_LGID}${u.EMAIL_ADDR}`.toLowerCase().includes(keyword.toLowerCase())) return false
        return true
      }),
    [users, keyword, roleFilter, statusFilter],
  )

  return (
    <div className="flex flex-col gap-4">
      {error && <p className="text-sm text-destructive">{error}</p>}
      {deactivateError && <p className="text-sm text-destructive">{deactivateError}</p>}

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <SearchInput
          value={keyword}
          onChange={setKeyword}
          placeholder="계정 · 이메일 검색"
          className="sm:max-w-xs"
        />
        <Select value={roleFilter} onValueChange={setRoleFilter} options={roleFilterOptions} className="sm:w-40" />
        <Select value={statusFilter} onValueChange={setStatusFilter} options={statusOptions} className="sm:w-32" />
        <Button className="sm:ml-auto" onClick={() => setOpenCreate(true)}>
          <UserPlus className="size-4" />
          사용자 추가
        </Button>
      </div>

      <div className="overflow-hidden rounded-lg border border-border">
        <table className="w-full text-sm">
          <thead className="bg-muted/60">
            <tr>
              {['로그인 ID', '이메일', '권한', '최근 접속', '상태', ''].map((h) => (
                <th key={h} className="px-3 py-2.5 text-left text-xs font-semibold text-muted-foreground">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 && (
              <tr>
                <td colSpan={6} className="px-3 py-6 text-center text-sm text-muted-foreground">
                  {loading ? '불러오는 중입니다...' : '조건에 맞는 사용자가 없습니다.'}
                </td>
              </tr>
            )}
            {filtered.map((u) => {
              const role = roleById.get(u.ROLE_ID)
              return (
                <tr key={u.USER_ID} className="border-t border-border">
                  <td className="px-3 py-2.5 font-medium">{u.USER_LGID}</td>
                  <td className="px-3 py-2.5 text-muted-foreground">{u.EMAIL_ADDR}</td>
                  <td className="px-3 py-2.5">
                    {role ? <RoleBadge role={role.ROLE_CD as RoleCode} /> : <Badge variant="muted">{u.ROLE_ID}</Badge>}
                  </td>
                  <td className="px-3 py-2.5 font-mono text-xs tabular-nums text-muted-foreground">
                    {u.LAST_LGN_DTTM ?? '-'}
                  </td>
                  <td className="px-3 py-2.5">
                    <Badge variant={u.USE_YN ? 'success' : 'muted'}>{u.USE_YN ? '활성' : '비활성'}</Badge>
                  </td>
                  <td className="px-3 py-2.5 text-right">
                    <div className="flex justify-end gap-1">
                      <button
                        type="button"
                        onClick={() => setEditTarget(u)}
                        className="rounded-lg p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
                        aria-label="계정 수정"
                      >
                        <Pencil className="size-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => setDeactivateTarget(u)}
                        disabled={!u.USE_YN}
                        className="rounded-lg p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground disabled:cursor-not-allowed disabled:opacity-40"
                        aria-label="계정 비활성화"
                      >
                        <UserX className="size-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      <UserFormModal open={openCreate} onClose={() => setOpenCreate(false)} roles={roles} onSaved={reload} />
      {editTarget && (
        <UserFormModal
          open
          onClose={() => setEditTarget(null)}
          roles={roles}
          onSaved={reload}
          user={editTarget}
        />
      )}
      <ConfirmDialog
        open={deactivateTarget !== null}
        onClose={() => setDeactivateTarget(null)}
        onConfirm={handleDeactivate}
        title="계정을 비활성화하시겠습니까?"
        description={
          deactivateTarget ? `"${deactivateTarget.USER_LGID}" 계정을 비활성화합니다. 계정 정보는 삭제되지 않으며, 비활성화 후에는 로그인할 수 없습니다.` : undefined
        }
        confirmText={deactivating ? '처리 중...' : '비활성화'}
        destructive
      />
    </div>
  )
}

function UserFormModal({
  open,
  onClose,
  roles,
  onSaved,
  user,
}: {
  open: boolean
  onClose: () => void
  roles: RoleOut[]
  onSaved: () => void
  /** 전달 시 수정 모드로 동작한다 — 로그인 ID·비밀번호는 이번 범위에서 수정 불가. */
  user?: SysUserOut
}) {
  const isEdit = Boolean(user)
  const [loginId, setLoginId] = useState(user?.USER_LGID ?? '')
  const [email, setEmail] = useState(user?.EMAIL_ADDR ?? '')
  const [password, setPassword] = useState('')
  const [roleId, setRoleId] = useState(user?.ROLE_ID ?? '')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  const roleOptions = roles.map((r) => ({ label: r.ROLE_NM, value: r.ROLE_ID }))

  function reset() {
    setLoginId(user?.USER_LGID ?? '')
    setEmail(user?.EMAIL_ADDR ?? '')
    setPassword('')
    setRoleId(user?.ROLE_ID ?? '')
    setFormError(null)
  }

  async function handleSubmit() {
    setSubmitting(true)
    setFormError(null)
    try {
      if (isEdit && user) {
        await apiPatch(`/api/v1/users/${user.USER_ID}`, { EMAIL_ADDR: email, ROLE_ID: roleId })
      } else {
        await apiPost('/api/v1/users', {
          USER_LGID: loginId,
          EMAIL_ADDR: email,
          password,
          ROLE_ID: roleId,
        })
      }
      onSaved()
      reset()
      onClose()
    } catch (err) {
      const fallback = isEdit ? '수정에 실패했습니다. 잠시 후 다시 시도하세요.' : '등록에 실패했습니다. 잠시 후 다시 시도하세요.'
      setFormError(err instanceof ApiError ? err.message : fallback)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <ModalForm
      open={open}
      onClose={() => {
        reset()
        onClose()
      }}
      title={isEdit ? '계정 수정' : '사용자 추가'}
      description={isEdit ? '이메일과 권한을 수정합니다.' : '신규 시스템 사용자 계정을 생성합니다.'}
      submitText={isEdit ? '수정 저장' : '생성'}
      onSubmit={handleSubmit}
      submitDisabled={
        submitting || !loginId.trim() || !email.trim() || (!isEdit && !password) || !roleId
      }
    >
      <div className="flex flex-col gap-4">
        {formError && <p className="text-sm text-destructive">{formError}</p>}
        <FormField label="로그인 ID" required>
          <Input
            value={loginId}
            onChange={(e) => setLoginId(e.target.value)}
            placeholder="예: hong_gd"
            disabled={isEdit}
          />
        </FormField>
        <FormField label="이메일" required>
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="user@blueward.co.kr"
          />
        </FormField>
        {!isEdit && (
          <FormField label="초기 비밀번호" required>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="8자 이상, 영문+숫자+특수문자"
            />
          </FormField>
        )}
        <FormField label="권한" required>
          <Select value={roleId} onValueChange={setRoleId} options={roleOptions} placeholder="권한 선택" />
        </FormField>
      </div>
    </ModalForm>
  )
}
