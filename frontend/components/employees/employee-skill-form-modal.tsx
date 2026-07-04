'use client'

import { useState } from 'react'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { apiPost, ApiError } from '@/lib/api'

// 로드맵 §9-1 "사원 상세 화면 — 기술추가 버튼/폼 없음" 해소. 백엔드 `POST
// /api/v1/employee-skills`는 이미 구현되어 있어 신규 폼만 추가한다. 기술 Select는
// 호출부(사원 상세 화면)가 이미 조회해둔 전체 기술 목록을 그대로 재사용하고, 이미
// 보유한 기술은 목록에서 제외해 중복 등록(409)을 사전에 방지한다.
const PROFICIENCY_OPTIONS = [
  { label: 'Lv.1', value: '1' },
  { label: 'Lv.2', value: '2' },
  { label: 'Lv.3', value: '3' },
  { label: 'Lv.4', value: '4' },
  { label: 'Lv.5', value: '5' },
]

interface SkillOption {
  SKILL_ID: string
  SKILL_NM: string
}

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSaved: () => void
  emplId: string
  skillOptions: SkillOption[]
}

export function EmployeeSkillFormModal({ open, onOpenChange, onSaved, emplId, skillOptions }: Props) {
  const [skillId, setSkillId] = useState('')
  const [prfcyLevl, setPrfcyLevl] = useState('3')
  const [exprYear, setExprYear] = useState('')
  const [lastUseDt, setLastUseDt] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  const selectOptions = skillOptions.map((s) => ({ label: s.SKILL_NM, value: s.SKILL_ID }))

  function reset() {
    setSkillId('')
    setPrfcyLevl('3')
    setExprYear('')
    setLastUseDt('')
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
      await apiPost('/api/v1/employee-skills', {
        EMPL_ID: emplId,
        SKILL_ID: skillId,
        PRFCY_LEVL: Number(prfcyLevl),
        EXPR_YEAR: exprYear ? Number(exprYear) : null,
        LAST_USE_DT: lastUseDt || null,
      })
      onSaved()
      handleClose()
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : '기술 추가에 실패했습니다. 잠시 후 다시 시도하세요.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <ModalForm
      open={open}
      onClose={handleClose}
      onSubmit={handleSubmit}
      title="보유 기술 추가"
      description="사원이 보유한 기술과 숙련도를 등록합니다."
      submitText="추가"
      submitDisabled={submitting || !skillId}
    >
      <div className="grid grid-cols-2 gap-x-4">
        {formError && <p className="col-span-2 mb-2 text-sm text-destructive">{formError}</p>}
        <FormField label="기술" required>
          <Select value={skillId} onValueChange={setSkillId} options={selectOptions} placeholder="기술 선택" />
        </FormField>
        <FormField label="숙련도" required>
          <Select value={prfcyLevl} onValueChange={setPrfcyLevl} options={PROFICIENCY_OPTIONS} />
        </FormField>
        <FormField label="경력(년)">
          <Input
            type="number"
            step="0.5"
            min="0"
            value={exprYear}
            onChange={(e) => setExprYear(e.target.value)}
            placeholder="예: 3.5"
          />
        </FormField>
        <FormField label="최근 사용일">
          <Input type="date" value={lastUseDt} onChange={(e) => setLastUseDt(e.target.value)} />
        </FormField>
      </div>
    </ModalForm>
  )
}
