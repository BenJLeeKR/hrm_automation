'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Zap, Clock, CalendarClock } from 'lucide-react'
import { availabilityRows } from '@/lib/mock-data'
import { teamOptions } from '@/lib/options'
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
import { teamLabel } from '@/lib/labels'
import type { AvailabilityKind } from '@/lib/types'

const KIND_DESC: Record<AvailabilityKind, string> = {
  IMMEDIATE: '현재 미투입 상태로 즉시 배정 가능한 인력',
  PARTIAL: '잔여 공수로 추가 투입이 가능한 인력',
  TERM: '진행 프로젝트 종료 후 가동 가능한 인력',
}

export default function AvailabilityPage() {
  const router = useRouter()
  const [tab, setTab] = useState<AvailabilityKind>('IMMEDIATE')
  const [query, setQuery] = useState('')
  const [team, setTeam] = useState('ALL')

  const counts = useMemo(
    () => ({
      IMMEDIATE: availabilityRows.filter((r) => r.kind === 'IMMEDIATE').length,
      PARTIAL: availabilityRows.filter((r) => r.kind === 'PARTIAL').length,
      TERM: availabilityRows.filter((r) => r.kind === 'TERM').length,
    }),
    [],
  )

  const rows = useMemo(() => {
    return availabilityRows.filter((r) => {
      if (r.kind !== tab) return false
      if (team !== 'ALL' && r.team !== team) return false
      if (
        query &&
        !r.name.includes(query) &&
        !r.skills.some((s) => s.toLowerCase().includes(query.toLowerCase())) &&
        !r.jobType.toLowerCase().includes(query.toLowerCase())
      )
        return false
      return true
    })
  }, [tab, team, query])

  return (
    <div className="flex flex-col gap-6 p-6">
      <PageHeader
        title="가동 가능 인력"
        description="투입 가능 시점별로 인력 풀을 조회하여 신규 프로젝트 배정에 활용합니다."
      />

      <div className="grid gap-4 sm:grid-cols-3">
        <StatCard
          label="즉시 가동 가능"
          value={`${counts.IMMEDIATE}명`}
          icon={Zap}
          tone="success"
        />
        <StatCard
          label="부분 가동 가능"
          value={`${counts.PARTIAL}명`}
          icon={Clock}
          tone="info"
        />
        <StatCard
          label="기간 종료 예정"
          value={`${counts.TERM}명`}
          icon={CalendarClock}
          tone="warning"
        />
      </div>

      <Card>
        <CardContent className="flex flex-col gap-4 pt-6">
          <Tabs
            value={tab}
            onValueChange={(v) => setTab(v as AvailabilityKind)}
            tabs={[
              { value: 'IMMEDIATE', label: `즉시 가동 (${counts.IMMEDIATE})` },
              { value: 'PARTIAL', label: `부분 가동 (${counts.PARTIAL})` },
              { value: 'TERM', label: `종료 예정 (${counts.TERM})` },
            ]}
          />

          <p className="text-sm text-muted-foreground">{KIND_DESC[tab]}</p>

          <div className="flex flex-col gap-3 sm:flex-row">
            <SearchInput
              value={query}
              onChange={setQuery}
              placeholder="이름 · 직무 · 기술 검색"
              className="sm:max-w-xs"
            />
            <Select
              value={team}
              onValueChange={setTeam}
              options={teamOptions}
              placeholder="조직 전체"
              className="sm:w-48"
            />
          </div>

          {rows.length === 0 ? (
            <EmptyState
              title="조건에 맞는 인력이 없습니다"
              description="검색어나 조직 필터를 조정해 보세요."
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
                  {rows.map((r) => (
                    <TableRow
                      key={r.empNo}
                      className="cursor-pointer"
                      onClick={() => router.push(`/employees/${r.empNo}`)}
                    >
                      <TableCell>
                        <span className="font-medium text-primary">{r.name}</span>
                        <span className="ml-2 font-mono text-xs text-muted-foreground">
                          {r.empNo}
                        </span>
                      </TableCell>
                      <TableCell className="text-muted-foreground">
                        {teamLabel[r.team]}
                      </TableCell>
                      <TableCell>{r.jobType}</TableCell>
                      <TableCell>
                        <div className="flex flex-wrap gap-1">
                          {r.skills.map((s) => (
                            <Badge key={s} variant="secondary">
                              {s}
                            </Badge>
                          ))}
                        </div>
                      </TableCell>
                      <TableCell>
                        <UtilizationBar value={r.allocation} />
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={r.availableDate === '즉시' ? 'success' : 'outline'}
                        >
                          {r.availableDate}
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
