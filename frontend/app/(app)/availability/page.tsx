'use client'

import { useEffect, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Zap, Clock, CalendarClock } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { StatCard } from '@/components/common/stat-card'
import { SearchInput } from '@/components/common/search-input'
import { UtilizationBar } from '@/components/common/utilization-progress'
import { EmptyState } from '@/components/common/empty-state'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs } from '@/components/ui/tabs'
import { Select } from '@/components/ui/select'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { apiGet } from '@/lib/api'

// 백엔드 가동 가능 인력 API(로드맵 §8 "가동 가능 인력 조회 화면 구현", SCR-010) 응답 타입 —
// 필드명은 backend/app/schemas/hr_avail_snap.py, hr_empl_mst.py와 동일하게 유지한다.
interface AvailabilityCalcOut {
  EMPL_ID: string
  SNAP_DT: string
  TOT_ALLOC_RT: number
  AVAIL_RT: number
  AVAIL_STRT_DT: string | null
  AVAIL_STAT_CD: 'AVAILABLE' | 'PARTIAL' | 'FULL'
  DATA_QUALITY_WARNING: boolean
}
interface EmployeeOut {
  EMPL_ID: string
  EMPL_NO: string
  EMPL_NM: string
  DEPT_ID: string
  JIKMU_ID: string | null
}
interface EmployeeListResponse {
  items: EmployeeOut[]
}
interface DepartmentOut {
  DEPT_ID: string
  DEPT_NM: string
}
interface JobTypeOut {
  JIKMU_ID: string
  JIKMU_NM: string
}
interface SkillOut {
  SKILL_ID: string
  SKILL_NM: string
}
interface EmployeeSkillOut {
  EMPL_ID: string
  SKILL_ID: string
}

// 화면 탭(즉시/부분/기간 가동)은 백엔드 AVAIL_STAT_CD와 1:1로 대응한다
// (AVAILABLE=즉시, PARTIAL=부분, FULL=기간 종료 후 가동 — AVAILABILITY_CALC_SPEC.md §4 참조).
type AvailabilityTab = 'AVAILABLE' | 'PARTIAL' | 'FULL'
const TAB_DESC: Record<AvailabilityTab, string> = {
  AVAILABLE: '현재 미투입 상태로 즉시 배정 가능한 인력',
  PARTIAL: '잔여 공수로 추가 투입이 가능한 인력',
  FULL: '진행 프로젝트 종료 후 가동 가능한 인력',
}

interface AvailabilityRow extends AvailabilityCalcOut {
  empNo: string
  empName: string
  deptName: string
  jobTypeName: string | null
  skillNames: string[]
}

async function loadAvailability(): Promise<{ rows: AvailabilityRow[]; departments: DepartmentOut[]; jobTypes: JobTypeOut[] }> {
  const [availability, employeesRes, departments, jobTypes, skills, employeeSkills] = await Promise.all([
    apiGet<AvailabilityCalcOut[]>('/api/v1/availability'),
    apiGet<EmployeeListResponse>('/api/v1/employees?limit=200'),
    apiGet<DepartmentOut[]>('/api/v1/departments'),
    apiGet<JobTypeOut[]>('/api/v1/job-types'),
    apiGet<SkillOut[]>('/api/v1/skills'),
    apiGet<EmployeeSkillOut[]>('/api/v1/employee-skills'),
  ])

  const employeeById = new Map(employeesRes.items.map((e) => [e.EMPL_ID, e]))
  const deptById = new Map(departments.map((d) => [d.DEPT_ID, d]))
  const jobTypeById = new Map(jobTypes.map((j) => [j.JIKMU_ID, j]))
  const skillNameById = new Map(skills.map((s) => [s.SKILL_ID, s.SKILL_NM]))
  const skillNamesByEmpId = new Map<string, string[]>()
  for (const es of employeeSkills) {
    const name = skillNameById.get(es.SKILL_ID)
    if (!name) continue
    const list = skillNamesByEmpId.get(es.EMPL_ID) ?? []
    list.push(name)
    skillNamesByEmpId.set(es.EMPL_ID, list)
  }

  const rows = availability.map((a) => {
    const employee = employeeById.get(a.EMPL_ID)
    return {
      ...a,
      empNo: employee?.EMPL_NO ?? '-',
      empName: employee?.EMPL_NM ?? a.EMPL_ID,
      deptName: employee ? (deptById.get(employee.DEPT_ID)?.DEPT_NM ?? '-') : '-',
      jobTypeName: employee?.JIKMU_ID ? (jobTypeById.get(employee.JIKMU_ID)?.JIKMU_NM ?? null) : null,
      skillNames: skillNamesByEmpId.get(a.EMPL_ID) ?? [],
    }
  })

  return { rows, departments, jobTypes }
}

export default function AvailabilityPage() {
  const router = useRouter()
  const [tab, setTab] = useState<AvailabilityTab>('AVAILABLE')
  const [query, setQuery] = useState('')
  const [dept, setDept] = useState('ALL')
  const [jobType, setJobType] = useState('ALL')
  const [rows, setRows] = useState<AvailabilityRow[]>([])
  const [departments, setDepartments] = useState<DepartmentOut[]>([])
  const [jobTypes, setJobTypes] = useState<JobTypeOut[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAvailability()
      .then((result) => {
        setRows(result.rows)
        setDepartments(result.departments)
        setJobTypes(result.jobTypes)
        setError(null)
      })
      .catch(() => setError('가동 가능 인력 목록을 불러오지 못했습니다. 잠시 후 다시 시도하세요.'))
      .finally(() => setLoading(false))
  }, [])

  const deptOptions = useMemo(
    () => [{ label: '전체', value: 'ALL' }, ...departments.map((d) => ({ label: d.DEPT_NM, value: d.DEPT_ID }))],
    [departments],
  )
  const jobTypeOptions = useMemo(
    () => [{ label: '전체', value: 'ALL' }, ...jobTypes.map((j) => ({ label: j.JIKMU_NM, value: j.JIKMU_ID }))],
    [jobTypes],
  )

  const counts = useMemo(
    () => ({
      AVAILABLE: rows.filter((r) => r.AVAIL_STAT_CD === 'AVAILABLE').length,
      PARTIAL: rows.filter((r) => r.AVAIL_STAT_CD === 'PARTIAL').length,
      FULL: rows.filter((r) => r.AVAIL_STAT_CD === 'FULL').length,
    }),
    [rows],
  )

  const filteredRows = useMemo(() => {
    return rows.filter((r) => {
      if (r.AVAIL_STAT_CD !== tab) return false
      if (dept !== 'ALL' && r.deptName !== deptOptions.find((o) => o.value === dept)?.label) return false
      if (jobType !== 'ALL' && r.jobTypeName !== jobTypeOptions.find((o) => o.value === jobType)?.label) return false
      if (
        query &&
        !r.empName.includes(query) &&
        !r.skillNames.some((s) => s.toLowerCase().includes(query.toLowerCase())) &&
        !(r.jobTypeName ?? '').toLowerCase().includes(query.toLowerCase())
      )
        return false
      return true
    })
  }, [rows, tab, dept, deptOptions, jobType, jobTypeOptions, query])

  return (
    <div className="flex flex-col gap-6 p-6">
      <PageHeader
        title="가동 가능 인력"
        description="투입 가능 시점별로 인력 풀을 조회하여 신규 프로젝트 배정에 활용합니다."
      />

      {error && <p className="text-sm text-destructive">{error}</p>}

      <div className="grid gap-4 sm:grid-cols-3">
        <StatCard label="즉시 가동 가능" value={`${counts.AVAILABLE}명`} icon={Zap} tone="success" />
        <StatCard label="부분 가동 가능" value={`${counts.PARTIAL}명`} icon={Clock} tone="info" />
        <StatCard label="기간 종료 예정" value={`${counts.FULL}명`} icon={CalendarClock} tone="warning" />
      </div>

      <Card>
        <CardContent className="flex flex-col gap-4 pt-6">
          <Tabs
            value={tab}
            onValueChange={(v) => setTab(v as AvailabilityTab)}
            tabs={[
              { value: 'AVAILABLE', label: `즉시 가동 (${counts.AVAILABLE})` },
              { value: 'PARTIAL', label: `부분 가동 (${counts.PARTIAL})` },
              { value: 'FULL', label: `종료 예정 (${counts.FULL})` },
            ]}
          />

          <p className="text-sm text-muted-foreground">{TAB_DESC[tab]}</p>

          <div className="flex flex-col gap-3 sm:flex-row">
            <SearchInput
              value={query}
              onChange={setQuery}
              placeholder="이름 · 직무 · 기술 검색"
              className="sm:max-w-xs"
            />
            <Select
              value={jobType}
              onValueChange={setJobType}
              options={jobTypeOptions}
              placeholder="직무 유형 전체"
              className="sm:w-48"
            />
            <Select
              value={dept}
              onValueChange={setDept}
              options={deptOptions}
              placeholder="조직 전체"
              className="sm:w-48"
            />
          </div>

          {filteredRows.length === 0 ? (
            <EmptyState
              title={loading ? '불러오는 중입니다...' : '조건에 맞는 인력이 없습니다'}
              description={loading ? undefined : '검색어나 조직 필터를 조정해 보세요.'}
            />
          ) : (
            <div className="overflow-hidden rounded-lg border border-border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>이름</TableHead>
                    <TableHead>조직</TableHead>
                    <TableHead>직무</TableHead>
                    <TableHead>보유 기술</TableHead>
                    <TableHead className="w-40">현재 가동률</TableHead>
                    <TableHead>가동 가능일</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredRows.map((r) => (
                    <TableRow
                      key={r.EMPL_ID}
                      className="cursor-pointer"
                      onClick={() => router.push(`/employees/${r.EMPL_ID}`)}
                    >
                      <TableCell>
                        <span className="font-medium text-primary">{r.empName}</span>
                        <span className="ml-2 font-mono text-xs text-muted-foreground">{r.empNo}</span>
                      </TableCell>
                      <TableCell className="text-muted-foreground">{r.deptName}</TableCell>
                      <TableCell>{r.jobTypeName ?? '-'}</TableCell>
                      <TableCell>
                        <div className="flex flex-wrap gap-1">
                          {r.skillNames.length === 0 ? (
                            <span className="text-xs text-muted-foreground">-</span>
                          ) : (
                            r.skillNames.map((s) => (
                              <Badge key={s} variant="secondary">
                                {s}
                              </Badge>
                            ))
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <UtilizationBar value={r.TOT_ALLOC_RT} />
                      </TableCell>
                      <TableCell>
                        <Badge variant={r.AVAIL_STAT_CD === 'AVAILABLE' ? 'success' : 'outline'}>
                          {r.AVAIL_STAT_CD === 'AVAILABLE'
                            ? '오늘'
                            : (r.AVAIL_STRT_DT ?? (r.DATA_QUALITY_WARNING ? '미정 (데이터 확인 필요)' : '-'))}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
