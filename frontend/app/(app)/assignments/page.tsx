'use client'

import { useEffect, useMemo, useState } from 'react'
import { AlertTriangle, Plus } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { FilterBar, FilterField } from '@/components/common/filter-bar'
import { SearchInput } from '@/components/common/search-input'
import { DataTable, type Column } from '@/components/common/data-table'
import { Select } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { UtilizationBar } from '@/components/common/utilization-progress'
import { AssignmentTypeBadge } from '@/components/common/status-badge'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { apiGet, apiPost, ApiError } from '@/lib/api'
import { assignmentTypeOptions, assignmentStatusOptions } from '@/lib/options'
import { assignmentStatusLabel } from '@/lib/labels'
import type { AssignmentType, AssignmentStatus } from '@/lib/types'

// 백엔드 투입 관리 API(로드맵 §8 "투입 관리 화면 구현", SCR-009) 응답 타입 — 필드명은
// backend/app/schemas/pjt_asgn_his.py와 동일하게 유지한다.
interface AssignmentOut {
  ASGN_ID: string
  EMPL_ID: string
  PJT_ID: string
  ASGN_TYPE_CD: AssignmentType
  PRJT_ROLE_NM: string
  ALLOC_RT: number
  ASGN_STRT_DT: string
  ASGN_END_DT: string | null
  ASGN_STAT_CD: AssignmentStatus
}
interface AssignmentListResponse {
  items: AssignmentOut[]
}
interface EmployeeOut {
  EMPL_ID: string
  EMPL_NO: string
  EMPL_NM: string
}
interface EmployeeListResponse {
  items: EmployeeOut[]
}
interface ProjectOut {
  PJT_ID: string
  PJT_NM: string
}
interface ProjectListResponse {
  items: ProjectOut[]
}

interface AssignmentRow extends AssignmentOut {
  empNo: string
  empName: string
  projectName: string
}

const typeSelectOptions = assignmentTypeOptions.filter((o) => o.value !== 'ALL')
const statusSelectOptions = assignmentStatusOptions.filter((o) => o.value !== 'ALL')

async function loadAssignments(): Promise<{ rows: AssignmentRow[]; employees: EmployeeOut[]; projects: ProjectOut[] }> {
  const [assignmentsRes, employeesRes, projectsRes] = await Promise.all([
    apiGet<AssignmentListResponse>('/api/v1/assignments?limit=200'),
    apiGet<EmployeeListResponse>('/api/v1/employees?limit=200'),
    apiGet<ProjectListResponse>('/api/v1/projects?limit=200'),
  ])

  const employeeById = new Map(employeesRes.items.map((e) => [e.EMPL_ID, e]))
  const projectById = new Map(projectsRes.items.map((p) => [p.PJT_ID, p]))

  const rows = assignmentsRes.items.map((a) => {
    const employee = employeeById.get(a.EMPL_ID)
    return {
      ...a,
      empNo: employee?.EMPL_NO ?? '-',
      empName: employee?.EMPL_NM ?? a.EMPL_ID,
      projectName: projectById.get(a.PJT_ID)?.PJT_NM ?? a.PJT_ID,
    }
  })

  return { rows, employees: employeesRes.items, projects: projectsRes.items }
}

export default function AssignmentsPage() {
  const [keyword, setKeyword] = useState('')
  const [type, setType] = useState('ALL')
  const [status, setStatus] = useState('ALL')
  const [rows, setRows] = useState<AssignmentRow[]>([])
  const [employees, setEmployees] = useState<EmployeeOut[]>([])
  const [projects, setProjects] = useState<ProjectOut[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [openCreate, setOpenCreate] = useState(false)

  function reload() {
    setLoading(true)
    loadAssignments()
      .then((result) => {
        setRows(result.rows)
        setEmployees(result.employees)
        setProjects(result.projects)
        setError(null)
      })
      .catch(() => setError('투입 이력을 불러오지 못했습니다. 잠시 후 다시 시도하세요.'))
      .finally(() => setLoading(false))
  }

  useEffect(reload, [])

  // 투입률 합계가 100%를 초과하는 사원 탐지 — 진행 중(ACTIVE)인 투입 건 기준
  const overAllocated = useMemo(() => {
    const totalByEmpNo = new Map<string, { name: string; total: number }>()
    for (const r of rows) {
      if (r.ASGN_STAT_CD !== 'ACTIVE') continue
      const prev = totalByEmpNo.get(r.empNo) ?? { name: r.empName, total: 0 }
      prev.total += r.ALLOC_RT
      totalByEmpNo.set(r.empNo, prev)
    }
    return [...totalByEmpNo.entries()]
      .filter(([, v]) => v.total > 100)
      .map(([empNo, v]) => ({ empNo, name: v.name, total: v.total }))
  }, [rows])

  const filtered = useMemo(
    () =>
      rows.filter((a) => {
        if (
          keyword &&
          !`${a.empName}${a.projectName}${a.PRJT_ROLE_NM}`.toLowerCase().includes(keyword.toLowerCase())
        )
          return false
        if (type !== 'ALL' && a.ASGN_TYPE_CD !== type) return false
        if (status !== 'ALL' && a.ASGN_STAT_CD !== status) return false
        return true
      }),
    [rows, keyword, type, status],
  )

  const columns: Column<AssignmentRow>[] = [
    {
      key: 'name',
      header: '사원',
      render: (a) => (
        <div>
          <p className="font-medium text-foreground">{a.empName}</p>
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
          <p className="text-xs text-muted-foreground">{a.PRJT_ROLE_NM}</p>
        </div>
      ),
    },
    { key: 'type', header: '투입 유형', render: (a) => <AssignmentTypeBadge type={a.ASGN_TYPE_CD} /> },
    {
      key: 'allocation',
      header: '투입률',
      className: 'w-40',
      render: (a) => <UtilizationBar value={a.ALLOC_RT} />,
    },
    {
      key: 'period',
      header: '투입 기간',
      render: (a) => (
        <span className="text-xs tabular-nums text-muted-foreground">
          {a.ASGN_STRT_DT} ~ {a.ASGN_END_DT ?? '-'}
        </span>
      ),
    },
    {
      key: 'status',
      header: '상태',
      render: (a) => (
        <Badge variant={a.ASGN_STAT_CD === 'ACTIVE' ? 'success' : 'muted'}>
          {assignmentStatusLabel[a.ASGN_STAT_CD]}
        </Badge>
      ),
    },
  ]

  return (
    <div>
      <PageHeader
        title="투입 관리"
        description="전사 투입 현황을 조회하고 공수 초과 배정을 모니터링합니다."
      >
        <Button onClick={() => setOpenCreate(true)}>
          <Plus className="size-4" />투입 등록
        </Button>
      </PageHeader>

      {error && <p className="mb-4 text-sm text-destructive">{error}</p>}

      {overAllocated.length > 0 && (
        <div className="mb-6 flex items-start gap-3 rounded-lg border border-[#f3c9c9] bg-[#fdf2f2] p-4">
          <AlertTriangle className="mt-0.5 size-5 shrink-0 text-[#c0392b]" />
          <div className="text-sm">
            <p className="font-semibold text-[#c0392b]">공수 초과 배정 감지</p>
            <p className="mt-0.5 text-[#a13a30]">
              {overAllocated.map((e) => `${e.name} (${e.total}%)`).join(', ')} — 진행 중(ACTIVE) 투입률
              합계가 100%를 초과합니다. 배정 조정이 필요합니다.
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
        rowKey={(a) => a.ASGN_ID}
        emptyTitle={loading ? '불러오는 중입니다...' : '조건에 맞는 투입 이력이 없습니다'}
        footer={
          <span>
            전체 {rows.length}건 중 {filtered.length}건 표시
          </span>
        }
      />

      <AssignmentFormModal
        open={openCreate}
        onClose={() => setOpenCreate(false)}
        employees={employees}
        projects={projects}
        onSaved={reload}
      />
    </div>
  )
}

function AssignmentFormModal({
  open,
  onClose,
  employees,
  projects,
  onSaved,
}: {
  open: boolean
  onClose: () => void
  employees: EmployeeOut[]
  projects: ProjectOut[]
  onSaved: () => void
}) {
  const employeeOptions = employees.map((e) => ({ label: `${e.EMPL_NM} (${e.EMPL_NO})`, value: e.EMPL_ID }))
  const projectOptions = projects.map((p) => ({ label: p.PJT_NM, value: p.PJT_ID }))

  const [empId, setEmpId] = useState('')
  const [pjtId, setPjtId] = useState('')
  const [type, setType] = useState(typeSelectOptions[0].value)
  const [role, setRole] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [allocRt, setAllocRt] = useState('100')
  const [remark, setRemark] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  function reset() {
    setEmpId('')
    setPjtId('')
    setType(typeSelectOptions[0].value)
    setRole('')
    setStartDate('')
    setEndDate('')
    setAllocRt('100')
    setRemark('')
    setFormError(null)
  }

  async function handleSubmit() {
    setSubmitting(true)
    setFormError(null)
    try {
      await apiPost('/api/v1/assignments', {
        EMPL_ID: empId,
        PJT_ID: pjtId,
        ASGN_TYPE_CD: type,
        PRJT_ROLE_NM: role,
        ALLOC_RT: Number(allocRt),
        ASGN_STRT_DT: startDate,
        ASGN_END_DT: endDate || null,
        RMRK: remark || null,
      })
      onSaved()
      reset()
      onClose()
    } catch (err) {
      // 동일 사원·겹치는 기간 ALLOC_RT 합계 100% 초과 시 백엔드가 409를 반환한다 —
      // 서버 검증 메시지를 그대로 보여준다.
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
      title="투입 등록"
      submitText="등록"
      onSubmit={handleSubmit}
      submitDisabled={submitting || !empId || !pjtId || !role.trim() || !startDate || !allocRt}
    >
      <div className="flex flex-col gap-4">
        {formError && <p className="text-sm text-destructive">{formError}</p>}
        <FormField label="사원" required>
          <Select value={empId} onValueChange={setEmpId} options={employeeOptions} placeholder="사원 선택" />
        </FormField>
        <FormField label="프로젝트" required>
          <Select value={pjtId} onValueChange={setPjtId} options={projectOptions} placeholder="프로젝트 선택" />
        </FormField>
        <FormField label="프로젝트 유형" required>
          <Select value={type} onValueChange={setType} options={typeSelectOptions} />
        </FormField>
        <FormField label="프로젝트 내 역할" required>
          <Input value={role} onChange={(e) => setRole(e.target.value)} placeholder="예: 리드개발, 분석, 참여" />
        </FormField>
        <div className="grid grid-cols-2 gap-4">
          <FormField label="투입 시작일" required>
            <Input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </FormField>
          <FormField label="투입 종료 예정일">
            <Input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </FormField>
        </div>
        <FormField label="투입률(%)" required>
          <Input type="number" min={0} max={100} value={allocRt} onChange={(e) => setAllocRt(e.target.value)} />
        </FormField>
        <FormField label="비고">
          <Textarea value={remark} onChange={(e) => setRemark(e.target.value)} rows={2} />
        </FormField>
      </div>
    </ModalForm>
  )
}
