'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Bell, AlertTriangle, CalendarClock } from 'lucide-react'
import { Dropdown } from '@/components/ui/dropdown'
import { apiGet } from '@/lib/api'

// 대시보드가 이미 계산해두는 데이터 품질 점검(`GET /dashboard/data-quality`)·이번 달 투입
// 종료 예정(`GET /dashboard/ending-this-month`) 결과를 재사용한 실시간 알림 드롭다운
// (§9-1 "상단 알림 아이콘 표시 내용 없음"). 신규 백엔드 API/스키마 없이 기존 대시보드
// 위젯 데이터를 그대로 조회한다.
//
// 읽음/안읽음 상태는 관리하지 않는다 — 알림을 영속 저장하는 테이블(예: SYS_NOTIFICATION)이
// 아직 설계되어 있지 않아(§9-1 원문에도 "집계·읽음 처리 방식은 미정"으로 명시), 이번
// 범위에서는 매번 최신 상태를 다시 조회해 보여주는 것으로 최소 구현한다. 읽음 처리가
// 필요해지면 별도 설계·백로그 항목으로 논의 필요.
interface DataQuality {
  skill_missing_count: number
  job_missing_count: number
  over_allocation_count: number
}

interface EndingAssignment {
  EMPL_NM: string
  PJT_NM: string
  ASGN_END_DT: string
}

export function NotificationsDropdown() {
  const router = useRouter()
  const [dataQuality, setDataQuality] = useState<DataQuality | null>(null)
  const [endingSoon, setEndingSoon] = useState<EndingAssignment[]>([])

  useEffect(() => {
    apiGet<DataQuality>('/api/v1/dashboard/data-quality').then(setDataQuality).catch(() => setDataQuality(null))
    apiGet<EndingAssignment[]>('/api/v1/dashboard/ending-this-month').then(setEndingSoon).catch(() => setEndingSoon([]))
  }, [])

  const qualityIssueCount = dataQuality
    ? dataQuality.skill_missing_count + dataQuality.job_missing_count + dataQuality.over_allocation_count
    : 0
  const totalCount = qualityIssueCount + endingSoon.length

  return (
    <Dropdown
      trigger={
        <span
          className="relative inline-flex rounded-lg p-2 text-nav-icon transition-colors hover:bg-nav-hover hover:text-nav-foreground"
          aria-label="알림"
        >
          <Bell className="size-5" />
          {totalCount > 0 && <span className="absolute right-1.5 top-1.5 size-2 rounded-full bg-nav-accent" />}
        </span>
      }
    >
      <div className="w-72">
        <p className="px-2.5 py-2 text-sm font-semibold text-foreground">알림</p>
        {totalCount === 0 ? (
          <p className="px-2.5 py-3 text-sm text-muted-foreground">새로운 알림이 없습니다.</p>
        ) : (
          <div className="flex flex-col gap-1">
            {qualityIssueCount > 0 && (
              <button
                type="button"
                onClick={() => router.push('/dashboard')}
                className="flex items-start gap-2 rounded-md px-2.5 py-2 text-left text-sm hover:bg-secondary"
              >
                <AlertTriangle className="mt-0.5 size-4 shrink-0 text-destructive" />
                <span>데이터 품질 점검 이슈 {qualityIssueCount}건 (기술/직무 미등록, 투입률 초과)</span>
              </button>
            )}
            {endingSoon.slice(0, 5).map((item, idx) => (
              <button
                key={`${item.EMPL_NM}-${item.PJT_NM}-${idx}`}
                type="button"
                onClick={() => router.push('/dashboard')}
                className="flex items-start gap-2 rounded-md px-2.5 py-2 text-left text-sm hover:bg-secondary"
              >
                <CalendarClock className="mt-0.5 size-4 shrink-0 text-muted-foreground" />
                <span>
                  {item.EMPL_NM} — {item.PJT_NM} 투입 종료 예정 ({item.ASGN_END_DT})
                </span>
              </button>
            ))}
            {endingSoon.length > 5 && (
              <p className="px-2.5 py-1 text-xs text-muted-foreground">외 {endingSoon.length - 5}건 더 있음</p>
            )}
          </div>
        )}
      </div>
    </Dropdown>
  )
}
