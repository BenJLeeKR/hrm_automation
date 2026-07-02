'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { FolderPlus, Users2, CalendarRange } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { FilterBar, FilterField } from '@/components/common/filter-bar'
import { SearchInput } from '@/components/common/search-input'
import { DataTable, type Column } from '@/components/common/data-table'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { ProjectStatusBadge } from '@/components/common/status-badge'
import { ProjectFormModal } from '@/components/projects/project-form-modal'
import { projects } from '@/lib/mock-data'
import { projectStatusOptions } from '@/lib/options'
import type { Project } from '@/lib/types'

export default function ProjectsPage() {
  const router = useRouter()
  const [keyword, setKeyword] = useState('')
  const [status, setStatus] = useState('ALL')
  const [openCreate, setOpenCreate] = useState(false)

  const filtered = useMemo(
    () =>
      projects.filter((p) => {
        if (
          keyword &&
          !`${p.name}${p.client}${p.code}`.toLowerCase().includes(keyword.toLowerCase())
        )
          return false
        if (status !== 'ALL' && p.status !== status) return false
        return true
      }),
    [keyword, status],
  )

  const columns: Column<Project>[] = [
    {
      key: 'name',
      header: '프로젝트',
      render: (p) => (
        <div>
          <p className="font-medium text-foreground">{p.name}</p>
          <p className="text-xs text-muted-foreground">{p.code}</p>
        </div>
      ),
    },
    { key: 'client', header: '고객사', render: (p) => <span className="text-sm">{p.client}</span> },
    {
      key: 'period',
      header: '수행 기간',
      render: (p) => (
        <span className="inline-flex items-center gap-1.5 text-sm tabular-nums text-muted-foreground">
          <CalendarRange className="size-3.5" />
          {p.startDate} ~ {p.endDate}
        </span>
      ),
    },
    {
      key: 'members',
      header: '투입 인원',
      render: (p) => (
        <span className="inline-flex items-center gap-1 text-sm tabular-nums">
          <Users2 className="size-3.5 text-muted-foreground" />
          {p.memberCount}명
        </span>
      ),
    },
    { key: 'status', header: '상태', render: (p) => <ProjectStatusBadge status={p.status} /> },
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
        rowKey={(p) => p.id}
        onRowClick={(p) => router.push(`/projects/${p.id}`)}
        emptyTitle="조건에 맞는 프로젝트가 없습니다"
        footer={<span>전체 {projects.length}건 중 {filtered.length}건 표시</span>}
      />

      <ProjectFormModal open={openCreate} onOpenChange={setOpenCreate} />
    </div>
  )
}
