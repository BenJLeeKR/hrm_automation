'use client'

import { useState } from 'react'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import type { Employee } from '@/lib/types'
import { teamOptions, positionOptions, employeeStatusOptions } from '@/lib/options'

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  employee?: Employee
}

const teamSelectOptions = teamOptions.filter((o) => o.value !== 'ALL')
const positionSelectOptions = positionOptions.filter((o) => o.value !== 'ALL')
const statusSelectOptions = employeeStatusOptions.filter((o) => o.value !== 'ALL')

export function EmployeeFormModal({ open, onOpenChange, employee }: Props) {
  const isEdit = Boolean(employee)
  const [name, setName] = useState(employee?.name ?? '')
  const [empNo, setEmpNo] = useState(employee?.empNo ?? '')
  const [team, setTeam] = useState(employee?.team ?? 'DELIVERY')
  const [position, setPosition] = useState(employee?.position ?? 'SAWON')
  const [status, setStatus] = useState(employee?.status ?? 'ACTIVE')
  const [email, setEmail] = useState(employee?.email ?? '')
  const [phone, setPhone] = useState(employee?.phone ?? '')

  return (
    <ModalForm
      open={open}
      onClose={() => onOpenChange(false)}
      onSubmit={() => onOpenChange(false)}
      title={isEdit ? '사원 정보 수정' : '신규 사원 등록'}
      description="기본 인적사항을 입력합니다. 역량 정보는 상세 화면에서 관리합니다."
      submitText={isEdit ? '수정 저장' : '등록'}
    >
      <div className="grid grid-cols-2 gap-x-4">
        <FormField label="이름" required>
          <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="홍길동" />
        </FormField>
        <FormField label="사번" required>
          <Input
            value={empNo}
            onChange={(e) => setEmpNo(e.target.value)}
            placeholder="BW-000"
            disabled={isEdit}
          />
        </FormField>
        <FormField label="조직" required>
          <Select value={team} onValueChange={(v) => setTeam(v as Employee['team'])} options={teamSelectOptions} />
        </FormField>
        <FormField label="직급" required>
          <Select value={position} onValueChange={setPosition} options={positionSelectOptions} />
        </FormField>
        <FormField label="이메일">
          <Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="user@bwware.co.kr" />
        </FormField>
        <FormField label="연락처">
          <Input value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="010-0000-0000" />
        </FormField>
        <FormField label="재직 상태" required>
          <Select value={status} onValueChange={(v) => setStatus(v as Employee['status'])} options={statusSelectOptions} />
        </FormField>
      </div>
    </ModalForm>
  )
}
