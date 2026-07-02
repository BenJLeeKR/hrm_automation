'use client'

import { use, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import {
  ArrowLeft,
  Mail,
  Phone,
  CalendarDays,
  Pencil,
  Plus,
  Building2,
} from 'lucide-react'
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
import { HistoryTimeline } from '@/components/common/history-timeline'
import {
  EmployeeStatusBadge,
  AssignmentTypeBadge,
} from '@/components/common/status-badge'
import { EmployeeFormModal } from '@/components/employees/employee-form-modal'
import { employees, positions } from '@/lib/mock-data'
import { teamLabel, assignmentStatusLabel } from '@/lib/labels'
import { EmptyState } from '@/components/common/empty-state'

const TABS = [
  { value: 'info', label: '기본 정보' },
  { value: 'skills', label: '보유 기술' },
  { value: 'assignments', label: '투입 이력' },
  { value: 'history', label: '변경 이력' },
]

export default function EmployeeDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = use(params)
  const router = useRouter()
  const [tab, setTab] = useState('info')
  const [openEdit, setOpenEdit] = useState(false)

  const employee = employees.find((e) => e.id === id)

  if (!employee) {
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

  const positionName =
    positions.find((p) => p.code === employee.position)?.name ?? employee.position

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
              <Avatar name={employee.name} className="size-14 text-lg" />
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-xl font-bold tracking-tight">{employee.name}</h1>
                  <EmployeeStatusBadge status={employee.status} />
                </div>
                <p className="mt-0.5 text-sm text-muted-foreground">
                  {employee.empNo} · {teamLabel[employee.team]} · {positionName}
                </p>
                <div className="mt-2 flex flex-wrap gap-1">
                  {employee.roles.map((r) => (
                    <Badge key={r} variant="soft">
                      {r}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
            <Button variant="secondary" onClick={() => setOpenEdit(true)}>
              <Pencil className="size-4" />
              정보 수정
            </Button>
          </div>

          <div className="mt-5 grid grid-cols-2 gap-4 border-t border-border pt-5 lg:grid-cols-4">
            <InfoItem icon={Mail} label="이메일" value={employee.email} />
            <InfoItem icon={Phone} label="연락처" value={employee.phone} />
            <InfoItem icon={CalendarDays} label="입사일" value={employee.hireDate} />
            <div>
              <p className="mb-1.5 flex items-center gap-1.5 text-xs text-muted-foreground">
                <Building2 className="size-3.5" />현재 가동률
              </p>
              <UtilizationBar value={employee.allocation} />
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs tabs={TABS} value={tab} onValueChange={setTab} className="mb-4" />

      {tab === 'info' && (
        <Card>
          <CardContent className="pt-5">
            <dl className="grid grid-cols-1 gap-x-8 gap-y-4 sm:grid-cols-2">
              <Field label="사번" value={employee.empNo} />
              <Field label="이름" value={employee.name} />
              <Field label="조직" value={teamLabel[employee.team]} />
              <Field label="직급" value={positionName} />
              <Field label="이메일" value={employee.email} />
              <Field label="연락처" value={employee.phone} />
              <Field label="입사일" value={employee.hireDate} />
              <Field label="가동 가능일" value={employee.availableDate} />
            </dl>
          </CardContent>
        </Card>
      )}

      {tab === 'skills' && (
        <Card className="overflow-hidden p-0">
          <div className="flex items-center justify-between px-5 py-3">
            <p className="text-sm font-semibold">보유 기술 {employee.skills.length}건</p>
            <Button size="sm" variant="secondary">
              <Plus className="size-3.5" />기술 추가
            </Button>
          </div>
          {employee.skills.length === 0 ? (
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
                {employee.skills.map((s) => (
                  <TableRow key={s.skillName}>
                    <TableCell className="font-medium">{s.skillName}</TableCell>
                    <TableCell>
                      <Badge variant="secondary">{s.group}</Badge>
                    </TableCell>
                    <TableCell>
                      <SkillLevel level={s.level} />
                    </TableCell>
                    <TableCell className="tabular-nums">{s.years}년</TableCell>
                    <TableCell className="tabular-nums text-muted-foreground">
                      {s.lastUsed}
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
          {employee.assignments.length === 0 ? (
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
                  <TableHead>구분</TableHead>
                  <TableHead>투입률</TableHead>
                  <TableHead>기간</TableHead>
                  <TableHead>상태</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {employee.assignments.map((a, i) => (
                  <TableRow key={i}>
                    <TableCell className="font-medium">{a.projectName}</TableCell>
                    <TableCell>{a.role}</TableCell>
                    <TableCell>
                      <AssignmentTypeBadge type={a.type} />
                    </TableCell>
                    <TableCell className="tabular-nums">{a.allocation}%</TableCell>
                    <TableCell className="tabular-nums text-muted-foreground">
                      {a.startDate} ~ {a.endDate}
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{assignmentStatusLabel[a.status]}</Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </Card>
      )}

      {tab === 'history' && (
        <Card>
          <CardContent className="pt-5">
            <HistoryTimeline items={employee.history} />
          </CardContent>
        </Card>
      )}

      <EmployeeFormModal open={openEdit} onOpenChange={setOpenEdit} employee={employee} />
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
