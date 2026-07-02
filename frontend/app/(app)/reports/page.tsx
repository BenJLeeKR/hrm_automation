'use client'

import { useState } from 'react'
import { Download, TrendingUp, Users, Layers, AlertTriangle } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { StatCard } from '@/components/common/stat-card'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Tabs } from '@/components/ui/tabs'
import { Select } from '@/components/ui/select'
import { SkillBarChart } from '@/components/charts/skill-bar-chart'
import { HeadcountChart } from '@/components/charts/headcount-chart'
import { DeptUtilizationChart } from '@/components/charts/dept-utilization-chart'
import { UtilizationMatrix } from '@/components/reports/utilization-matrix'
import { dashboardKpis, orgUtilization } from '@/lib/mock-data'

const PERIOD_OPTIONS = [
  { value: 'RECENT_12M', label: '최근 12개월' },
  { value: 'RECENT_6M', label: '최근 6개월' },
  { value: 'YTD', label: '올해 누적' },
]

export default function ReportsPage() {
  const [tab, setTab] = useState('UTILIZATION')
  const [period, setPeriod] = useState('RECENT_12M')

  return (
    <div>
      <PageHeader
        title="리포트"
        description="가동률, 인력 구성, 기술 분포에 대한 분석 리포트를 제공합니다."
      >
        <div className="flex items-center gap-2">
          <Select value={period} onValueChange={setPeriod} options={PERIOD_OPTIONS} />
          <Button variant="secondary">
            <Download className="size-4" />
            내보내기
          </Button>
        </div>
      </PageHeader>

      <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          label="조직 평균 가동률"
          value={`${dashboardKpis.avgUtilization}%`}
          icon={TrendingUp}
          tone="primary"
        />
        <StatCard
          label="수행 기준 가동률"
          value={`${orgUtilization.running}%`}
          icon={Layers}
          tone="info"
        />
        <StatCard
          label="제안 포함 가동률"
          value={`${orgUtilization.proposed}%`}
          icon={Users}
          tone="success"
        />
        <StatCard
          label="공수 초과 인력"
          value={`${1}명`}
          icon={AlertTriangle}
          tone="warning"
        />
      </div>

      <div className="mb-6">
        <Tabs
          value={tab}
          onValueChange={setTab}
          tabs={[
            { value: 'UTILIZATION', label: '가동률 매트릭스' },
            { value: 'HEADCOUNT', label: '인력 추이' },
            { value: 'SKILL', label: '기술 분포' },
          ]}
        />
      </div>

      {tab === 'UTILIZATION' && (
        <Card>
          <CardHeader>
            <CardTitle>월별 가동률 매트릭스</CardTitle>
          </CardHeader>
          <CardContent>
            <UtilizationMatrix />
          </CardContent>
        </Card>
      )}

      {tab === 'HEADCOUNT' && (
        <div className="grid gap-6 lg:grid-cols-3">
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>인력 증감 추이</CardTitle>
            </CardHeader>
            <CardContent>
              <HeadcountChart />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>조직별 가동률</CardTitle>
            </CardHeader>
            <CardContent>
              <DeptUtilizationChart />
            </CardContent>
          </Card>
        </div>
      )}

      {tab === 'SKILL' && (
        <Card>
          <CardHeader>
            <CardTitle>보유 기술 분포 (상위 10)</CardTitle>
          </CardHeader>
          <CardContent>
            <SkillBarChart />
          </CardContent>
        </Card>
      )}
    </div>
  )
}
