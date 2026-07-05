'use client'

import { useState } from 'react'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { apiPatch, apiPost, ApiError } from '@/lib/api'
import { employeeStatusOptions } from '@/lib/options'
import type { EmployeeStatus } from '@/lib/types'

// 로드맵 §9-1 "사원 목록 '사원 등록' 모달 — POST /api/v1/employees API 미연결" 해소
// (2026-07-04)에 이어, "사원 상세 화면 — 정보수정 버튼/폼 없음" 항목 해소를 위해 수정
// 모드(`employee` prop 전달 시 `PATCH /api/v1/employees/{empl_id}`)를 추가했다.
// 조직/직급 Select는 실 마스터 데이터(DEPT_ID/JIKGUP_ID)를 호출부로부터 전달받아
// 사용한다 — 다른 실 API 전환 화면들과 동일하게 하드코딩된 코드 목록 대신 실 마스터
// 데이터를 사용하는 원칙을 따른다.
const statusSelectOptions = employeeStatusOptions.filter((o) => o.value !== 'ALL')

interface DepartmentOption {
  DEPT_ID: string
  DEPT_NM: string
}
interface PositionOption {
  JIKGUP_ID: string
  JIKGUP_NM: string
}
interface JobTypeOption {
  JIKMU_ID: string
  JIKMU_NM: string
}
interface EditableEmployee {
  EMPL_ID: string
  EMPL_NO: string
  EMPL_NM: string
  DEPT_ID: string
  JIKGUP_ID: string
  JIKMU_ID: string | null
  EMPL_STAT_CD: EmployeeStatus
  EMAIL_ADDR: string | null
  MPHONE_NO: string | null
}

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSaved: () => void
  departments: DepartmentOption[]
  positions: PositionOption[]
  jobTypes: JobTypeOption[]
  /** 전달 시 수정 모드로 동작한다 — 사번은 수정 불가(등록 시에만 입력). */
  employee?: EditableEmployee
}

export function EmployeeFormModal({ open, onOpenChange, onSaved, departments, positions, jobTypes, employee }: Props) {
  const isEdit = Boolean(employee)
  const [name, setName] = useState(employee?.EMPL_NM ?? '')
  const [empNo, setEmpNo] = useState(employee?.EMPL_NO ?? '')
  const [deptId, setDeptId] = useState(employee?.DEPT_ID ?? '')
  const [jikgupId, setJikgupId] = useState(employee?.JIKGUP_ID ?? '')
  const [jikmuId, setJikmuId] = useState(employee?.JIKMU_ID ?? '')
  const [status, setStatus] = useState(employee?.EMPL_STAT_CD ?? 'ACTIVE')
  const [email, setEmail] = useState(employee?.EMAIL_ADDR ?? '')
  const [phone, setPhone] = useState(employee?.MPHONE_NO ?? '')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  const deptOptions = departments.map((d) => ({ label: d.DEPT_NM, value: d.DEPT_ID }))
  const positionOptions = positions.map((p) => ({ label: p.JIKGUP_NM, value: p.JIKGUP_ID }))
  const jobTypeOptions = [
    { label: '선택 안 함', value: '' },
    ...jobTypes.map((j) => ({ label: j.JIKMU_NM, value: j.JIKMU_ID })),
  ]

  function reset() {
    setName(employee?.EMPL_NM ?? '')
    setEmpNo(employee?.EMPL_NO ?? '')
    setDeptId(employee?.DEPT_ID ?? '')
    setJikgupId(employee?.JIKGUP_ID ?? '')
    setJikmuId(employee?.JIKMU_ID ?? '')
    setStatus(employee?.EMPL_STAT_CD ?? 'ACTIVE')
    setEmail(employee?.EMAIL_ADDR ?? '')
    setPhone(employee?.MPHONE_NO ?? '')
    setFormError(null)
  }

  function handleClose() {
    reset()
    onOpenChange(false)
  }

  async function handleSubmit() {
    setSubmitting(true)
    setFormError(null)
    const payload = {
      EMPL_NM: name,
      DEPT_ID: deptId,
      JIKGUP_ID: jikgupId,
      JIKMU_ID: jikmuId || null,
      EMPL_STAT_CD: status,
      EMAIL_ADDR: email,
      MPHONE_NO: phone || null,
    }
    try {
      if (isEdit && employee) {
        await apiPatch(`/api/v1/employees/${employee.EMPL_ID}`, payload)
      } else {
        await apiPost('/api/v1/employees', { ...payload, EMPL_NO: empNo })
      }
      onSaved()
      handleClose()
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
      onClose={handleClose}
      onSubmit={handleSubmit}
      title={isEdit ? '사원 정보 수정' : '신규 사원 등록'}
      description="기본 인적사항을 입력합니다. 역량 정보는 상세 화면에서 관리합니다."
      submitText={isEdit ? '수정 저장' : '등록'}
      submitDisabled={submitting || !name.trim() || !empNo.trim() || !deptId || !jikgupId || !email.trim()}
    >
      <div className="grid grid-cols-2 gap-x-4">
        {formError && <p className="col-span-2 mb-2 text-sm text-destructive">{formError}</p>}
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
          <Select value={deptId} onValueChange={setDeptId} options={deptOptions} placeholder="조직 선택" />
        </FormField>
        <FormField label="직급" required>
          <Select value={jikgupId} onValueChange={setJikgupId} options={positionOptions} placeholder="직급 선택" />
        </FormField>
        <FormField label="직무 유형">
          <Select value={jikmuId} onValueChange={setJikmuId} options={jobTypeOptions} placeholder="직무 유형 선택" />
        </FormField>
        <FormField label="이메일" required>
          <Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="user@blueward.co.kr" />
        </FormField>
        <FormField label="연락처">
          <Input value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="010-0000-0000" />
        </FormField>
        <FormField label="재직 상태" required>
          <Select value={status} onValueChange={(v) => setStatus(v as EmployeeStatus)} options={statusSelectOptions} />
        </FormField>
      </div>
    </ModalForm>
  )
}
