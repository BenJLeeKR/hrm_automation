'use client'

import { useEffect, useMemo, useState } from 'react'
import { Download } from 'lucide-react'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { apiGet, apiDownloadFile, ApiError } from '@/lib/api'
import { cn } from '@/lib/utils'
import type { AssignmentType } from '@/lib/types'

// 백엔드 월별 가동률 통계 매트릭스 API(로드맵 §8, SCR-013 탭 3,
// `ResourceManagement_v2.xlsx` "가동률_통계" 시트 구조) 응답 타입 — 필드명은
// backend/app/schemas/reports.py와 동일하게 유지한다. 기존 프로토타입(목데이터
// `utilizationMatrix`/`matrixMonths` 기반 히트맵)의 셀 스타일은 그대로 재사용하고,
// 데이터 소스만 실 API로 교체했다.
interface UtilizationMatrixRow {
  pjt_nm: string
  asgn_type_cd: AssignmentType
  monthly: number[]
  avg: number
}
interface UtilizationMatrixEmployee {
  empl_no: string
  empl_nm: string
  dept_nm: string
  rows: UtilizationMatrixRow[]
  subtotal: number[]
  annual_avg: number
  over_100_months: string[]
}
interface UtilizationMatrixOut {
  period: string[]
  employees: UtilizationMatrixEmployee[]
  org_avg: {
    running_only: number[]
    running_committed: number[]
    all: number[]
  }
}
interface DepartmentOut {
  DEPT_ID: string
  DEPT_NM: string
}

const ASGN_TYPE_ICON: Record<AssignmentType, string> = {
  RUNNING: '🔵',
  COMMITTED: '🟠',
  PROPOSED: '🟢',
}

function cellStyle(v: number): string {
  if (v <= 0) return 'bg-secondary text-muted-foreground'
  if (v > 100) return 'bg-[#c0392b] text-white'
  if (v >= 100) return 'bg-[#004799] text-white'
  if (v >= 80) return 'bg-[#3d6fb0] text-white'
  if (v >= 50) return 'bg-[#9db8d8] text-[#0f2540]'
  return 'bg-[#dbe6f3] text-[#0f2540]'
}

function shiftMonth(yyyymm: string, offset: number): string {
  const year = Number(yyyymm.slice(0, 4))
  const month = Number(yyyymm.slice(4, 6)) - 1
  const d = new Date(year, month + offset, 1)
  return `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}`
}

function currentYyyyMm(): string {
  const now = new Date()
  return `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}`
}

function monthInputValue(yyyymm: string): string {
  return `${yyyymm.slice(0, 4)}-${yyyymm.slice(4, 6)}`
}

function formatMonthLabel(period: string): string {
  const [y, m] = period.split('-')
  return `${y.slice(2)}.${m}`
}

export function UtilizationMatrix() {
  const currentMonth = currentYyyyMm()
  // 기본값: 최근 12개월(설계서 SCR-013 "기간 선택" 기본값 기준)
  const [fromMonth, setFromMonth] = useState(() => shiftMonth(currentMonth, -11))
  const [toMonth, setToMonth] = useState(currentMonth)
  const [dept, setDept] = useState('ALL')
  const [departments, setDepartments] = useState<DepartmentOut[]>([])
  const [matrix, setMatrix] = useState<UtilizationMatrixOut | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [exporting, setExporting] = useState(false)
  const [exportError, setExportError] = useState<string | null>(null)

  async function handleExport() {
    setExporting(true)
    setExportError(null)
    try {
      const params = new URLSearchParams({ from: fromMonth, to: toMonth })
      if (dept !== 'ALL') params.set('dept_id', dept)
      await apiDownloadFile(
        `/api/v1/reports/utilization-matrix/export?${params.toString()}`,
        `utilization_matrix_${fromMonth}_${toMonth}.xlsx`,
      )
    } catch (err) {
      setExportError(err instanceof ApiError ? err.message : 'Excel 내보내기에 실패했습니다.')
    } finally {
      setExporting(false)
    }
  }

  useEffect(() => {
    apiGet<DepartmentOut[]>('/api/v1/departments')
      .then(setDepartments)
      .catch(() => setDepartments([]))
  }, [])

  useEffect(() => {
    setLoading(true)
    setError(null)
    const params = new URLSearchParams({ from: fromMonth, to: toMonth })
    if (dept !== 'ALL') params.set('dept_id', dept)
    apiGet<UtilizationMatrixOut>(`/api/v1/reports/utilization-matrix?${params.toString()}`)
      .then(setMatrix)
      .catch((err) => setError(err instanceof ApiError ? err.message : '가동률 통계를 불러오지 못했습니다.'))
      .finally(() => setLoading(false))
  }, [fromMonth, toMonth, dept])

  const deptOptions = useMemo(
    () => [{ label: '전체', value: 'ALL' }, ...departments.map((d) => ({ label: d.DEPT_NM, value: d.DEPT_ID }))],
    [departments],
  )

  // (사번, 프로젝트) 단위 행 + 프로젝트가 2개 이상인 사원은 "소계" 행을 추가로 붙인다.
  // "사원" 정보는 그룹의 첫 행에만 채우고(rowSpan으로 병합), 나머지 행은 비워둔다.
  const employeeGroups = useMemo(() => {
    if (!matrix) return []
    return matrix.employees.map((e) => {
      const projectRows = e.rows.map((r) => ({
        key: `${e.empl_no}-${r.pjt_nm}-${r.asgn_type_cd}`,
        project: `${ASGN_TYPE_ICON[r.asgn_type_cd]} ${r.pjt_nm}`,
        months: r.monthly,
        avg: r.avg,
        isSubtotal: false,
      }))
      const rows =
        e.rows.length === 0
          ? [
              {
                key: `${e.empl_no}-empty`,
                project: '투입 없음',
                months: e.subtotal,
                avg: e.annual_avg,
                isSubtotal: false,
              },
            ]
          : e.rows.length === 1
            ? projectRows
            : [
                ...projectRows,
                {
                  key: `${e.empl_no}-subtotal`,
                  project: '소계',
                  months: e.subtotal,
                  avg: e.annual_avg,
                  isSubtotal: true,
                },
              ]
      return {
        key: e.empl_no,
        empNo: e.empl_no,
        name: e.empl_nm,
        dept: e.dept_nm,
        rows,
      }
    })
  }, [matrix])

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs text-muted-foreground">기간</span>
        <input
          type="month"
          value={monthInputValue(fromMonth)}
          onChange={(e) => setFromMonth(e.target.value.replace('-', ''))}
          className="h-8 rounded-lg border border-border bg-background px-2 text-sm"
        />
        <span className="text-xs text-muted-foreground">~</span>
        <input
          type="month"
          value={monthInputValue(toMonth)}
          onChange={(e) => setToMonth(e.target.value.replace('-', ''))}
          className="h-8 rounded-lg border border-border bg-background px-2 text-sm"
        />
        <Select value={dept} onValueChange={setDept} options={deptOptions} className="ml-1 w-40" />
        <Button variant="secondary" size="sm" onClick={handleExport} disabled={exporting || !matrix} className="ml-auto">
          <Download className="size-4" />
          {exporting ? '내보내는 중...' : 'Excel 내보내기'}
        </Button>
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}
      {exportError && <p className="text-sm text-destructive">{exportError}</p>}

      {loading ? (
        <p className="py-8 text-center text-sm text-muted-foreground">불러오는 중입니다...</p>
      ) : !matrix || matrix.employees.length === 0 ? (
        <p className="py-8 text-center text-sm text-muted-foreground">조건에 맞는 인력이 없습니다.</p>
      ) : (
        <>
          <div className="overflow-x-auto scrollbar-thin">
            <table className="w-full border-separate border-spacing-0 text-sm">
              <thead>
                <tr>
                  <th className="sticky left-0 z-10 bg-card px-3 py-2 text-left text-xs font-semibold text-muted-foreground">
                    사원
                  </th>
                  <th className="bg-card px-3 py-2 text-left text-xs font-semibold text-muted-foreground">
                    프로젝트
                  </th>
                  {matrix.period.map((p) => (
                    <th key={p} className="min-w-12 px-1 py-2 text-center text-xs font-medium text-muted-foreground">
                      {formatMonthLabel(p)}
                    </th>
                  ))}
                  <th className="px-2 py-2 text-center text-xs font-semibold text-muted-foreground">평균</th>
                </tr>
              </thead>
              <tbody>
                {employeeGroups.map((group) =>
                  group.rows.map((row, i) => (
                    <tr key={row.key} className={cn(row.isSubtotal && 'bg-muted/40 font-semibold')}>
                      {i === 0 && (
                        <td
                          rowSpan={group.rows.length}
                          className="sticky left-0 z-10 bg-card px-3 py-1.5 align-top"
                        >
                          <div className="whitespace-nowrap">
                            <span className="font-medium">
                              {group.empNo} {group.name}
                            </span>
                            <span className="ml-2 text-xs text-muted-foreground">{group.dept}</span>
                          </div>
                        </td>
                      )}
                      <td className="bg-card px-3 py-1.5 whitespace-nowrap text-xs">{row.project}</td>
                      {row.months.map((v, mi) => (
                        <td key={mi} className="px-0.5 py-0.5">
                          <div
                            className={cn(
                              'flex h-8 items-center justify-center rounded text-xs font-medium tabular-nums',
                              cellStyle(v),
                            )}
                            title={`${matrix.period[mi]}: ${v}%`}
                          >
                            {v > 0 ? v : ''}
                            {v > 100 && ' ⚠'}
                          </div>
                        </td>
                      ))}
                      <td className="px-2 text-center">
                        <span className={cn('text-sm font-semibold tabular-nums', row.avg > 100 && 'text-[#c0392b]')}>
                          {row.avg}%
                        </span>
                      </td>
                    </tr>
                  )),
                )}
              </tbody>
              <tfoot>
                <OrgAvgRow label="◆ 조직 평균 [수행중]" values={matrix.org_avg.running_only} />
                <OrgAvgRow label="◆ 조직 평균 [수행중+투입준비중]" values={matrix.org_avg.running_committed} />
                <OrgAvgRow label="★ 전체 조직 평균 [전체]" values={matrix.org_avg.all} bold />
              </tfoot>
            </table>
          </div>

          <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
            <span className="font-medium">범례:</span>
            <span className="flex items-center gap-1.5">🔵 수행중(계약완료)</span>
            <span className="flex items-center gap-1.5">🟠 투입준비중(수주확정)</span>
            <span className="flex items-center gap-1.5">🟢 제안중(제안진행)</span>
            {[
              { label: '~50%', cls: 'bg-[#dbe6f3]' },
              { label: '50~80%', cls: 'bg-[#9db8d8]' },
              { label: '80~100%', cls: 'bg-[#3d6fb0]' },
              { label: '100%', cls: 'bg-[#004799]' },
              { label: '초과', cls: 'bg-[#c0392b]' },
            ].map((l) => (
              <span key={l.label} className="flex items-center gap-1.5">
                <span className={cn('size-3 rounded', l.cls)} />
                {l.label}
              </span>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function OrgAvgRow({ label, values, bold }: { label: string; values: number[]; bold?: boolean }) {
  const avg = values.length ? Math.round((values.reduce((a, b) => a + b, 0) / values.length) * 10) / 10 : 0
  return (
    <tr className={cn('border-t border-border', bold && 'font-semibold')}>
      <td colSpan={2} className="sticky left-0 z-10 bg-card px-3 py-2 text-xs text-muted-foreground">
        {label}
      </td>
      {values.map((v, i) => (
        <td key={i} className="px-1 py-2 text-center text-xs tabular-nums">
          {v}
        </td>
      ))}
      <td className="px-2 py-2 text-center text-xs font-medium tabular-nums">{avg}%</td>
    </tr>
  )
}
