'use client'

import { useState } from 'react'
import { ModalForm } from '@/components/common/modal-form'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { employees } from '@/lib/mock-data'
import type { AssignmentType } from '@/lib/types'

interface AssignedMember {
  empNo: string
  name: string
  role: string
  allocation: number
  type: AssignmentType
  startDate: string
  endDate: string
}

interface AssignmentFormModalProps {
  open: boolean
  onClose: () => void
  projectName: string
  onSubmit: (member: AssignedMember) => void
}

const employeeOptions = employees.map((e) => ({
  value: e.empNo,
  label: `${e.name} · ${e.roles.join('/')} (${e.allocation}%)`,
}))

const typeOptions = [
  { value: 'RUNNING', label: '수행중' },
  { value: 'COMMITTED', label: '투입준비중' },
  { value: 'PROPOSED', label: '제안중' },
]

export function AssignmentFormModal({
  open,
  onClose,
  projectName,
  onSubmit,
}: AssignmentFormModalProps) {
  const [empNo, setEmpNo] = useState('')
  const [role, setRole] = useState('')
  const [type, setType] = useState<AssignmentType>('RUNNING')
  const [allocation, setAllocation] = useState('50')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const selected = employees.find((e) => e.empNo === empNo)

  function reset() {
    setEmpNo('')
    setRole('')
    setType('RUNNING')
    setAllocation('50')
    setStartDate('')
    setEndDate('')
  }

  function handleSubmit() {
    if (!selected) return
    onSubmit({
      empNo: selected.empNo,
      name: selected.name,
      role: role || selected.roles[0] || '팀원',
      allocation: Number(allocation) || 0,
      type,
      startDate: startDate || '2026-07-01',
      endDate: endDate || '2026-12-31',
    })
    reset()
    onClose()
  }

  return (
    <ModalForm
      open={open}
      onClose={onClose}
      title="인력 투입"
      description={`${projectName} 프로젝트에 인력을 배정합니다.`}
      submitText="투입"
      onSubmit={handleSubmit}
      submitDisabled={!selected}
    >
      <div className="flex flex-col gap-4">
        <div className="flex flex-col gap-1.5">
          <Label>대상 사원</Label>
          <Select
            value={empNo}
            onValueChange={setEmpNo}
            options={employeeOptions}
            placeholder="사원 선택"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="assign-role">역할</Label>
            <Input
              id="assign-role"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              placeholder={selected?.roles[0] ?? '예: 백엔드 개발'}
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label>투입 유형</Label>
            <Select
              value={type}
              onValueChange={(v) => setType(v as AssignmentType)}
              options={typeOptions}
            />
          </div>
        </div>

        <div className="flex flex-col gap-1.5">
          <Label htmlFor="assign-alloc">투입률 (%)</Label>
          <Input
            id="assign-alloc"
            type="number"
            min={0}
            max={100}
            value={allocation}
            onChange={(e) => setAllocation(e.target.value)}
          />
          {selected && (
            <p className="text-xs text-muted-foreground">
              현재 가동률 {selected.allocation}% · 투입 후 예상{' '}
              <span
                className={
                  selected.allocation + Number(allocation) > 100
                    ? 'font-semibold text-destructive'
                    : 'font-semibold text-foreground'
                }
              >
                {selected.allocation + Number(allocation)}%
              </span>
            </p>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="assign-start">시작일</Label>
            <Input
              id="assign-start"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="assign-end">종료일</Label>
            <Input
              id="assign-end"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
        </div>
      </div>
    </ModalForm>
  )
}
