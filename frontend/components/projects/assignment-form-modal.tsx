'use client'

import { useState } from 'react'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Select } from '@/components/ui/select'
import { apiPatch, apiPost, ApiError } from '@/lib/api'
import { assignmentTypeOptions, assignmentStatusOptions } from '@/lib/options'

// 로드맵 §9-1 "프로젝트 상세 화면 — 인력투입 버튼 없음" 해소를 위해, 그동안 투입 관리
// 화면(`assignments/page.tsx`)에 인라인 함수로만 있던 실 API 연동 등록 모달을, 이미
// 저장소에 있었으나 목데이터(`lib/mock-data.ts`) 기반이라 어디에서도 실제로 쓰이지
// 않던 이 파일을 대체하며 공용 컴포넌트로 추출한다. `fixedPjtId`/`fixedPjtName` 전달
// 시(프로젝트 상세 화면) 프로젝트 Select 대신 고정 표시하고, 미전달 시(투입 관리
// 화면) 프로젝트 목록에서 선택하는 기존 동작을 그대로 유지한다.
//
// §9-1 "투입 이력 개별(인력별) 수정 버튼/폼 없음" 해소를 위해 `assignment` prop 전달 시
// 수정 모드(`PATCH /api/v1/assignments/{asgn_id}`)를 추가했다 — 사원 관리의
// `employee-form-modal.tsx`와 동일한 등록/수정 공용 패턴. 대상 사원·프로젝트는 등록
// 이후 변경할 대상이 아니라(사번/프로젝트 코드와 동일한 원칙) 수정 모드에서는 Select를
// 비활성화하고, 대신 진행 상태(`ASGN_STAT_CD`) Select를 새로 노출한다.
const typeSelectOptions = assignmentTypeOptions.filter((o) => o.value !== 'ALL')
const statusSelectOptions = assignmentStatusOptions.filter((o) => o.value !== 'ALL')

interface EmployeeOption {
  EMPL_ID: string
  EMPL_NO: string
  EMPL_NM: string
}
interface ProjectOption {
  PJT_ID: string
  PJT_NM: string
}
interface EditableAssignment {
  ASGN_ID: string
  EMPL_ID: string
  PJT_ID: string
  ASGN_TYPE_CD: string
  PRJT_ROLE_NM: string
  ALLOC_RT: number
  ASGN_STRT_DT: string
  ASGN_END_DT: string | null
  ASGN_STAT_CD: string
  RMRK: string | null
}

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSaved: () => void
  employees: EmployeeOption[]
  projects?: ProjectOption[]
  fixedPjtId?: string
  fixedPjtName?: string
  /** 전달 시 수정 모드로 동작한다 — 대상 사원·프로젝트는 수정 불가. */
  assignment?: EditableAssignment
}

export function AssignmentFormModal({
  open,
  onOpenChange,
  onSaved,
  employees,
  projects,
  fixedPjtId,
  fixedPjtName,
  assignment,
}: Props) {
  const isEdit = Boolean(assignment)
  const employeeOptions = employees.map((e) => ({ label: `${e.EMPL_NM} (${e.EMPL_NO})`, value: e.EMPL_ID }))
  const projectOptions = (projects ?? []).map((p) => ({ label: p.PJT_NM, value: p.PJT_ID }))

  const [empId, setEmpId] = useState(assignment?.EMPL_ID ?? '')
  const [pjtId, setPjtId] = useState(assignment?.PJT_ID ?? '')
  const [type, setType] = useState(assignment?.ASGN_TYPE_CD ?? typeSelectOptions[0].value)
  const [status, setStatus] = useState(assignment?.ASGN_STAT_CD ?? statusSelectOptions[0].value)
  const [role, setRole] = useState(assignment?.PRJT_ROLE_NM ?? '')
  const [startDate, setStartDate] = useState(assignment?.ASGN_STRT_DT ?? '')
  const [endDate, setEndDate] = useState(assignment?.ASGN_END_DT ?? '')
  const [allocRt, setAllocRt] = useState(String(assignment?.ALLOC_RT ?? 100))
  const [remark, setRemark] = useState(assignment?.RMRK ?? '')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  function reset() {
    setEmpId(assignment?.EMPL_ID ?? '')
    setPjtId(assignment?.PJT_ID ?? '')
    setType(assignment?.ASGN_TYPE_CD ?? typeSelectOptions[0].value)
    setStatus(assignment?.ASGN_STAT_CD ?? statusSelectOptions[0].value)
    setRole(assignment?.PRJT_ROLE_NM ?? '')
    setStartDate(assignment?.ASGN_STRT_DT ?? '')
    setEndDate(assignment?.ASGN_END_DT ?? '')
    setAllocRt(String(assignment?.ALLOC_RT ?? 100))
    setRemark(assignment?.RMRK ?? '')
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
      if (isEdit && assignment) {
        await apiPatch(`/api/v1/assignments/${assignment.ASGN_ID}`, {
          ASGN_TYPE_CD: type,
          PRJT_ROLE_NM: role,
          ALLOC_RT: Number(allocRt),
          ASGN_STRT_DT: startDate,
          ASGN_END_DT: endDate || null,
          ASGN_STAT_CD: status,
          RMRK: remark || null,
        })
      } else {
        await apiPost('/api/v1/assignments', {
          EMPL_ID: empId,
          PJT_ID: fixedPjtId ?? pjtId,
          ASGN_TYPE_CD: type,
          PRJT_ROLE_NM: role,
          ALLOC_RT: Number(allocRt),
          ASGN_STRT_DT: startDate,
          ASGN_END_DT: endDate || null,
          RMRK: remark || null,
        })
      }
      onSaved()
      handleClose()
    } catch (err) {
      // 동일 사원·겹치는 기간 ALLOC_RT 합계 100% 초과 시 백엔드가 409를 반환한다 —
      // 서버 검증 메시지를 그대로 보여준다.
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
      title={isEdit ? '투입 정보 수정' : '투입 등록'}
      description={fixedPjtName ? `${fixedPjtName} 프로젝트에 인력을 배정합니다.` : undefined}
      submitText={isEdit ? '수정 저장' : '등록'}
      onSubmit={handleSubmit}
      submitDisabled={submitting || !empId || (!fixedPjtId && !pjtId) || !role.trim() || !startDate || !allocRt}
    >
      <div className="flex flex-col gap-4">
        {formError && <p className="text-sm text-destructive">{formError}</p>}
        <FormField label="사원" required>
          <Select value={empId} onValueChange={setEmpId} options={employeeOptions} placeholder="사원 선택" disabled={isEdit} />
        </FormField>
        {!fixedPjtId && (
          <FormField label="프로젝트" required>
            <Select
              value={pjtId}
              onValueChange={setPjtId}
              options={projectOptions}
              placeholder="프로젝트 선택"
              disabled={isEdit}
            />
          </FormField>
        )}
        <FormField label="프로젝트 유형" required>
          <Select value={type} onValueChange={setType} options={typeSelectOptions} />
        </FormField>
        {isEdit && (
          <FormField label="진행 상태" required>
            <Select value={status} onValueChange={setStatus} options={statusSelectOptions} />
          </FormField>
        )}
        <FormField label="프로젝트 내 역할" required>
          <Input value={role} onChange={(e) => setRole(e.target.value)} placeholder="예: 리드개발, 분석, 참여" />
        </FormField>
        <div className="grid grid-cols-2 gap-4">
          <FormField label="투입 시작일" required>
            <Input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </FormField>
          <FormField label="투입 종료 예정일">
            <Input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </FormField>
        </div>
        <FormField label="투입률(%)" required>
          <Input type="number" min={0} max={100} value={allocRt} onChange={(e) => setAllocRt(e.target.value)} />
        </FormField>
        <FormField label="비고">
          <Textarea value={remark ?? ''} onChange={(e) => setRemark(e.target.value)} rows={2} />
        </FormField>
      </div>
    </ModalForm>
  )
}
