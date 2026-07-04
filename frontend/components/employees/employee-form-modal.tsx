'use client'

import { useState } from 'react'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { apiPost, ApiError } from '@/lib/api'
import { employeeStatusOptions } from '@/lib/options'

// 로드맵 §9-1 "사원 목록 '사원 등록' 모달 — POST /api/v1/employees API 미연결" 해소.
// 조직/직급 Select는 실 마스터 데이터(DEPT_ID/JIKGUP_ID)를 부모(employees/page.tsx)로부터
// 전달받아 사용한다 — 다른 실 API 전환 화면들과 동일하게 하드코딩된 코드 목록 대신 실
// 마스터 데이터를 사용하는 원칙을 따른다.
//
// 수정(edit) 모드는 이번 범위에서 다루지 않는다 — 사원 상세 화면의 "정보수정" 버튼/폼
// 자체가 아직 없어(§9-1 별도 항목) 이 모달을 편집 용도로 여는 진입점이 없다. 필요 시
// `employee` prop과 `PATCH /api/v1/employees/{empl_id}` 연동을 그 작업에서 추가한다.
const statusSelectOptions = employeeStatusOptions.filter((o) => o.value !== 'ALL')

interface DepartmentOption {
  DEPT_ID: string
  DEPT_NM: string
}
interface PositionOption {
  JIKGUP_ID: string
  JIKGUP_NM: string
}

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSaved: () => void
  departments: DepartmentOption[]
  positions: PositionOption[]
}

export function EmployeeFormModal({ open, onOpenChange, onSaved, departments, positions }: Props) {
  const [name, setName] = useState('')
  const [empNo, setEmpNo] = useState('')
  const [deptId, setDeptId] = useState('')
  const [jikgupId, setJikgupId] = useState('')
  const [status, setStatus] = useState('ACTIVE')
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  const deptOptions = departments.map((d) => ({ label: d.DEPT_NM, value: d.DEPT_ID }))
  const positionOptions = positions.map((p) => ({ label: p.JIKGUP_NM, value: p.JIKGUP_ID }))

  function reset() {
    setName('')
    setEmpNo('')
    setDeptId('')
    setJikgupId('')
    setStatus('ACTIVE')
    setEmail('')
    setPhone('')
    setFormError(null)
  }

  function handleClose() {
    reset()
    onOpenChange(false)
  }

  async function handleSubmit() {
    setSubmitting(true)
    setFormError(null)
    try {
      await apiPost('/api/v1/employees', {
        EMPL_NO: empNo,
        EMPL_NM: name,
        DEPT_ID: deptId,
        JIKGUP_ID: jikgupId,
        EMPL_STAT_CD: status,
        EMAIL_ADDR: email || null,
        MPHONE_NO: phone || null,
      })
      onSaved()
      handleClose()
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : '등록에 실패했습니다. 잠시 후 다시 시도하세요.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <ModalForm
      open={open}
      onClose={handleClose}
      onSubmit={handleSubmit}
      title="신규 사원 등록"
      description="기본 인적사항을 입력합니다. 역량 정보는 상세 화면에서 관리합니다."
      submitText="등록"
      submitDisabled={submitting || !name.trim() || !empNo.trim() || !deptId || !jikgupId}
    >
      <div className="grid grid-cols-2 gap-x-4">
        {formError && <p className="col-span-2 mb-2 text-sm text-destructive">{formError}</p>}
        <FormField label="이름" required>
          <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="홍길동" />
        </FormField>
        <FormField label="사번" required>
          <Input value={empNo} onChange={(e) => setEmpNo(e.target.value)} placeholder="BW-000" />
        </FormField>
        <FormField label="조직" required>
          <Select value={deptId} onValueChange={setDeptId} options={deptOptions} placeholder="조직 선택" />
        </FormField>
        <FormField label="직급" required>
          <Select value={jikgupId} onValueChange={setJikgupId} options={positionOptions} placeholder="직급 선택" />
        </FormField>
        <FormField label="이메일">
          <Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="user@blueward.co.kr" />
        </FormField>
        <FormField label="연락처">
          <Input value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="010-0000-0000" />
        </FormField>
        <FormField label="재직 상태" required>
          <Select value={status} onValueChange={setStatus} options={statusSelectOptions} />
        </FormField>
      </div>
    </ModalForm>
  )
}
