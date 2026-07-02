'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { UserPlus, Users } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { FilterBar, FilterField } from '@/components/common/filter-bar'
import { SearchInput } from '@/components/common/search-input'
import { DataTable, type Column } from '@/components/common/data-table'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Avatar } from '@/components/ui/avatar'
import { EmployeeStatusBadge } from '@/components/common/status-badge'
import { UtilizationBar } from '@/components/common/utilization-progress'
import { EmployeeFormModal } from '@/components/employees/employee-form-modal'
import { employees, positions } from '@/lib/mock-data'
import { teamLabel } from '@/lib/labels'
import {
  teamOptions,
  positionOptions,
  employeeStatusOptions,
  roleOptions,
} from '@/lib/options'
import type { Employee } from '@/lib/types'

const positionName = (code: string) =>
  positions.find((p) => p.code === code)?.name ?? code

export default function EmployeesPage() {
  const router = useRouter()
  const [keyword, setKeyword] = useState('')
  const [team, setTeam] = useState('ALL')
  const [position, setPosition] = useState('ALL')
  const [status, setStatus] = useState('ALL')
  const [role, setRole] = useState('ALL')
  const [openCreate, setOpenCreate] = useState(false)

  const filtered = useMemo(() => {
    return employees.filter((e) => {
      if (keyword && !`${e.name}${e.empNo}${e.email}`.toLowerCase().includes(keyword.toLowerCase()))
        return false
      if (team !== 'ALL' && e.team !== team) return false
      if (position !== 'ALL' && e.position !== position) return false
      if (status !== 'ALL' && e.status !== status) return false
      if (role !== 'ALL' && !e.roles.includes(role)) return false
      return true
    })
  }, [keyword, team, position, status, role])

  const columns: Column<Employee>[] = [
    {
      key: 'name',
      header: '사원',
      render: (e) => (
        <div className="flex items-center gap-3">
          <Avatar name={e.name} />
          <div>
            <p className="font-medium text-foreground">{e.name}</p>
            <p className="text-xs text-muted-foreground">{e.empNo}</p>
          </div>
        </div>
      ),
    },
    {
      key: 'team',
      header: '조직',
      render: (e) => <span className="text-sm">{teamLabel[e.team]}</span>,
    },
    {
      key: 'position',
      header: '직급',
      render: (e) => <span className="text-sm">{positionName(e.position)}</span>,
    },
    {
      key: 'roles',
      header: '보유 역할',
      render: (e) => (
        <div className="flex flex-wrap gap-1">
          {e.roles.map((r) => (
            <Badge key={r} variant="soft">
              {r}
            </Badge>
          ))}
        </div>
      ),
    },
    {
      key: 'allocation',
      header: '현재 가동률',
      className: 'w-40',
      render: (e) => <UtilizationBar value={e.allocation} />,
    },
    {
      key: 'available',
      header: '가동 가능일',
      render: (e) => (
        <span className="text-sm tabular-nums text-muted-foreground">
          {e.availableDate}
        </span>
      ),
    },
    {
      key: 'status',
      header: '상태',
      render: (e) => <EmployeeStatusBadge status={e.status} />,
    },
  ]

  return (
    <div>
      <PageHeader
        title="사원 관리"
        description="구성원 정보와 보유 역량, 현재 가동 현황을 관리합니다."
      >
        <Button onClick={() => setOpenCreate(true)}>
          <UserPlus className="size-4" />
          사원 등록
        </Button>
      </PageHeader>

      <FilterBar>
        <FilterField label="검색" className="min-w-56 flex-1">
          <SearchInput
            value={keyword}
            onChange={setKeyword}
            placeholder="이름 · 사번 · 이메일 검색"
          />
        </FilterField>
        <FilterField label="조직">
          <Select value={team} onValueChange={setTeam} options={teamOptions} />
        </FilterField>
        <FilterField label="직급">
          <Select value={position} onValueChange={setPosition} options={positionOptions} />
        </FilterField>
        <FilterField label="보유 역할">
          <Select value={role} onValueChange={setRole} options={roleOptions} />
        </FilterField>
        <FilterField label="재직 상태">
          <Select value={status} onValueChange={setStatus} options={employeeStatusOptions} />
        </FilterField>
      </FilterBar>

      <DataTable
        columns={columns}
        data={filtered}
        rowKey={(e) => e.id}
        onRowClick={(e) => router.push(`/employees/${e.id}`)}
        emptyTitle="조건에 맞는 사원이 없습니다"
        emptyDescription="검색어나 필터를 조정해 보세요."
        footer={
          <>
            <span className="inline-flex items-center gap-1.5">
              <Users className="size-3.5" />전체 {employees.length}명 중 {filtered.length}명 표시
            </span>
            <span>1 / 1 페이지</span>
          </>
        }
      />

      <EmployeeFormModal open={openCreate} onOpenChange={setOpenCreate} />
    </div>
  )
}
