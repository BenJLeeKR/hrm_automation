'use client'

import { use, useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft, Mail, Phone, CalendarDays, Building2 } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Avatar } from '@/components/ui/avatar'
import { Tabs } from '@/components/ui/tabs'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { SkillLevel } from '@/components/common/skill-level'
import { UtilizationBar } from '@/components/common/utilization-progress'
import { EmployeeStatusBadge } from '@/components/common/status-badge'
import { EmptyState } from '@/components/common/empty-state'
import { apiGet } from '@/lib/api'
import { assignmentStatusLabel } from '@/lib/labels'
import type { EmployeeStatus } from '@/lib/types'

// 백엔드 사원 상세 관련 API 응답 타입(로드맵 §8 "사원 상세 화면 구현", SCR-004) — 필드명은
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
  MPHONE_NO: string | null
  HIRE_DT: string | null
  RETIR_DT: string | null
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
interface SkillOut {
  SKILL_ID: string
  SKILL_GRP_CD: string
  SKILL_NM: string
}
interface EmployeeSkillOut {
  EMPL_SKILL_ID: string
  SKILL_ID: string
  PRFCY_LEVL: number | null
  EXPR_YEAR: number | null
  LAST_USE_DT: string | null
}
interface ProjectOut {
  PJT_ID: string
  PJT_NM: string
}
interface ProjectListResponse {
  total: number
  items: ProjectOut[]
}
interface AssignmentOut {
  ASGN_ID: string
  PJT_ID: string
  ASGN_TYPE_CD: string
  PRJT_ROLE_NM: string
  ALLOC_RT: number
  ASGN_STRT_DT: string
  ASGN_END_DT: string | null
  ASGN_STAT_CD: 'PLANNED' | 'ACTIVE' | 'DONE' | 'CANCELED'
}
interface AssignmentListResponse {
  total: number
  items: AssignmentOut[]
}

interface EmployeeDetailData {
  employee: EmployeeOut
  deptName: string
  positionName: string
  jobTypeName: string | null
  skills: Array<EmployeeSkillOut & { skillName: string; skillGroup: string }>
  assignments: Array<AssignmentOut & { projectName: string }>
  currentUtilization: number
}

const TABS = [
  { value: 'info', label: '기본 정보' },
  { value: 'skills', label: '보유 기술' },
  { value: 'assignments', label: '투입 이력' },
]

async function loadEmployeeDetail(id: string): Promise<EmployeeDetailData> {
  const [employee, departments, positions, jobTypes, skills, employeeSkills, projects, assignments] =
    await Promise.all([
      apiGet<EmployeeOut>(`/api/v1/employees/${id}`),
      apiGet<DepartmentOut[]>('/api/v1/departments'),
      apiGet<PositionOut[]>('/api/v1/positions'),
      apiGet<JobTypeOut[]>('/api/v1/job-types'),
      apiGet<SkillOut[]>('/api/v1/skills'),
      apiGet<EmployeeSkillOut[]>(`/api/v1/employee-skills?empl_id=${id}`),
      // GET /projects는 배열이 아니라 {total, items} 페이지네이션 응답이다 — 사원 1인의
      // 투입 이력에 등장할 수 있는 프로젝트를 전부 조인하기 위해 넉넉한 limit 사용
      apiGet<ProjectListResponse>('/api/v1/projects?limit=200'),
      // 사원 1인의 투입 이력 전체를 보여주기 위해 페이지네이션 기본값(20건)보다 넉넉한 값 사용
      apiGet<AssignmentListResponse>(`/api/v1/assignments?empl_id=${id}&limit=200`),
    ])

  const skillById = new Map(skills.map((s) => [s.SKILL_ID, s]))
  const projectById = new Map(projects.items.map((p) => [p.PJT_ID, p]))
  const assignmentItems = assignments.items

  const currentUtilization = assignmentItems
    .filter((a) => a.ASGN_STAT_CD === 'ACTIVE')
    .reduce((sum, a) => sum + a.ALLOC_RT, 0)

  return {
    employee,
    deptName: departments.find((d) => d.DEPT_ID === employee.DEPT_ID)?.DEPT_NM ?? '-',
    positionName: positions.find((p) => p.JIKGUP_ID === employee.JIKGUP_ID)?.JIKGUP_NM ?? '-',
    jobTypeName: jobTypes.find((j) => j.JIKMU_ID === employee.JIKMU_ID)?.JIKMU_NM ?? null,
    skills: employeeSkills.map((es) => ({
      ...es,
      skillName: skillById.get(es.SKILL_ID)?.SKILL_NM ?? es.SKILL_ID,
      skillGroup: skillById.get(es.SKILL_ID)?.SKILL_GRP_CD ?? '-',
    })),
    assignments: assignmentItems.map((a) => ({
      ...a,
      projectName: projectById.get(a.PJT_ID)?.PJT_NM ?? a.PJT_ID,
    })),
    currentUtilization,
  }
}

export default function EmployeeDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = use(params)
  const router = useRouter()
  const [tab, setTab] = useState('info')
  const [data, setData] = useState<EmployeeDetailData | null>(null)
  const [notFound, setNotFound] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    loadEmployeeDetail(id)
      .then((result) => {
        if (!cancelled) setData(result)
      })
      .catch((err) => {
        if (cancelled) return
        if (err?.status === 404) {
          setNotFound(true)
        } else {
          setError('사원 정보를 불러오지 못했습니다. 잠시 후 다시 시도하세요.')
        }
      })
    return () => {
      cancelled = true
    }
  }, [id])

  if (notFound) {
    return (
      <div>
        <PageHeader title="사원 상세" />
        <EmptyState
          title="사원을 찾을 수 없습니다"
          description="요청하신 사원 정보가 존재하지 않습니다."
        >
          <Button variant="secondary" onClick={() => router.push('/employees')}>
            목록으로
          </Button>
        </EmptyState>
      </div>
    )
  }

  if (error) {
    return (
      <div>
        <PageHeader title="사원 상세" />
        <p className="text-sm text-destructive">{error}</p>
      </div>
    )
  }

  if (!data) {
    return (
      <div>
        <PageHeader title="사원 상세" />
        <p className="text-sm text-muted-foreground">불러오는 중입니다...</p>
      </div>
    )
  }

  const { employee, deptName, positionName, jobTypeName, skills, assignments, currentUtilization } = data

  return (
    <div>
      <Link
        href="/employees"
        className="mb-4 inline-flex items-center gap-1.5 text-sm text-muted-foreground transition-colors hover:text-foreground"
      >
        <ArrowLeft className="size-4" />
        사원 목록으로
      </Link>

      <Card className="mb-5">
        <CardContent className="pt-5">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-4">
              <Avatar name={employee.EMPL_NM} className="size-14 text-lg" />
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-xl font-bold tracking-tight">{employee.EMPL_NM}</h1>
                  <EmployeeStatusBadge status={employee.EMPL_STAT_CD} />
                </div>
                <p className="mt-0.5 text-sm text-muted-foreground">
                  {employee.EMPL_NO} · {deptName} · {positionName}
                </p>
                {jobTypeName && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    <Badge variant="soft">{jobTypeName}</Badge>
                  </div>
                )}
              </div>
            </div>
            {/* 정보 수정/퇴직 처리 버튼은 실 API 연동(PATCH/DELETE) 자체는 구현되어 있으나,
                편집 폼 UI를 이번 "사원 상세 화면 구현" 범위에서 다루지 않아 후속 작업으로
                분리했다(§9 리스크 참조) — 조회 전용 화면으로 우선 제공한다. */}
          </div>

          <div className="mt-5 grid grid-cols-2 gap-4 border-t border-border pt-5 lg:grid-cols-4">
            <InfoItem icon={Mail} label="이메일" value={employee.EMAIL_ADDR ?? '-'} />
            <InfoItem icon={Phone} label="연락처" value={employee.MPHONE_NO ?? '-'} />
            <InfoItem icon={CalendarDays} label="입사일" value={employee.HIRE_DT ?? '-'} />
            <div>
              <p className="mb-1.5 flex items-center gap-1.5 text-xs text-muted-foreground">
                <Building2 className="size-3.5" />현재 가동률
              </p>
              <UtilizationBar value={currentUtilization} />
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs tabs={TABS} value={tab} onValueChange={setTab} className="mb-4" />

      {tab === 'info' && (
        <Card>
          <CardContent className="pt-5">
            <dl className="grid grid-cols-1 gap-x-8 gap-y-4 sm:grid-cols-2">
              <Field label="사번" value={employee.EMPL_NO} />
              <Field label="이름" value={employee.EMPL_NM} />
              <Field label="조직" value={deptName} />
              <Field label="직급" value={positionName} />
              <Field label="직무 유형" value={jobTypeName ?? '-'} />
              <Field label="이메일" value={employee.EMAIL_ADDR ?? '-'} />
              <Field label="연락처" value={employee.MPHONE_NO ?? '-'} />
              <Field label="입사일" value={employee.HIRE_DT ?? '-'} />
            </dl>
          </CardContent>
        </Card>
      )}

      {tab === 'skills' && (
        <Card className="overflow-hidden p-0">
          <div className="flex items-center justify-between px-5 py-3">
            <p className="text-sm font-semibold">보유 기술 {skills.length}건</p>
          </div>
          {skills.length === 0 ? (
            <EmptyState title="등록된 기술이 없습니다" />
          ) : (
            <Table>
              <TableHeader>
                <TableRow className="hover:bg-transparent">
                  <TableHead>기술명</TableHead>
                  <TableHead>그룹</TableHead>
                  <TableHead>숙련도</TableHead>
                  <TableHead>경력(년)</TableHead>
                  <TableHead>최근 사용</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {skills.map((s) => (
                  <TableRow key={s.EMPL_SKILL_ID}>
                    <TableCell className="font-medium">{s.skillName}</TableCell>
                    <TableCell>
                      <Badge variant="secondary">{s.skillGroup}</Badge>
                    </TableCell>
                    <TableCell>
                      <SkillLevel level={s.PRFCY_LEVL ?? 0} />
                    </TableCell>
                    <TableCell className="tabular-nums">{s.EXPR_YEAR ?? '-'}</TableCell>
                    <TableCell className="tabular-nums text-muted-foreground">
                      {s.LAST_USE_DT ?? '-'}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </Card>
      )}

      {tab === 'assignments' && (
        <Card className="overflow-hidden p-0">
          {assignments.length === 0 ? (
            <EmptyState
              title="투입 이력이 없습니다"
              description="현재 이 사원은 즉시 투입 가능한 상태입니다."
            />
          ) : (
            <Table>
              <TableHeader>
                <TableRow className="hover:bg-transparent">
                  <TableHead>프로젝트</TableHead>
                  <TableHead>역할</TableHead>
                  <TableHead>투입률</TableHead>
                  <TableHead>기간</TableHead>
                  <TableHead>상태</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {assignments.map((a) => (
                  <TableRow key={a.ASGN_ID}>
                    <TableCell className="font-medium">{a.projectName}</TableCell>
                    <TableCell>{a.PRJT_ROLE_NM}</TableCell>
                    <TableCell className="tabular-nums">{a.ALLOC_RT}%</TableCell>
                    <TableCell className="tabular-nums text-muted-foreground">
                      {a.ASGN_STRT_DT} ~ {a.ASGN_END_DT ?? '-'}
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{assignmentStatusLabel[a.ASGN_STAT_CD]}</Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </Card>
      )}
    </div>
  )
}

function InfoItem({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof Mail
  label: string
  value: string
}) {
  return (
    <div>
      <p className="mb-1.5 flex items-center gap-1.5 text-xs text-muted-foreground">
        <Icon className="size-3.5" />
        {label}
      </p>
      <p className="text-sm font-medium">{value}</p>
    </div>
  )
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between border-b border-dashed border-border pb-3">
      <dt className="text-sm text-muted-foreground">{label}</dt>
      <dd className="text-sm font-medium">{value}</dd>
    </div>
  )
}
