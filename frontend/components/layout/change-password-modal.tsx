'use client'

import { useState } from 'react'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { apiPost, ApiError } from '@/lib/api'

interface ChangePasswordModalProps {
  open: boolean
  onClose: () => void
}

// 백엔드 `POST /api/v1/auth/change-password`(`app/api/v1/auth.py`, §9-1 "설정" 메뉴를
// "비밀번호 변경"으로 교체) 연동 — 현재 비밀번호 확인 후 본인 비밀번호만 교체한다.
export function ChangePasswordModal({ open, onClose }: ChangePasswordModalProps) {
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  function reset() {
    setCurrentPassword('')
    setNewPassword('')
    setConfirmPassword('')
    setError(null)
  }

  async function handleSubmit() {
    if (newPassword !== confirmPassword) {
      setError('새 비밀번호가 일치하지 않습니다.')
      return
    }
    setSubmitting(true)
    setError(null)
    try {
      await apiPost('/api/v1/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      })
      reset()
      onClose()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : '비밀번호 변경에 실패했습니다. 잠시 후 다시 시도하세요.')
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
      title="비밀번호 변경"
      description="현재 비밀번호를 확인한 뒤 새 비밀번호로 변경합니다."
      submitText="변경"
      onSubmit={handleSubmit}
      submitDisabled={submitting || !currentPassword || !newPassword || !confirmPassword}
    >
      <div className="flex flex-col gap-4">
        {error && <p className="text-sm text-destructive">{error}</p>}
        <FormField label="현재 비밀번호" required>
          <Input type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} />
        </FormField>
        <FormField label="새 비밀번호" required hint="8자 이상, 영문+숫자+특수문자 포함">
          <Input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
        </FormField>
        <FormField label="새 비밀번호 확인" required>
          <Input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
        </FormField>
      </div>
    </ModalForm>
  )
}
