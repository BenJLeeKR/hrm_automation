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
import { ProjectFormModal } from '@/components/projects/project-form-modal'
import { apiGet } from '@/lib/api'
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
  items: Array<{ PJT_ID: string; ASGN_STAT_CD: string; ASGN_STRT_DT: string; ASGN_END_DT: string | null }>
}

const statusVariant: Record<ProjectOut['PJT_STAT_CD'], 'muted' | 'default' | 'warning' | 'secondary'> = {
  PLANNED: 'muted',
  RUNNING: 'default',
  HOLD: 'warning',
  CLOSED: 'secondary',
}
async function loadProjects(): Promise<{ projects: ProjectOut[]; memberCountByPjtId: Map<string, number> }> {
  const [projectList, assignments] = await Promise.all([
    apiGet<ProjectListResponse>('/api/v1/projects?limit=200'),
    // 목록의 "투입 인원" 컬럼 계산용 — 전체 투입 이력 중 진행 중(ACTIVE)인 건만 집계
    apiGet<AssignmentListResponse>('/api/v1/assignments?limit=200&asgn_stat_cd=ACTIVE'),
  ])

  // 사원 상세 화면과 동일하게, `AVAILABILITY_CALC_SPEC.md` §2/§4 기준 "진행 중"은
  // ASGN_STAT_CD='ACTIVE'뿐 아니라 오늘이 투입 기간(ASGN_STRT_DT~ASGN_END_DT) 안에
  // 있어야 한다 — 이 조건이 없으면 투입 기간이 이미 끝난 ACTIVE 건까지 인원수에
  // 잡혀 사원 목록의 가동률 집계와 어긋난다(사용자 리포트로 발견, 2026-07-05).
  const today = new Date().toISOString().slice(0, 10)
  const memberCountByPjtId = new Map<string, number>()
  for (const a of assignments.items) {
    if (a.ASGN_STRT_DT > today || (a.ASGN_END_DT !== null && a.ASGN_END_DT < today)) continue
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

      <ProjectFormModal open={openCreate} onOpenChange={setOpenCreate} onSaved={reload} />
    </div>
  )
}
