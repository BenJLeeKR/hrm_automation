'use client'

import { useEffect, useState } from 'react'
import { Users, Zap, Clock, CalendarClock, AlertTriangle } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { StatCard } from '@/components/common/stat-card'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { SkillBarChart } from '@/components/charts/skill-bar-chart'
import { DeptUtilizationChart } from '@/components/charts/dept-utilization-chart'
import { apiGet, ApiError } from '@/lib/api'

// 백엔드 리포트 API(로드맵 §8 "리포트 화면 구현", SCR-013 탭 1·2) 응답 타입 — 필드명은
// backend/app/schemas/reports.py와 동일하게 유지한다. 탭 3 "월별 가동률 통계" 매트릭스와
// 리포트 발송/Excel 내보내기는 이번 범위에서 제외했다(§9 리스크 참조).
interface DeptUtilizationItem {
  DEPT_ID: string
  DEPT_NM: string
  employee_count: number
  avg_utilization_rate: number
}
interface SkillDistributionItem {
  SKILL_ID: string
  SKILL_NM: string
  employee_count: number
}
interface ReportOut {
  as_of: string
  total_active_employees: number
  available_count: number
  partial_count: number
  full_count: number
  ending_count: number
  job_missing_count: number
  dept_utilization: DeptUtilizationItem[]
  skill_distribution: SkillDistributionItem[]
}

function isoWeekOf(d: Date): string {
  // ISO 8601 주차 계산 — 백엔드 GET /reports/weekly?week=YYYY-Www 파라미터 형식에 맞춘다.
  const target = new Date(d.valueOf())
  const dayNr = (d.getDay() + 6) % 7
  target.setDate(target.getDate() - dayNr + 3)
  const firstThursday = new Date(target.getFullYear(), 0, 4)
  const diff = target.getTime() - firstThursday.getTime()
  const week = 1 + Math.round(diff / (7 * 24 * 60 * 60 * 1000))
  return `${target.getFullYear()}-W${String(week).padStart(2, '0')}`
}

function currentYyyyMm(): string {
  const now = new Date()
  return `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}`
}

export default function ReportsPage() {
  const [tab, setTab] = useState<'WEEKLY' | 'MONTHLY' | 'MATRIX'>('WEEKLY')
  const [week, setWeek] = useState(isoWeekOf(new Date()))
  const [month, setMonth] = useState(currentYyyyMm())
  const [report, setReport] = useState<ReportOut | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (tab === 'MATRIX') return
    setLoading(true)
    setError(null)
    const path =
      tab === 'WEEKLY'
        ? `/api/v1/reports/weekly?week=${week}`
        : `/api/v1/reports/monthly?month=${month}`
    apiGet<ReportOut>(path)
      .then(setReport)
      .catch((err) => setError(err instanceof ApiError ? err.message : '리포트를 불러오지 못했습니다.'))
      .finally(() => setLoading(false))
  }, [tab, week, month])

  return (
    <div>
      <PageHeader
        title="리포트"
        description="가동률, 인력 구성, 기술 분포에 대한 분석 리포트를 제공합니다."
      />

      <div className="mb-6">
        <Tabs
          value={tab}
          onValueChange={(v) => setTab(v as typeof tab)}
          tabs={[
            { value: 'WEEKLY', label: '주간 리포트' },
            { value: 'MONTHLY', label: '월간 리포트' },
            { value: 'MATRIX', label: '월별 가동률 통계' },
          ]}
        />
      </div>

      {tab === 'MATRIX' ? (
        <Card>
          <CardContent className="py-12 text-center text-sm text-muted-foreground">
            월별 가동률 통계 매트릭스는 준비 중입니다.
          </CardContent>
        </Card>
      ) : (
        <>
          <div className="mb-4 flex items-center gap-2">
            {tab === 'WEEKLY' ? (
              <Input type="week" value={week} onChange={(e) => setWeek(e.target.value)} className="w-44" />
            ) : (
              <Input
                type="month"
                value={`${month.slice(0, 4)}-${month.slice(4, 6)}`}
                onChange={(e) => setMonth(e.target.value.replace('-', ''))}
                className="w-44"
              />
            )}
          </div>

          {error && <p className="mb-4 text-sm text-destructive">{error}</p>}

          {!report ? (
            <p className="text-sm text-muted-foreground">{loading ? '불러오는 중입니다...' : ''}</p>
          ) : (
            <>
              <div className="mb-6 grid gap-4 sm:grid-cols-3 lg:grid-cols-6">
                <StatCard label="전체 인원" value={String(report.total_active_employees)} unit="명" icon={Users} tone="primary" />
                <StatCard label="즉시 가동" value={String(report.available_count)} unit="명" icon={Zap} tone="success" />
                <StatCard label="부분 가동" value={String(report.partial_count)} unit="명" icon={Clock} tone="info" />
                <StatCard label="풀 투입" value={String(report.full_count)} unit="명" icon={Users} tone="warning" />
                <StatCard label="종료 예정" value={String(report.ending_count)} unit="건" icon={CalendarClock} tone="warning" />
                <StatCard label="직무 미등록" value={String(report.job_missing_count)} unit="명" icon={AlertTriangle} tone="danger" />
              </div>

              <div className="grid gap-6 lg:grid-cols-2">
                <Card>
                  <CardHeader>
                    <CardTitle>부서별 가동률</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <DeptUtilizationChart
                      data={report.dept_utilization.map((d) => ({ team: d.DEPT_NM, value: Math.round(d.avg_utilization_rate) }))}
                    />
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>기술별 인력 분포 (상위 10)</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <SkillBarChart
                      data={report.skill_distribution.map((s) => ({ name: s.SKILL_NM, count: s.employee_count }))}
                    />
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </>
      )}
    </div>
  )
}
