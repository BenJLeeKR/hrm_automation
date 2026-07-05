'use client'

import { useState } from 'react'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Select } from '@/components/ui/select'
import { apiPatch, apiPost, ApiError } from '@/lib/api'
import { projectStatusOptions } from '@/lib/options'

// 로드맵 §9-1 "프로젝트 상세 화면 — 수정 버튼/폼 없음" 해소를 위해, 그동안 프로젝트
// 목록 화면(`projects/page.tsx`)에 인라인으로만 있던 등록 전용 모달을 사원 관리 화면의
// `employee-form-modal.tsx`와 동일한 패턴(공용 컴포넌트 + `project` prop 전달 시 수정
// 모드)으로 추출한다. 상태 Select는 DB CHECK 제약과 동일한 고정 열거값(PLANNED/RUNNING/
// HOLD/CLOSED)이라 `lib/options.ts`의 하드코딩된 목록을 그대로 사용(다른 상태/유형 계열
// 필터와 동일한 원칙).
const statusSelectOptions = projectStatusOptions.filter((o) => o.value !== 'ALL')

interface EditableProject {
  PJT_ID: string
  PJT_CD: string
  PJT_NM: string
  CLNT_NM: string | null
  PJT_STAT_CD: string
  STRT_DT: string
  END_DT: string | null
  PJT_DESC: string | null
}

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSaved: () => void
  /** 전달 시 수정 모드로 동작한다 — 프로젝트 코드는 수정 불가(등록 시에만 입력, UNIQUE 제약). */
  project?: EditableProject
}

export function ProjectFormModal({ open, onOpenChange, onSaved, project }: Props) {
  const isEdit = Boolean(project)
  const [code, setCode] = useState(project?.PJT_CD ?? '')
  const [name, setName] = useState(project?.PJT_NM ?? '')
  const [client, setClient] = useState(project?.CLNT_NM ?? '')
  const [statusValue, setStatusValue] = useState(project?.PJT_STAT_CD ?? statusSelectOptions[0].value)
  const [startDate, setStartDate] = useState(project?.STRT_DT ?? '')
  const [endDate, setEndDate] = useState(project?.END_DT ?? '')
  const [desc, setDesc] = useState(project?.PJT_DESC ?? '')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  function reset() {
    setCode(project?.PJT_CD ?? '')
    setName(project?.PJT_NM ?? '')
    setClient(project?.CLNT_NM ?? '')
    setStatusValue(project?.PJT_STAT_CD ?? statusSelectOptions[0].value)
    setStartDate(project?.STRT_DT ?? '')
    setEndDate(project?.END_DT ?? '')
    setDesc(project?.PJT_DESC ?? '')
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
      PJT_NM: name,
      CLNT_NM: client || null,
      PJT_STAT_CD: statusValue,
      STRT_DT: startDate,
      END_DT: endDate || null,
      PJT_DESC: desc || null,
    }
    try {
      if (isEdit && project) {
        await apiPatch(`/api/v1/projects/${project.PJT_ID}`, payload)
      } else {
        await apiPost('/api/v1/projects', { ...payload, PJT_CD: code.toUpperCase() })
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
      title={isEdit ? '프로젝트 정보 수정' : '프로젝트 등록'}
      description={isEdit ? '프로젝트 기본 정보를 수정합니다.' : '신규 프로젝트 기본 정보를 입력합니다.'}
      submitText={isEdit ? '수정 저장' : '등록'}
      submitDisabled={submitting || !code.trim() || !name.trim() || !startDate}
    >
      <div className="flex flex-col gap-4">
        {formError && <p className="text-sm text-destructive">{formError}</p>}
        <FormField label="프로젝트 코드" required>
          <Input
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="예: PJT006 (영문 대문자, 고유값)"
            disabled={isEdit}
          />
        </FormField>
        <FormField label="프로젝트명" required>
          <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="예: 차세대 여신 시스템 구축" />
        </FormField>
        <div className="grid grid-cols-2 gap-4">
          <FormField label="고객사">
            <Input value={client} onChange={(e) => setClient(e.target.value)} placeholder="예: K은행" />
          </FormField>
          <FormField label="상태" required>
            <Select value={statusValue} onValueChange={setStatusValue} options={statusSelectOptions} />
          </FormField>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <FormField label="시작일" required>
            <Input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </FormField>
          <FormField label="종료일">
            <Input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </FormField>
        </div>
        <FormField label="개요">
          <Textarea
            value={desc ?? ''}
            onChange={(e) => setDesc(e.target.value)}
            rows={3}
            placeholder="프로젝트 범위와 목표를 입력하세요."
          />
        </FormField>
      </div>
    </ModalForm>
  )
}
