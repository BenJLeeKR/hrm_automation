'use client'

import { Users, Zap, PieChart, CalendarClock, Gauge, AlertTriangle } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { StatCard } from '@/components/common/stat-card'
import { SectionCard } from '@/components/common/section-card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { HeadcountChart } from '@/components/charts/headcount-chart'
import { JobTypeDonut } from '@/components/charts/job-type-donut'
import { DeptUtilizationChart } from '@/components/charts/dept-utilization-chart'
import {
  dashboardKpis,
  orgUtilization,
  dataQuality,
  endingThisMonth,
  recentEmployees,
} from '@/lib/mock-data'
import { allocationBadge } from '@/lib/labels'

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="대시보드"
        description="블루어드 인력 리소스 현황을 한눈에 확인하세요."
      />

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard
          label="총 인력"
          value={String(dashboardKpis.totalEmployees)}
          unit="명"
          icon={Users}
          tone="primary"
          trend={{ value: '+2.9%', up: true }}
          hint="재직 중 기준"
        />
        <StatCard
          label="즉시 투입 가능"
          value={String(dashboardKpis.immediate)}
          unit="명"
          icon={Zap}
          tone="success"
          hint="가동률 30% 미만"
        />
        <StatCard
          label="평균 가동률"
          value={`${dashboardKpis.avgUtilization}`}
          unit="%"
          icon={Gauge}
          tone="info"
          trend={{ value: '+1.4%', up: true }}
          hint="딜리버리 조직 기준"
        />
        <StatCard
          label="이달 투입 종료"
          value={String(dashboardKpis.endingThisMonth)}
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
          <HeadcountChart />
        </SectionCard>

        <SectionCard title="직무 유형 분포" icon={PieChart}>
          <JobTypeDonut />
        </SectionCard>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <SectionCard title="조직별 가동률" icon={Gauge}>
          <DeptUtilizationChart />
          <div className="mt-4 space-y-3 border-t border-border pt-4">
            <UtilRow label="투입 확정 반영 시" value={orgUtilization.committed} />
            <UtilRow label="제안 포함 시" value={orgUtilization.proposed} />
          </div>
        </SectionCard>

        <SectionCard
          title="이달 투입 종료 예정"
          icon={CalendarClock}
          bodyClassName="px-0 pb-2"
        >
          <ul className="divide-y divide-border">
            {endingThisMonth.map((item) => {
              const b = allocationBadge(item.allocation)
              return (
                <li
                  key={`${item.name}-${item.project}`}
                  className="flex items-center justify-between gap-3 px-5 py-2.5"
                >
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">{item.name}</p>
                    <p className="truncate text-xs text-muted-foreground">{item.project}</p>
                  </div>
                  <div className="flex shrink-0 items-center gap-2">
                    <Badge variant={b.variant}>{item.allocation}%</Badge>
                    <span className="w-[74px] text-right text-xs text-muted-foreground tabular-nums">
                      {item.endDate}
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
              <QualityRow label="스킬 정보 누락" count={dataQuality.skillMissing} />
              <QualityRow label="직무 정보 누락" count={dataQuality.jobMissing} />
              <QualityRow label="가동률 초과(100% 이상)" count={dataQuality.overAllocation} />
            </div>
          </SectionCard>

          <SectionCard title="최근 입사자" icon={Users} bodyClassName="px-0 pb-2">
            <ul className="divide-y divide-border">
              {recentEmployees.map((emp) => (
                <li
                  key={emp.empNo}
                  className="flex items-center justify-between gap-3 px-5 py-2"
                >
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">
                      {emp.name}{' '}
                      <span className="text-xs font-normal text-muted-foreground">
                        {emp.role}
                      </span>
                    </p>
                    <p className="text-xs text-muted-foreground">{emp.empNo}</p>
                  </div>
                  <span className="shrink-0 text-xs text-muted-foreground tabular-nums">
                    {emp.hireDate}
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
