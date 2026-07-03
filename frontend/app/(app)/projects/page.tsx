'use client'

import { useEffect, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { FolderPlus, Users2, CalendarRange } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { FilterBar, FilterField } from '@/components/common/filter-bar'
import { SearchInput } from '@/components/common/search-input'
import { DataTable, type Column } from '@/components/common/data-table'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { apiGet, apiPost, ApiError } from '@/lib/api'
import { projectStatusOptions } from '@/lib/options'

// 백엔드 프로젝트 마스터 API(로드맵 §8 "프로젝트 목록/상세 화면 구현", SCR-007) 응답 타입 —
// 필드명은 backend/app/schemas/pjt_mst.py, pjt_asgn_his.py와 동일하게 유지한다.
interface ProjectOut {
  PJT_ID: string
  PJT_CD: string
  PJT_NM: string
  CLNT_NM: string | null
  PJT_STAT_CD: 'PLANNED' | 'RUNNING' | 'HOLD' | 'CLOSED'
  STRT_DT: string
  END_DT: string | null
  PJT_DESC: string | null
}
interface ProjectListResponse {
  total: number
  items: ProjectOut[]
}
interface AssignmentListResponse {
  items: Array<{ PJT_ID: string; ASGN_STAT_CD: string }>
}

const statusVariant: Record<ProjectOut['PJT_STAT_CD'], 'muted' | 'default' | 'warning' | 'secondary'> = {
  PLANNED: 'muted',
  RUNNING: 'default',
  HOLD: 'warning',
  CLOSED: 'secondary',
}
const statusSelectOptions = projectStatusOptions.filter((o) => o.value !== 'ALL')

async function loadProjects(): Promise<{ projects: ProjectOut[]; memberCountByPjtId: Map<string, number> }> {
  const [projectList, assignments] = await Promise.all([
    apiGet<ProjectListResponse>('/api/v1/projects?limit=200'),
    // 목록의 "투입 인원" 컬럼 계산용 — 전체 투입 이력 중 진행 중(ACTIVE)인 건만 집계
    apiGet<AssignmentListResponse>('/api/v1/assignments?limit=200&asgn_stat_cd=ACTIVE'),
  ])

  const memberCountByPjtId = new Map<string, number>()
  for (const a of assignments.items) {
    memberCountByPjtId.set(a.PJT_ID, (memberCountByPjtId.get(a.PJT_ID) ?? 0) + 1)
  }

  return { projects: projectList.items, memberCountByPjtId }
}

export default function ProjectsPage() {
  const router = useRouter()
  const [keyword, setKeyword] = useState('')
  const [status, setStatus] = useState('ALL')
  const [projects, setProjects] = useState<ProjectOut[]>([])
  const [memberCountByPjtId, setMemberCountByPjtId] = useState<Map<string, number>>(new Map())
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [openCreate, setOpenCreate] = useState(false)

  function reload() {
    setLoading(true)
    loadProjects()
      .then(({ projects, memberCountByPjtId }) => {
        setProjects(projects)
        setMemberCountByPjtId(memberCountByPjtId)
        setError(null)
      })
      .catch(() => setError('프로젝트 목록을 불러오지 못했습니다. 잠시 후 다시 시도하세요.'))
      .finally(() => setLoading(false))
  }

  useEffect(reload, [])

  const filtered = useMemo(
    () =>
      projects.filter((p) => {
        if (
          keyword &&
          !`${p.PJT_NM}${p.CLNT_NM ?? ''}${p.PJT_CD}`.toLowerCase().includes(keyword.toLowerCase())
        )
          return false
        if (status !== 'ALL' && p.PJT_STAT_CD !== status) return false
        return true
      }),
    [projects, keyword, status],
  )

  const columns: Column<ProjectOut>[] = [
    {
      key: 'name',
      header: '프로젝트',
      render: (p) => (
        <div>
          <p className="font-medium text-foreground">{p.PJT_NM}</p>
          <p className="text-xs text-muted-foreground">{p.PJT_CD}</p>
        </div>
      ),
    },
    { key: 'client', header: '고객사', render: (p) => <span className="text-sm">{p.CLNT_NM ?? '-'}</span> },
    {
      key: 'period',
      header: '수행 기간',
      render: (p) => (
        <span className="inline-flex items-center gap-1.5 text-sm tabular-nums text-muted-foreground">
          <CalendarRange className="size-3.5" />
          {p.STRT_DT} ~ {p.END_DT ?? '-'}
        </span>
      ),
    },
    {
      key: 'members',
      header: '투입 인원',
      render: (p) => (
        <span className="inline-flex items-center gap-1 text-sm tabular-nums">
          <Users2 className="size-3.5 text-muted-foreground" />
          {memberCountByPjtId.get(p.PJT_ID) ?? 0}명
        </span>
      ),
    },
    { key: 'status', header: '상태', render: (p) => <Badge variant={statusVariant[p.PJT_STAT_CD]}>{p.PJT_STAT_CD}</Badge> },
  ]

  return (
    <div>
      <PageHeader
        title="프로젝트 관리"
        description="수행 중이거나 예정된 프로젝트를 등록하고 투입 인력을 관리합니다."
      >
        <Button onClick={() => setOpenCreate(true)}>
          <FolderPlus className="size-4" />프로젝트 등록
        </Button>
      </PageHeader>

      {error && <p className="mb-4 text-sm text-destructive">{error}</p>}

      <FilterBar>
        <FilterField label="검색" className="min-w-56 flex-1">
          <SearchInput value={keyword} onChange={setKeyword} placeholder="프로젝트명 · 고객사 · 코드 검색" />
        </FilterField>
        <FilterField label="상태">
          <Select value={status} onValueChange={setStatus} options={projectStatusOptions} />
        </FilterField>
      </FilterBar>

      <DataTable
        columns={columns}
        data={filtered}
        rowKey={(p) => p.PJT_ID}
        onRowClick={(p) => router.push(`/projects/${p.PJT_ID}`)}
        emptyTitle={loading ? '불러오는 중입니다...' : '조건에 맞는 프로젝트가 없습니다'}
        footer={<span>전체 {projects.length}건 중 {filtered.length}건 표시</span>}
      />

      <ProjectFormModal open={openCreate} onClose={() => setOpenCreate(false)} onSaved={reload} />
    </div>
  )
}

function ProjectFormModal({
  open,
  onClose,
  onSaved,
}: {
  open: boolean
  onClose: () => void
  onSaved: () => void
}) {
  const [code, setCode] = useState('')
  const [name, setName] = useState('')
  const [client, setClient] = useState('')
  const [statusValue, setStatusValue] = useState(statusSelectOptions[0].value)
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [desc, setDesc] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  function reset() {
    setCode('')
    setName('')
    setClient('')
    setStatusValue(statusSelectOptions[0].value)
    setStartDate('')
    setEndDate('')
    setDesc('')
    setFormError(null)
  }

  async function handleSubmit() {
    setSubmitting(true)
    setFormError(null)
    try {
      await apiPost('/api/v1/projects', {
        PJT_CD: code.toUpperCase(),
        PJT_NM: name,
        CLNT_NM: client || null,
        PJT_STAT_CD: statusValue,
        STRT_DT: startDate,
        END_DT: endDate || null,
        PJT_DESC: desc || null,
      })
      onSaved()
      reset()
      onClose()
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : '등록에 실패했습니다. 잠시 후 다시 시도하세요.')
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
      title="프로젝트 등록"
      description="신규 프로젝트 기본 정보를 입력합니다."
      submitText="등록"
      onSubmit={handleSubmit}
      submitDisabled={submitting || !code.trim() || !name.trim() || !startDate}
    >
      <div className="flex flex-col gap-4">
        {formError && <p className="text-sm text-destructive">{formError}</p>}
        <FormField label="프로젝트 코드" required>
          <Input value={code} onChange={(e) => setCode(e.target.value)} placeholder="예: PJT006 (영문 대문자, 고유값)" />
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
          <Textarea value={desc} onChange={(e) => setDesc(e.target.value)} rows={3} placeholder="프로젝트 범위와 목표를 입력하세요." />
        </FormField>
      </div>
    </ModalForm>
  )
}
