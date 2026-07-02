'use client'

import { use, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowLeft, UserPlus, Trash2 } from 'lucide-react'
import { projects as seedProjects } from '@/lib/mock-data'
import { PageHeader } from '@/components/common/page-header'
import { EmptyState } from '@/components/common/empty-state'
import { ProjectStatusBadge } from '@/components/common/status-badge'
import { UtilizationBar } from '@/components/common/utilization-progress'
import { ConfirmDialog } from '@/components/common/confirm-dialog'
import { AssignmentFormModal } from '@/components/projects/assignment-form-modal'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { assignmentTypeLabel } from '@/lib/labels'
import type { AssignmentType } from '@/lib/types'
import type { Project } from '@/lib/types'

export default function ProjectDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = use(params)
  const router = useRouter()

  const base = useMemo(() => seedProjects.find((p) => p.id === id), [id])
  const [project, setProject] = useState<Project | undefined>(base)
  const [openAssign, setOpenAssign] = useState(false)
  const [removeTarget, setRemoveTarget] = useState<string | null>(null)

  if (!project) {
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

  const members = project.members
  const totalAllocation = members.reduce((s, m) => s + m.allocation, 0)

  function handleRemove() {
    if (!removeTarget) return
    setProject((prev) =>
      prev
        ? { ...prev, members: prev.members.filter((m) => m.empNo !== removeTarget) }
        : prev,
    )
    setRemoveTarget(null)
  }

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
        title={project.name}
        description={`${project.code} · ${project.client}`}
      >
        <Button onClick={() => setOpenAssign(true)}>
          <UserPlus className="size-4" />
          인력 투입
        </Button>
      </PageHeader>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>프로젝트 개요</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <p className="text-sm leading-relaxed text-muted-foreground">
              {project.desc}
            </p>
            <Separator />
            <dl className="grid grid-cols-2 gap-x-6 gap-y-4 text-sm sm:grid-cols-3">
              <div>
                <dt className="text-xs text-muted-foreground">상태</dt>
                <dd className="mt-1">
                  <ProjectStatusBadge status={project.status} />
                </dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">고객사</dt>
                <dd className="mt-1 font-medium">{project.client}</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">투입 인원</dt>
                <dd className="mt-1 font-medium">{members.length}명</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">시작일</dt>
                <dd className="mt-1 font-medium tabular-nums">{project.startDate}</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">종료일</dt>
                <dd className="mt-1 font-medium tabular-nums">{project.endDate}</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">총 투입 공수</dt>
                <dd className="mt-1 font-medium tabular-nums">{totalAllocation}%</dd>
              </div>
            </dl>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>투입 유형 구성</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            {(['RUNNING', 'COMMITTED', 'PROPOSED'] as AssignmentType[]).map((t) => {
              const count = members.filter((m) => m.type === t).length
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
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>투입 인력 ({members.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {members.length === 0 ? (
            <EmptyState
              title="투입된 인력이 없습니다"
              description="상단의 인력 투입 버튼으로 팀원을 배정하세요."
            />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>사번</TableHead>
                  <TableHead>이름</TableHead>
                  <TableHead>역할</TableHead>
                  <TableHead>투입 유형</TableHead>
                  <TableHead className="w-44">투입률</TableHead>
                  <TableHead>기간</TableHead>
                  <TableHead className="w-16 text-right">관리</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {members.map((m) => (
                  <TableRow key={m.empNo}>
                    <TableCell className="font-mono text-xs text-muted-foreground">
                      {m.empNo}
                    </TableCell>
                    <TableCell>
                      <button
                        onClick={() => router.push(`/employees/${m.empNo}`)}
                        className="font-medium text-primary hover:underline"
                      >
                        {m.name}
                      </button>
                    </TableCell>
                    <TableCell className="text-muted-foreground">{m.role}</TableCell>
                    <TableCell>
                      <Badge variant="outline">{assignmentTypeLabel[m.type]}</Badge>
                    </TableCell>
                    <TableCell>
                      <UtilizationBar value={m.allocation} />
                    </TableCell>
                    <TableCell className="text-xs tabular-nums text-muted-foreground">
                      {m.startDate} ~ {m.endDate}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        variant="ghost"
                        size="icon"
                        aria-label={`${m.name} 투입 해제`}
                        onClick={() => setRemoveTarget(m.empNo)}
                      >
                        <Trash2 className="size-4 text-destructive" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      <AssignmentFormModal
        open={openAssign}
        onClose={() => setOpenAssign(false)}
        projectName={project.name}
        onSubmit={(m) =>
          setProject((prev) =>
            prev ? { ...prev, members: [...prev.members, m] } : prev,
          )
        }
      />

      <ConfirmDialog
        open={removeTarget !== null}
        onClose={() => setRemoveTarget(null)}
        onConfirm={handleRemove}
        title="투입 해제"
        description="해당 인력을 프로젝트에서 투입 해제하시겠습니까?"
        confirmText="투입 해제"
        destructive
      />
    </div>
  )
}
