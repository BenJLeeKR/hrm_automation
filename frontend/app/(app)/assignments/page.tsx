'use client'

import { useMemo, useState } from 'react'
import { AlertTriangle } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { FilterBar, FilterField } from '@/components/common/filter-bar'
import { SearchInput } from '@/components/common/search-input'
import { DataTable, type Column } from '@/components/common/data-table'
import { Select } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { UtilizationBar } from '@/components/common/utilization-progress'
import { AssignmentTypeBadge } from '@/components/common/status-badge'
import { assignments, employees } from '@/lib/mock-data'
import { assignmentTypeOptions, assignmentStatusOptions } from '@/lib/options'
import { assignmentStatusLabel } from '@/lib/labels'
import type { Assignment } from '@/lib/types'

export default function AssignmentsPage() {
  const [keyword, setKeyword] = useState('')
  const [type, setType] = useState('ALL')
  const [status, setStatus] = useState('ALL')

  // 투입률 합계가 100%를 초과하는 사원 탐지
  const overAllocated = useMemo(
    () => employees.filter((e) => e.allocation > 100),
    [],
  )

  const filtered = useMemo(
    () =>
      assignments.filter((a) => {
        if (
          keyword &&
          !`${a.name}${a.projectName}${a.role}`
            .toLowerCase()
            .includes(keyword.toLowerCase())
        )
          return false
        if (type !== 'ALL' && a.type !== type) return false
        if (status !== 'ALL' && a.status !== status) return false
        return true
      }),
    [keyword, type, status],
  )

  const columns: Column<Assignment>[] = [
    {
      key: 'name',
      header: '사원',
      render: (a) => (
        <div>
          <p className="font-medium text-foreground">{a.name}</p>
          <p className="font-mono text-xs text-muted-foreground">{a.empNo}</p>
        </div>
      ),
    },
    {
      key: 'project',
      header: '프로젝트 / 역할',
      render: (a) => (
        <div>
          <p className="text-sm text-foreground">{a.projectName}</p>
          <p className="text-xs text-muted-foreground">{a.role}</p>
        </div>
      ),
    },
    { key: 'type', header: '투입 유형', render: (a) => <AssignmentTypeBadge type={a.type} /> },
    {
      key: 'allocation',
      header: '투입률',
      className: 'w-40',
      render: (a) => <UtilizationBar value={a.allocation} />,
    },
    {
      key: 'period',
      header: '투입 기간',
      render: (a) => (
        <span className="text-xs tabular-nums text-muted-foreground">
          {a.startDate} ~ {a.endDate}
        </span>
      ),
    },
    {
      key: 'status',
      header: '상태',
      render: (a) => (
        <Badge variant={a.status === 'ACTIVE' ? 'success' : 'muted'}>
          {assignmentStatusLabel[a.status]}
        </Badge>
      ),
    },
  ]

  return (
    <div>
      <PageHeader
        title="투입 관리"
        description="전사 투입 현황을 조회하고 공수 초과 배정을 모니터링합니다."
      />

      {overAllocated.length > 0 && (
        <div className="mb-6 flex items-start gap-3 rounded-lg border border-[#f3c9c9] bg-[#fdf2f2] p-4">
          <AlertTriangle className="mt-0.5 size-5 shrink-0 text-[#c0392b]" />
          <div className="text-sm">
            <p className="font-semibold text-[#c0392b]">공수 초과 배정 감지</p>
            <p className="mt-0.5 text-[#a13a30]">
              {overAllocated
                .map((e) => `${e.name} (${e.allocation}%)`)
                .join(', ')}{' '}
              — 투입률 합계가 100%를 초과합니다. 배정 조정이 필요합니다.
            </p>
          </div>
        </div>
      )}

      <FilterBar>
        <FilterField label="검색" className="min-w-56 flex-1">
          <SearchInput
            value={keyword}
            onChange={setKeyword}
            placeholder="사원명 · 프로젝트 · 역할 검색"
          />
        </FilterField>
        <FilterField label="투입 유형">
          <Select value={type} onValueChange={setType} options={assignmentTypeOptions} />
        </FilterField>
        <FilterField label="상태">
          <Select
            value={status}
            onValueChange={setStatus}
            options={assignmentStatusOptions}
          />
        </FilterField>
      </FilterBar>

      <DataTable
        columns={columns}
        data={filtered}
        rowKey={(a) => a.id}
        emptyTitle="조건에 맞는 투입 이력이 없습니다"
        footer={
          <span>
            전체 {assignments.length}건 중 {filtered.length}건 표시
          </span>
        }
      />
    </div>
  )
}
