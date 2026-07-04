'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Download, Upload, UserPlus, Users } from 'lucide-react'
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
import { EmployeeImportDialog } from '@/components/employees/employee-import-dialog'
import { employees, positions } from '@/lib/mock-data'
import { teamLabel } from '@/lib/labels'
import {
  teamOptions,
  positionOptions,
  employeeStatusOptions,
  jobTypeOptions,
} from '@/lib/options'
import type { Employee } from '@/lib/types'
import { apiDownloadFile, ApiError } from '@/lib/api'

// 사원의 `roles`(mock-data.ts)에는 신규 JIKMU_CD(예: DEVELOPER, DEVOPS)와 구 Excel
// 코드(예: AA, TA, 컨설턴트, 사업관리)가 혼재되어 있다 — ERD `HR_JIKMU_MST` §3.3의
// "엑셀 코드 → JIKMU_CD 매핑" 규칙과 동일. 직무 유형 필터(jobTypeOptions, JIKMU_CD 기준)를
// 두 표기 모두에 대해 정상 동작시키기 위한 매핑이며, 사원 데이터가 실제 API로 전환되면
// JIKMU_ID 단일 값으로 대체되어 이 매핑은 제거 가능하다.
const JIKMU_CD_ALIASES: Record<string, string[]> = {
  ARCHITECT: ['ARCHITECT', 'AA'],
  TECH_LEAD: ['TECH_LEAD', 'TA'],
  CONSULTANT: ['CONSULTANT', '컨설턴트'],
  PMO: ['PMO', '사업관리'],
}

function matchesJobType(employeeRoles: string[], jikmuCd: string) {
  const aliases = JIKMU_CD_ALIASES[jikmuCd] ?? [jikmuCd]
  return aliases.some((code) => employeeRoles.includes(code))
}

const positionName = (code: string) =>
  positions.find((p) => p.code === code)?.name ?? code

export default function EmployeesPage() {
  const router = useRouter()
  const [keyword, setKeyword] = useState('')
  const [team, setTeam] = useState('ALL')
  const [position, setPosition] = useState('ALL')
  const [status, setStatus] = useState('ALL')
  const [jobType, setJobType] = useState('ALL')
  const [openCreate, setOpenCreate] = useState(false)
  const [openImport, setOpenImport] = useState(false)
  const [exporting, setExporting] = useState(false)
  const [exportError, setExportError] = useState<string | null>(null)

  async function handleExport() {
    setExporting(true)
    setExportError(null)
    try {
      await apiDownloadFile('/api/v1/employees/export', 'employees.xlsx')
    } catch (err) {
      setExportError(err instanceof ApiError ? err.message : 'Excel 내보내기에 실패했습니다.')
    } finally {
      setExporting(false)
    }
  }

  const filtered = useMemo(() => {
    return employees.filter((e) => {
      if (keyword && !`${e.name}${e.empNo}${e.email}`.toLowerCase().includes(keyword.toLowerCase()))
        return false
      if (team !== 'ALL' && e.team !== team) return false
      if (position !== 'ALL' && e.position !== position) return false
      if (status !== 'ALL' && e.status !== status) return false
      if (jobType !== 'ALL' && !matchesJobType(e.roles, jobType)) return false
      return true
    })
  }, [keyword, team, position, status, jobType])

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
        <Button variant="outline" onClick={() => setOpenImport(true)}>
          <Upload className="size-4" />
          Excel 가져오기
        </Button>
        <Button variant="outline" onClick={handleExport} disabled={exporting}>
          <Download className="size-4" />
          {exporting ? '내보내는 중...' : 'Excel 내보내기'}
        </Button>
        <Button onClick={() => setOpenCreate(true)}>
          <UserPlus className="size-4" />
          사원 등록
        </Button>
      </PageHeader>

      {exportError && <p className="mb-4 text-sm text-destructive">{exportError}</p>}

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
        <FilterField label="직무 유형">
          <Select value={jobType} onValueChange={setJobType} options={jobTypeOptions} />
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
      <EmployeeImportDialog open={openImport} onOpenChange={setOpenImport} />
    </div>
  )
}
