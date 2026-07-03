'use client'

import { useEffect, useMemo, useState } from 'react'
import { Plus, Wrench, Users2, Pencil, Power } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { FilterBar, FilterField } from '@/components/common/filter-bar'
import { SearchInput } from '@/components/common/search-input'
import { DataTable, type Column } from '@/components/common/data-table'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { StatCard } from '@/components/common/stat-card'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { apiGet, apiPatch, apiPost, ApiError } from '@/lib/api'
import { skillGroupOptions, useYnOptions } from '@/lib/options'

// 백엔드 기술 마스터 API(로드맵 §8 "기술 관리 화면 구현", SCR-005) 응답 타입 —
// 필드명은 backend/app/schemas/hr_skill_mst.py, hr_empl_skill_rel.py와 동일하게 유지한다.
interface SkillOut {
  SKILL_ID: string
  SKILL_GRP_CD: string
  SKILL_NM: string
  USE_YN: boolean
}
interface EmployeeSkillOut {
  SKILL_ID: string
}

const groupSelectOptions = skillGroupOptions.filter((o) => o.value !== 'ALL')
const useYnSelectOptions = useYnOptions.filter((o) => o.value !== 'ALL')

async function loadSkills(): Promise<{ skills: SkillOut[]; userCountBySkillId: Map<string, number> }> {
  // 백엔드 GET /skills는 use_yn 파라미터 생략 시 사용중(true)인 기술만 반환하므로,
  // "전체"(사용중+미사용) 목록을 보여주기 위해 두 상태를 각각 조회해 병합한다.
  const [activeSkills, inactiveSkills, employeeSkills] = await Promise.all([
    apiGet<SkillOut[]>('/api/v1/skills?use_yn=true'),
    apiGet<SkillOut[]>('/api/v1/skills?use_yn=false'),
    apiGet<EmployeeSkillOut[]>('/api/v1/employee-skills'),
  ])

  const userCountBySkillId = new Map<string, number>()
  for (const es of employeeSkills) {
    userCountBySkillId.set(es.SKILL_ID, (userCountBySkillId.get(es.SKILL_ID) ?? 0) + 1)
  }

  return { skills: [...activeSkills, ...inactiveSkills], userCountBySkillId }
}

export default function SkillsPage() {
  const [keyword, setKeyword] = useState('')
  const [group, setGroup] = useState('ALL')
  const [useYn, setUseYn] = useState('ALL')
  const [skills, setSkills] = useState<SkillOut[]>([])
  const [userCountBySkillId, setUserCountBySkillId] = useState<Map<string, number>>(new Map())
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState<SkillOut | null>(null)
  const [openForm, setOpenForm] = useState(false)

  function reload() {
    setLoading(true)
    loadSkills()
      .then(({ skills, userCountBySkillId }) => {
        setSkills(skills)
        setUserCountBySkillId(userCountBySkillId)
        setError(null)
      })
      .catch(() => setError('기술 목록을 불러오지 못했습니다. 잠시 후 다시 시도하세요.'))
      .finally(() => setLoading(false))
  }

  useEffect(reload, [])

  const filtered = useMemo(
    () =>
      skills.filter((s) => {
        if (keyword && !s.SKILL_NM.toLowerCase().includes(keyword.toLowerCase())) return false
        if (group !== 'ALL' && s.SKILL_GRP_CD !== group) return false
        if (useYn !== 'ALL' && String(s.USE_YN) !== useYn) return false
        return true
      }),
    [skills, keyword, group, useYn],
  )

  const activeCount = skills.filter((s) => s.USE_YN).length
  const totalUsers = [...userCountBySkillId.values()].reduce((sum, n) => sum + n, 0)

  function openEdit(skill: SkillOut) {
    setEditing(skill)
    setOpenForm(true)
  }
  function openCreate() {
    setEditing(null)
    setOpenForm(true)
  }

  async function toggleUseYn(skill: SkillOut) {
    try {
      await apiPatch(`/api/v1/skills/${skill.SKILL_ID}`, { USE_YN: !skill.USE_YN })
      reload()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : '사용 여부 변경에 실패했습니다.')
    }
  }

  const columns: Column<SkillOut>[] = [
    { key: 'group', header: '기술 그룹', className: 'w-32', render: (s) => <Badge variant="secondary">{s.SKILL_GRP_CD}</Badge> },
    { key: 'name', header: '기술명', render: (s) => <span className="font-medium">{s.SKILL_NM}</span> },
    {
      key: 'userCount',
      header: '보유 인원',
      render: (s) => (
        <span className="inline-flex items-center gap-1 text-sm tabular-nums">
          <Users2 className="size-3.5 text-muted-foreground" />
          {userCountBySkillId.get(s.SKILL_ID) ?? 0}명
        </span>
      ),
    },
    {
      key: 'useYn',
      header: '사용 여부',
      render: (s) => (
        <Badge variant={s.USE_YN ? 'success' : 'muted'}>{s.USE_YN ? '사용중' : '미사용'}</Badge>
      ),
    },
    {
      key: 'actions',
      header: '',
      className: 'w-24 text-right',
      render: (s) => (
        <div className="flex justify-end gap-1">
          <Button size="icon-sm" variant="ghost" onClick={(e) => { e.stopPropagation(); openEdit(s) }} aria-label="수정">
            <Pencil className="size-4" />
          </Button>
          <Button size="icon-sm" variant="ghost" onClick={(e) => { e.stopPropagation(); toggleUseYn(s) }} aria-label={s.USE_YN ? '비활성화' : '활성화'}>
            <Power className="size-4" />
          </Button>
        </div>
      ),
    },
  ]

  return (
    <div>
      <PageHeader
        title="기술 관리"
        description="조직에서 관리하는 표준 기술 스택을 등록하고 유지보수합니다."
      >
        <Button onClick={openCreate}>
          <Plus className="size-4" />기술 등록
        </Button>
      </PageHeader>

      {error && <p className="mb-4 text-sm text-destructive">{error}</p>}

      <div className="mb-4 grid grid-cols-2 gap-4 lg:grid-cols-3">
        <StatCard label="전체 기술" value={String(skills.length)} unit="개" icon={Wrench} tone="primary" />
        <StatCard label="사용중 기술" value={String(activeCount)} unit="개" icon={Wrench} tone="success" />
        <StatCard label="누적 보유 인원" value={String(totalUsers)} unit="명" icon={Users2} tone="info" />
      </div>

      <FilterBar>
        <FilterField label="검색" className="min-w-56 flex-1">
          <SearchInput value={keyword} onChange={setKeyword} placeholder="기술명 검색" />
        </FilterField>
        <FilterField label="기술 그룹">
          <Select value={group} onValueChange={setGroup} options={skillGroupOptions} />
        </FilterField>
        <FilterField label="사용 여부">
          <Select value={useYn} onValueChange={setUseYn} options={useYnOptions} />
        </FilterField>
      </FilterBar>

      <DataTable
        columns={columns}
        data={filtered}
        rowKey={(s) => s.SKILL_ID}
        emptyTitle={loading ? '불러오는 중입니다...' : '조건에 맞는 기술이 없습니다'}
        footer={<span>전체 {skills.length}개 중 {filtered.length}개 표시</span>}
      />

      <SkillFormModal
        key={editing?.SKILL_ID ?? 'new'}
        open={openForm}
        onClose={() => setOpenForm(false)}
        skill={editing}
        onSaved={reload}
      />
    </div>
  )
}

function SkillFormModal({
  open,
  onClose,
  skill,
  onSaved,
}: {
  open: boolean
  onClose: () => void
  skill: SkillOut | null
  onSaved: () => void
}) {
  const [name, setName] = useState(skill?.SKILL_NM ?? '')
  const [group, setGroup] = useState(skill?.SKILL_GRP_CD ?? groupSelectOptions[0].value)
  const [useYn, setUseYn] = useState(String(skill?.USE_YN ?? true))
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  async function handleSubmit() {
    setSubmitting(true)
    setFormError(null)
    try {
      if (skill) {
        await apiPatch(`/api/v1/skills/${skill.SKILL_ID}`, {
          SKILL_NM: name,
          SKILL_GRP_CD: group,
          USE_YN: useYn === 'true',
        })
      } else {
        await apiPost('/api/v1/skills', {
          SKILL_NM: name,
          SKILL_GRP_CD: group,
          USE_YN: useYn === 'true',
        })
      }
      onSaved()
      onClose()
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : '저장에 실패했습니다. 잠시 후 다시 시도하세요.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <ModalForm
      open={open}
      onClose={onClose}
      onSubmit={handleSubmit}
      title={skill ? '기술 수정' : '기술 등록'}
      submitText={skill ? '수정 저장' : '등록'}
      submitDisabled={submitting || !name.trim()}
    >
      {formError && <p className="mb-3 text-sm text-destructive">{formError}</p>}
      <FormField label="기술명" required>
        <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="예: Kotlin" />
      </FormField>
      <FormField label="기술 그룹" required>
        <Select value={group} onValueChange={setGroup} options={groupSelectOptions} />
      </FormField>
      <FormField label="사용 여부" required>
        <Select value={useYn} onValueChange={setUseYn} options={useYnSelectOptions} />
      </FormField>
    </ModalForm>
  )
}
