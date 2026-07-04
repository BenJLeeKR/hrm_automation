'use client'

import { useEffect, useMemo, useState } from 'react'
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
import { employeeStatusOptions } from '@/lib/options'
import type { EmployeeStatus } from '@/lib/types'
import { apiDownloadFile, apiGet, ApiError } from '@/lib/api'

// 백엔드 사원 목록 관련 API 응답 타입(로드맵 §8 "사원 목록 화면 실 API 연동") — 필드명은
// backend/app/schemas/*.py와 동일하게 유지한다.
interface EmployeeOut {
  EMPL_ID: string
  EMPL_NO: string
  EMPL_NM: string
  DEPT_ID: string
  JIKGUP_ID: string
  JIKMU_ID: string | null
  EMPL_STAT_CD: EmployeeStatus
  EMAIL_ADDR: string | null
}
interface EmployeeListResponse {
  items: EmployeeOut[]
  total: number
}
interface DepartmentOut {
  DEPT_ID: string
  DEPT_NM: string
}
interface PositionOut {
  JIKGUP_ID: string
  JIKGUP_NM: string
}
interface JobTypeOut {
  JIKMU_ID: string
  JIKMU_NM: string
}
interface EmployeeRoleOut {
  EMPL_ID: string
  JIKMU_ID: string
}
interface AvailabilityCalcOut {
  EMPL_ID: string
  TOT_ALLOC_RT: number
  AVAIL_STAT_CD: 'AVAILABLE' | 'PARTIAL' | 'FULL'
  AVAIL_STRT_DT: string | null
  DATA_QUALITY_WARNING: boolean
}

interface EmployeeRow extends EmployeeOut {
  deptName: string
  positionName: string
  roleNames: string[]
  allocation: number
  availableDate: string
}

async function loadEmployees(): Promise<{
  rows: EmployeeRow[]
  departments: DepartmentOut[]
  positions: PositionOut[]
  jobTypes: JobTypeOut[]
}> {
  const [employeesRes, departments, positions, jobTypes, employeeRoles, availability] = await Promise.all([
    apiGet<EmployeeListResponse>('/api/v1/employees?limit=200'),
    apiGet<DepartmentOut[]>('/api/v1/departments'),
    apiGet<PositionOut[]>('/api/v1/positions'),
    apiGet<JobTypeOut[]>('/api/v1/job-types'),
    apiGet<EmployeeRoleOut[]>('/api/v1/employee-roles'),
    apiGet<AvailabilityCalcOut[]>('/api/v1/availability'),
  ])

  const deptById = new Map(departments.map((d) => [d.DEPT_ID, d.DEPT_NM]))
  const positionById = new Map(positions.map((p) => [p.JIKGUP_ID, p.JIKGUP_NM]))
  const jobTypeById = new Map(jobTypes.map((j) => [j.JIKMU_ID, j.JIKMU_NM]))
  const availByEmplId = new Map(availability.map((a) => [a.EMPL_ID, a]))
  const roleNamesByEmplId = new Map<string, string[]>()
  for (const r of employeeRoles) {
    const name = jobTypeById.get(r.JIKMU_ID)
    if (!name) continue
    const list = roleNamesByEmplId.get(r.EMPL_ID) ?? []
    list.push(name)
    roleNamesByEmplId.set(r.EMPL_ID, list)
  }

  const rows = employeesRes.items.map((e) => {
    const avail = availByEmplId.get(e.EMPL_ID)
    return {
      ...e,
      deptName: deptById.get(e.DEPT_ID) ?? '-',
      positionName: positionById.get(e.JIKGUP_ID) ?? '-',
      roleNames: roleNamesByEmplId.get(e.EMPL_ID) ?? (e.JIKMU_ID ? [jobTypeById.get(e.JIKMU_ID) ?? ''] : []),
      allocation: avail?.TOT_ALLOC_RT ?? 0,
      availableDate: avail
        ? avail.AVAIL_STAT_CD === 'AVAILABLE'
          ? '즉시'
          : (avail.AVAIL_STRT_DT ?? (avail.DATA_QUALITY_WARNING ? '미정' : '-'))
        : '-',
    }
  })

  return { rows, departments, positions, jobTypes }
}

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

  const [rows, setRows] = useState<EmployeeRow[]>([])
  const [departments, setDepartments] = useState<DepartmentOut[]>([])
  const [positions, setPositions] = useState<PositionOut[]>([])
  const [jobTypes, setJobTypes] = useState<JobTypeOut[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  function reload() {
    setLoading(true)
    loadEmployees()
      .then((result) => {
        setRows(result.rows)
        setDepartments(result.departments)
        setPositions(result.positions)
        setJobTypes(result.jobTypes)
        setError(null)
      })
      .catch(() => setError('사원 목록을 불러오지 못했습니다. 잠시 후 다시 시도하세요.'))
      .finally(() => setLoading(false))
  }

  useEffect(reload, [])

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

  // 조직/직급/직무 유형 필터는 실제 마스터 데이터를 그대로 사용한다 — 하드코딩된 목록은
  // 마스터 데이터가 바뀌면(예: 부서 추가) 조용히 stale해지므로 쓰지 않는다(기술/직무유형
  // 관리 화면에서 이미 확인된 원칙과 동일).
  const teamOptions = useMemo(
    () => [{ label: '전체', value: 'ALL' }, ...departments.map((d) => ({ label: d.DEPT_NM, value: d.DEPT_ID }))],
    [departments],
  )
  const positionOptions = useMemo(
    () => [{ label: '전체', value: 'ALL' }, ...positions.map((p) => ({ label: p.JIKGUP_NM, value: p.JIKGUP_ID }))],
    [positions],
  )
  const jobTypeOptions = useMemo(
    () => [{ label: '전체', value: 'ALL' }, ...jobTypes.map((j) => ({ label: j.JIKMU_NM, value: j.JIKMU_ID }))],
    [jobTypes],
  )

  const filtered = useMemo(() => {
    return rows.filter((e) => {
      if (
        keyword &&
        !`${e.EMPL_NM}${e.EMPL_NO}${e.EMAIL_ADDR ?? ''}`.toLowerCase().includes(keyword.toLowerCase())
      )
        return false
      if (team !== 'ALL' && e.DEPT_ID !== team) return false
      if (position !== 'ALL' && e.JIKGUP_ID !== position) return false
      if (status !== 'ALL' && e.EMPL_STAT_CD !== status) return false
      if (jobType !== 'ALL' && e.JIKMU_ID !== jobType) return false
      return true
    })
  }, [rows, keyword, team, position, status, jobType])

  const columns: Column<EmployeeRow>[] = [
    {
      key: 'name',
      header: '사원',
      render: (e) => (
        <div className="flex items-center gap-3">
          <Avatar name={e.EMPL_NM} />
          <div>
            <p className="font-medium text-foreground">{e.EMPL_NM}</p>
            <p className="text-xs text-muted-foreground">{e.EMPL_NO}</p>
          </div>
        </div>
      ),
    },
    {
      key: 'team',
      header: '조직',
      render: (e) => <span className="text-sm">{e.deptName}</span>,
    },
    {
      key: 'position',
      header: '직급',
      render: (e) => <span className="text-sm">{e.positionName}</span>,
    },
    {
      key: 'roles',
      header: '보유 역할',
      render: (e) => (
        <div className="flex flex-wrap gap-1">
          {e.roleNames.length === 0 ? (
            <span className="text-xs text-muted-foreground">-</span>
          ) : (
            e.roleNames.map((r) => (
              <Badge key={r} variant="soft">
                {r}
              </Badge>
            ))
          )}
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
      render: (e) => <EmployeeStatusBadge status={e.EMPL_STAT_CD} />,
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

      {error && <p className="mb-4 text-sm text-destructive">{error}</p>}
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
        rowKey={(e) => e.EMPL_ID}
        onRowClick={(e) => router.push(`/employees/${e.EMPL_ID}`)}
        emptyTitle={loading ? '불러오는 중입니다...' : '조건에 맞는 사원이 없습니다'}
        emptyDescription={loading ? undefined : '검색어나 필터를 조정해 보세요.'}
        footer={
          <>
            <span className="inline-flex items-center gap-1.5">
              <Users className="size-3.5" />전체 {rows.length}명 중 {filtered.length}명 표시
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
