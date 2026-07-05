'use client'

import { use, useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowLeft, Pencil, CircleOff, UserPlus } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { EmptyState } from '@/components/common/empty-state'
import { UtilizationBar } from '@/components/common/utilization-progress'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { ProjectFormModal } from '@/components/projects/project-form-modal'
import { AssignmentFormModal } from '@/components/projects/assignment-form-modal'
import { ConfirmDialog } from '@/components/common/confirm-dialog'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { apiGet, apiPatch, ApiError } from '@/lib/api'
import { assignmentTypeLabel, assignmentStatusLabel } from '@/lib/labels'

// 백엔드 프로젝트 상세 관련 API 응답 타입(로드맵 §8 "프로젝트 목록/상세 화면 구현", SCR-008) —
// 필드명은 backend/app/schemas/*.py와 동일하게 유지한다.
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
interface EmployeeOut {
  EMPL_ID: string
  EMPL_NO: string
  EMPL_NM: string
  DEPT_ID: string
  JIKMU_ID: string | null
}
interface DepartmentOut {
  DEPT_ID: string
  DEPT_NM: string
}
interface JobTypeOut {
  JIKMU_ID: string
  JIKMU_NM: string
}
interface AssignmentOut {
  ASGN_ID: string
  EMPL_ID: string
  ASGN_TYPE_CD: 'RUNNING' | 'COMMITTED' | 'PROPOSED'
  PRJT_ROLE_NM: string
  ALLOC_RT: number
  ASGN_STRT_DT: string
  ASGN_END_DT: string | null
  ASGN_STAT_CD: 'PLANNED' | 'ACTIVE' | 'DONE' | 'CANCELED'
}
interface AssignmentListResponse {
  items: AssignmentOut[]
}
interface EmployeeListResponse {
  items: EmployeeOut[]
}

interface ProjectDetailData {
  project: ProjectOut
  employees: EmployeeOut[]
  assignments: Array<AssignmentOut & { employeeName: string; deptName: string; jobTypeName: string | null }>
}

async function loadProjectDetail(id: string): Promise<ProjectDetailData> {
  const [project, assignmentsRes, employeesRes, departments, jobTypes] = await Promise.all([
    apiGet<ProjectOut>(`/api/v1/projects/${id}`),
    apiGet<AssignmentListResponse>(`/api/v1/assignments?pjt_id=${id}&limit=200`),
    apiGet<EmployeeListResponse>('/api/v1/employees?limit=200'),
    apiGet<DepartmentOut[]>('/api/v1/departments'),
    apiGet<JobTypeOut[]>('/api/v1/job-types'),
  ])

  const employeeById = new Map(employeesRes.items.map((e) => [e.EMPL_ID, e]))
  const deptById = new Map(departments.map((d) => [d.DEPT_ID, d]))
  const jobTypeById = new Map(jobTypes.map((j) => [j.JIKMU_ID, j]))

  return {
    project,
    employees: employeesRes.items,
    assignments: assignmentsRes.items.map((a) => {
      const employee = employeeById.get(a.EMPL_ID)
      return {
        ...a,
        employeeName: employee?.EMPL_NM ?? a.EMPL_ID,
        deptName: employee ? (deptById.get(employee.DEPT_ID)?.DEPT_NM ?? '-') : '-',
        jobTypeName: employee?.JIKMU_ID ? (jobTypeById.get(employee.JIKMU_ID)?.JIKMU_NM ?? null) : null,
      }
    }),
  }
}

export default function ProjectDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = use(params)
  const router = useRouter()
  const [data, setData] = useState<ProjectDetailData | null>(null)
  const [notFound, setNotFound] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [openEdit, setOpenEdit] = useState(false)
  const [openCloseConfirm, setOpenCloseConfirm] = useState(false)
  const [closing, setClosing] = useState(false)
  const [closeError, setCloseError] = useState<string | null>(null)
  const [openAddAssignment, setOpenAddAssignment] = useState(false)

  async function handleClose() {
    setClosing(true)
    setCloseError(null)
    try {
      await apiPatch(`/api/v1/projects/${id}`, { PJT_STAT_CD: 'CLOSED' })
      reload()
    } catch (err) {
      setCloseError(err instanceof ApiError ? err.message : '종료 처리에 실패했습니다. 잠시 후 다시 시도하세요.')
    } finally {
      setClosing(false)
    }
  }

  function reload() {
    let cancelled = false
    loadProjectDetail(id)
      .then((result) => {
        if (!cancelled) setData(result)
      })
      .catch((err) => {
        if (cancelled) return
        if (err instanceof ApiError && err.status === 404) {
          setNotFound(true)
        } else {
          setError('프로젝트 정보를 불러오지 못했습니다. 잠시 후 다시 시도하세요.')
        }
      })
    return () => {
      cancelled = true
    }
  }

  useEffect(reload, [id])

  if (notFound) {
    return (
      <div className="p-6">
        <EmptyState
          title="프로젝트를 찾을 수 없습니다"
          description="요청하신 프로젝트 정보가 존재하지 않습니다."
        >
          <Button variant="secondary" onClick={() => router.push('/projects')}>
            목록으로
          </Button>
        </EmptyState>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6">
        <p className="text-sm text-destructive">{error}</p>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="p-6">
        <p className="text-sm text-muted-foreground">불러오는 중입니다...</p>
      </div>
    )
  }

  const { project, employees, assignments } = data
  const activeAssignments = assignments.filter((a) => a.ASGN_STAT_CD === 'ACTIVE')
  const plannedCount = assignments.filter((a) => a.ASGN_STAT_CD === 'PLANNED').length
  const doneCount = assignments.filter((a) => a.ASGN_STAT_CD === 'DONE').length
  const memberCount = new Set(activeAssignments.map((a) => a.EMPL_ID)).size
  const avgAllocation = activeAssignments.length
    ? Math.round(activeAssignments.reduce((s, a) => s + a.ALLOC_RT, 0) / activeAssignments.length)
    : 0

  return (
    <div className="flex flex-col gap-6 p-6">
      <button
        onClick={() => router.push('/projects')}
        className="flex w-fit items-center gap-1.5 text-sm text-muted-foreground transition-colors hover:text-foreground"
      >
        <ArrowLeft className="size-4" />
        프로젝트 목록
      </button>

      <PageHeader
        title={project.PJT_NM}
        description={`${project.PJT_CD} · ${project.CLNT_NM ?? '고객사 미지정'}`}
      >
        <Button variant="secondary" onClick={() => setOpenEdit(true)}>
          <Pencil className="size-4" />
          수정
        </Button>
        <Button
          variant="secondary"
          onClick={() => setOpenCloseConfirm(true)}
          disabled={project.PJT_STAT_CD === 'CLOSED'}
        >
          <CircleOff className="size-4" />
          종료처리
        </Button>
        <Button onClick={() => setOpenAddAssignment(true)}>
          <UserPlus className="size-4" />
          인력투입
        </Button>
      </PageHeader>

      {closeError && <p className="text-sm text-destructive">{closeError}</p>}

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>프로젝트 개요</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <p className="text-sm leading-relaxed text-muted-foreground">
              {project.PJT_DESC ?? '등록된 개요가 없습니다.'}
            </p>
            <Separator />
            <dl className="grid grid-cols-2 gap-x-6 gap-y-4 text-sm sm:grid-cols-3">
              <div>
                <dt className="text-xs text-muted-foreground">상태</dt>
                <dd className="mt-1">
                  <Badge>{project.PJT_STAT_CD}</Badge>
                </dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">고객사</dt>
                <dd className="mt-1 font-medium">{project.CLNT_NM ?? '-'}</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">투입 인원</dt>
                <dd className="mt-1 font-medium">{memberCount}명</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">시작일</dt>
                <dd className="mt-1 font-medium tabular-nums">{project.STRT_DT}</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">종료일</dt>
                <dd className="mt-1 font-medium tabular-nums">{project.END_DT ?? '-'}</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">평균 투입률</dt>
                <dd className="mt-1 font-medium tabular-nums">{avgAllocation}%</dd>
              </div>
            </dl>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>투입 유형 구성</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            {(['RUNNING', 'COMMITTED', 'PROPOSED'] as const).map((t) => {
              const count = activeAssignments.filter((a) => a.ASGN_TYPE_CD === t).length
              if (count === 0) return null
              return (
                <div
                  key={t}
                  className="flex items-center justify-between rounded-md border border-border bg-muted/40 px-3 py-2"
                >
                  <span className="text-sm">{assignmentTypeLabel[t]}</span>
                  <Badge variant="secondary">{count}명</Badge>
                </div>
              )
            })}
            {activeAssignments.length === 0 && (
              <p className="text-sm text-muted-foreground">진행 중인 투입이 없습니다.</p>
            )}
            {/* 사용자 요청으로 진행 중(ACTIVE) 유형별 구성 외에도 계획(PLANNED)·종료(DONE)
                상태의 인력 수를 함께 표시한다(§9-1과 무관한 직접 요청 건, 2026-07-05). */}
            <div className="mt-1 flex items-center justify-between rounded-md border border-dashed border-border px-3 py-2">
              <span className="text-sm text-muted-foreground">계획된 인력</span>
              <Badge variant="outline">{plannedCount}명</Badge>
            </div>
            <div className="flex items-center justify-between rounded-md border border-dashed border-border px-3 py-2">
              <span className="text-sm text-muted-foreground">종료된 인력</span>
              <Badge variant="outline">{doneCount}명</Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>투입 인력 ({assignments.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {assignments.length === 0 ? (
            <EmptyState
              title="투입된 인력이 없습니다"
              description="이 프로젝트에 배정된 투입 이력이 없습니다."
            />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>이름</TableHead>
                  <TableHead>부서</TableHead>
                  <TableHead>직무</TableHead>
                  <TableHead>역할</TableHead>
                  <TableHead>투입 유형</TableHead>
                  <TableHead className="w-44">투입률</TableHead>
                  <TableHead>기간</TableHead>
                  <TableHead>상태</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {assignments.map((a) => (
                  <TableRow key={a.ASGN_ID}>
                    <TableCell className="font-medium">{a.employeeName}</TableCell>
                    <TableCell className="text-muted-foreground">{a.deptName}</TableCell>
                    <TableCell className="text-muted-foreground">{a.jobTypeName ?? '-'}</TableCell>
                    <TableCell className="text-muted-foreground">{a.PRJT_ROLE_NM}</TableCell>
                    <TableCell>
                      <Badge variant="outline">{assignmentTypeLabel[a.ASGN_TYPE_CD]}</Badge>
                    </TableCell>
                    <TableCell>
                      <UtilizationBar value={a.ALLOC_RT} />
                    </TableCell>
                    <TableCell className="text-xs tabular-nums text-muted-foreground">
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
        </CardContent>
      </Card>

      <ProjectFormModal open={openEdit} onOpenChange={setOpenEdit} onSaved={reload} project={project} />
      <AssignmentFormModal
        open={openAddAssignment}
        onOpenChange={setOpenAddAssignment}
        onSaved={reload}
        employees={employees}
        fixedPjtId={project.PJT_ID}
        fixedPjtName={project.PJT_NM}
      />
      <ConfirmDialog
        open={openCloseConfirm}
        onClose={() => setOpenCloseConfirm(false)}
        onConfirm={handleClose}
        title="프로젝트를 종료 처리하시겠습니까?"
        description={`"${project.PJT_NM}" 프로젝트의 상태를 "종료"로 전환합니다. 프로젝트 정보는 삭제되지 않습니다.`}
        confirmText={closing ? '처리 중...' : '종료 처리'}
        destructive
      />
    </div>
  )
}
