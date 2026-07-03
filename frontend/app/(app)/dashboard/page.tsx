'use client'

import { useEffect, useState } from 'react'
import { Users, Zap, PieChart, CalendarClock, Gauge, AlertTriangle } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { StatCard } from '@/components/common/stat-card'
import { SectionCard } from '@/components/common/section-card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { HeadcountChart, type HeadcountTrendPoint } from '@/components/charts/headcount-chart'
import { JobTypeDonut, type JobTypeDistributionPoint } from '@/components/charts/job-type-donut'
import { DeptUtilizationChart, type DeptUtilizationPoint } from '@/components/charts/dept-utilization-chart'
import { apiGet } from '@/lib/api'
import { allocationBadge } from '@/lib/labels'

// 백엔드 대시보드 API 8종(로드맵 §8 "대시보드 화면 구현") 응답 타입 — 필드명은
// backend/app/schemas/dashboard.py와 동일하게 유지한다.
interface SummaryOut {
  total_active_employees: number
  available_count: number
  partial_count: number
  full_count: number
  ending_this_month_count: number
  avg_utilization_rate: number | null
}
interface DeptUtilizationItem {
  DEPT_ID: string
  DEPT_NM: string
  employee_count: number
  avg_utilization_rate: number
}
interface JobTypeDistributionItem {
  JIKMU_ID: string | null
  JIKMU_NM: string
  employee_count: number
}
interface UtilizationByTypeOut {
  month: string
  running_rate: number
  running_committed_rate: number
  all_rate: number
}
interface DataQualityOut {
  skill_missing_count: number
  job_missing_count: number
  over_allocation_count: number
}
interface EndingAssignmentItem {
  EMPL_NM: string
  DEPT_NM: string | null
  PJT_NM: string
  ASGN_END_DT: string
  ALLOC_RT: number
}
interface RecentEmployeeItem {
  EMPL_NO: string
  EMPL_NM: string
  DEPT_NM: string | null
  HIRE_DT: string
  JIKMU_NM: string | null
}
interface HeadcountTrendItem {
  month: string
  total: number
  hires: number
  exits: number
}

interface DashboardData {
  summary: SummaryOut
  deptUtilization: DeptUtilizationPoint[]
  jobTypeDistribution: JobTypeDistributionPoint[]
  utilizationByType: UtilizationByTypeOut
  dataQuality: DataQualityOut
  endingThisMonth: EndingAssignmentItem[]
  recentEmployees: RecentEmployeeItem[]
  headcountTrend: HeadcountTrendPoint[]
}

function currentYyyyMm(): string {
  const now = new Date()
  return `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}`
}

function formatTrendMonth(yyyyMm: string): string {
  return `${yyyyMm.slice(2, 4)}.${yyyyMm.slice(4, 6)}`
}

async function loadDashboardData(): Promise<DashboardData> {
  const [summary, deptUtilizationRaw, jobTypeRaw, utilizationByType, dataQuality, endingThisMonth, recentEmployees, headcountTrendRaw] =
    await Promise.all([
      apiGet<SummaryOut>('/api/v1/dashboard/summary'),
      apiGet<DeptUtilizationItem[]>('/api/v1/dashboard/dept-utilization'),
      apiGet<JobTypeDistributionItem[]>('/api/v1/dashboard/job-type-distribution'),
      apiGet<UtilizationByTypeOut>(`/api/v1/dashboard/utilization-by-type?month=${currentYyyyMm()}`),
      apiGet<DataQualityOut>('/api/v1/dashboard/data-quality'),
      apiGet<EndingAssignmentItem[]>('/api/v1/dashboard/ending-this-month'),
      apiGet<RecentEmployeeItem[]>('/api/v1/dashboard/recent-employees?limit=5'),
      apiGet<HeadcountTrendItem[]>('/api/v1/dashboard/headcount-trend?months=12'),
    ])

  return {
    summary,
    deptUtilization: deptUtilizationRaw.map((d) => ({ team: d.DEPT_NM, value: Math.round(d.avg_utilization_rate) })),
    jobTypeDistribution: jobTypeRaw.map((j) => ({ name: j.JIKMU_NM, value: j.employee_count })),
    utilizationByType,
    dataQuality,
    endingThisMonth,
    recentEmployees,
    headcountTrend: headcountTrendRaw.map((h) => ({
      month: formatTrendMonth(h.month),
      total: h.total,
      hires: h.hires,
      exits: h.exits,
    })),
  }
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    loadDashboardData()
      .then((result) => {
        if (!cancelled) setData(result)
      })
      .catch(() => {
        if (!cancelled) setError('대시보드 데이터를 불러오지 못했습니다. 잠시 후 다시 시도하세요.')
      })
    return () => {
      cancelled = true
    }
  }, [])

  if (error) {
    return (
      <div className="space-y-6">
        <PageHeader title="대시보드" description="블루어드 인력 리소스 현황을 한눈에 확인하세요." />
        <p className="text-sm text-destructive">{error}</p>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="space-y-6">
        <PageHeader title="대시보드" description="블루어드 인력 리소스 현황을 한눈에 확인하세요." />
        <p className="text-sm text-muted-foreground">불러오는 중입니다...</p>
      </div>
    )
  }

  const { summary, deptUtilization, jobTypeDistribution, utilizationByType, dataQuality, endingThisMonth, recentEmployees, headcountTrend } =
    data

  return (
    <div className="space-y-6">
      <PageHeader
        title="대시보드"
        description="블루어드 인력 리소스 현황을 한눈에 확인하세요."
      />

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard
          label="총 인력"
          value={String(summary.total_active_employees)}
          unit="명"
          icon={Users}
          tone="primary"
          hint="재직 중 기준"
        />
        <StatCard
          label="즉시 투입 가능"
          value={String(summary.available_count)}
          unit="명"
          icon={Zap}
          tone="success"
          hint="가동률 0%"
        />
        <StatCard
          label="평균 가동률"
          value={summary.avg_utilization_rate === null ? '-' : summary.avg_utilization_rate.toFixed(1)}
          unit="%"
          icon={Gauge}
          tone="info"
          hint="전체 재직 인원 기준"
        />
        <StatCard
          label="이달 투입 종료"
          value={String(summary.ending_this_month_count)}
          unit="건"
          icon={CalendarClock}
          tone="warning"
          hint="재배치 검토 필요"
        />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <SectionCard
          title="월별 인력 추이"
          icon={Users}
          className="lg:col-span-2"
          action={
            <div className="flex items-center gap-3 text-xs text-muted-foreground">
              <LegendDot color="var(--color-chart-1)" label="총원" />
              <LegendDot color="var(--color-chart-2)" label="입사" />
              <LegendDot color="var(--color-chart-4)" label="퇴사" />
            </div>
          }
        >
          <HeadcountChart data={headcountTrend} />
        </SectionCard>

        <SectionCard title="직무 유형 분포" icon={PieChart}>
          <JobTypeDonut data={jobTypeDistribution} />
        </SectionCard>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <SectionCard title="조직별 가동률" icon={Gauge}>
          <DeptUtilizationChart data={deptUtilization} />
          <div className="mt-4 space-y-3 border-t border-border pt-4">
            <UtilRow label="투입 확정 반영 시" value={utilizationByType.running_committed_rate} />
            <UtilRow label="제안 포함 시" value={utilizationByType.all_rate} />
          </div>
        </SectionCard>

        <SectionCard
          title="이달 투입 종료 예정"
          icon={CalendarClock}
          bodyClassName="px-0 pb-2"
        >
          <ul className="divide-y divide-border">
            {endingThisMonth.length === 0 && (
              <li className="px-5 py-3 text-xs text-muted-foreground">이달 종료 예정인 투입이 없습니다.</li>
            )}
            {endingThisMonth.map((item) => {
              const b = allocationBadge(item.ALLOC_RT)
              return (
                <li
                  key={`${item.EMPL_NM}-${item.PJT_NM}`}
                  className="flex items-center justify-between gap-3 px-5 py-2.5"
                >
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">{item.EMPL_NM}</p>
                    <p className="truncate text-xs text-muted-foreground">{item.PJT_NM}</p>
                  </div>
                  <div className="flex shrink-0 items-center gap-2">
                    <Badge variant={b.variant}>{item.ALLOC_RT}%</Badge>
                    <span className="w-[74px] text-right text-xs text-muted-foreground tabular-nums">
                      {item.ASGN_END_DT}
                    </span>
                  </div>
                </li>
              )
            })}
          </ul>
        </SectionCard>

        <div className="space-y-4">
          <SectionCard title="데이터 품질 점검" icon={AlertTriangle}>
            <div className="space-y-2.5">
              <QualityRow label="스킬 정보 누락" count={dataQuality.skill_missing_count} />
              <QualityRow label="직무 정보 누락" count={dataQuality.job_missing_count} />
              <QualityRow label="가동률 초과(100% 이상)" count={dataQuality.over_allocation_count} />
            </div>
          </SectionCard>

          <SectionCard title="최근 입사자" icon={Users} bodyClassName="px-0 pb-2">
            <ul className="divide-y divide-border">
              {recentEmployees.length === 0 && (
                <li className="px-5 py-3 text-xs text-muted-foreground">최근 입사자가 없습니다.</li>
              )}
              {recentEmployees.map((emp) => (
                <li
                  key={emp.EMPL_NO}
                  className="flex items-center justify-between gap-3 px-5 py-2"
                >
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">
                      {emp.EMPL_NM}{' '}
                      <span className="text-xs font-normal text-muted-foreground">
                        {emp.JIKMU_NM ?? '-'}
                      </span>
                    </p>
                    <p className="text-xs text-muted-foreground">{emp.EMPL_NO}</p>
                  </div>
                  <span className="shrink-0 text-xs text-muted-foreground tabular-nums">
                    {emp.HIRE_DT}
                  </span>
                </li>
              ))}
            </ul>
          </SectionCard>
        </div>
      </div>
    </div>
  )
}

function LegendDot({ color, label }: { color: string; label: string }) {
  return (
    <span className="inline-flex items-center gap-1.5">
      <span className="size-2 rounded-full" style={{ backgroundColor: color }} />
      {label}
    </span>
  )
}

function UtilRow({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="mb-1 flex items-center justify-between text-xs">
        <span className="text-muted-foreground">{label}</span>
        <span className="font-semibold tabular-nums">{value}%</span>
      </div>
      <Progress value={value} />
    </div>
  )
}

function QualityRow({ label, count }: { label: string; count: number }) {
  const ok = count === 0
  return (
    <div className="flex items-center justify-between rounded-lg border border-border bg-secondary/40 px-3 py-2">
      <span className="text-sm">{label}</span>
      <Badge variant={ok ? 'success' : count > 3 ? 'warning' : 'danger'}>
        {count}건
      </Badge>
    </div>
  )
}
