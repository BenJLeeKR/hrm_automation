'use client'

import { useEffect, useMemo, useState } from 'react'
import { ChevronRight, Download } from 'lucide-react'
import { SearchInput } from '@/components/common/search-input'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogHeader, DialogBody } from '@/components/ui/dialog'
import { apiGet, apiDownloadFile, ApiError } from '@/lib/api'
import { cn } from '@/lib/utils'

// 백엔드 감사 로그 API(로드맵 §8 "설정 화면 구현", SCR-016) 응답 타입 — 필드명은
// backend/app/schemas/sys_audit_log.py와 동일하게 유지한다. Excel 내보내기(§9-1)는
// `GET /audit-logs/export`로 별도 제공한다.
interface AuditLogItem {
  AUDIT_ID: string
  USER_LGID: string
  ACT_CD: string
  TGT_TBL_NM: string
  TGT_ID: string | null
  BFR_VAL_JSON: Record<string, unknown> | null
  AFT_VAL_JSON: Record<string, unknown> | null
  CLNT_IP: string | null
  USER_AGT: string | null
  REG_DTTM: string
}
interface AuditLogListResponse {
  items: AuditLogItem[]
  total: number
}

const ACTION_META: Record<string, { label: string; variant: 'success' | 'info' | 'warning' | 'danger' | 'muted' }> = {
  CREATE: { label: '생성', variant: 'success' },
  UPDATE: { label: '수정', variant: 'info' },
  DELETE: { label: '삭제', variant: 'danger' },
  LOGIN: { label: '로그인', variant: 'muted' },
  IMPORT: { label: '일괄등록', variant: 'warning' },
  EXPORT: { label: '내보내기', variant: 'warning' },
}

const actionOptions = [
  { value: 'ALL', label: '전체 작업' },
  ...Object.entries(ACTION_META).map(([value, m]) => ({ value, label: m.label })),
]

function JsonBlock({ title, data }: { title: string; data: unknown }) {
  return (
    <div className="flex-1">
      <p className="mb-1.5 text-xs font-semibold text-muted-foreground">{title}</p>
      <pre className="overflow-x-auto scrollbar-thin rounded-lg border border-border bg-muted/50 p-3 font-mono text-xs leading-relaxed">
        {data ? JSON.stringify(data, null, 2) : '—'}
      </pre>
    </div>
  )
}

export function AuditLogTable() {
  const [keyword, setKeyword] = useState('')
  const [action, setAction] = useState('ALL')
  const [logs, setLogs] = useState<AuditLogItem[]>([])
  const [total, setTotal] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [detail, setDetail] = useState<AuditLogItem | null>(null)
  const [exporting, setExporting] = useState(false)
  const [exportError, setExportError] = useState<string | null>(null)

  async function handleExport() {
    setExporting(true)
    setExportError(null)
    try {
      const params = new URLSearchParams()
      if (action !== 'ALL') params.set('act_cd', action)
      if (keyword) params.set('user_lgid', keyword)
      await apiDownloadFile(`/api/v1/audit-logs/export?${params.toString()}`, 'audit_logs.xlsx')
    } catch (err) {
      setExportError(err instanceof ApiError ? err.message : 'Excel 내보내기에 실패했습니다.')
    } finally {
      setExporting(false)
    }
  }

  useEffect(() => {
    setLoading(true)
    const params = new URLSearchParams({ limit: '100' })
    if (action !== 'ALL') params.set('act_cd', action)
    if (keyword) params.set('user_lgid', keyword)

    apiGet<AuditLogListResponse>(`/api/v1/audit-logs?${params.toString()}`)
      .then((res) => {
        setLogs(res.items)
        setTotal(res.total)
        setError(null)
      })
      .catch((err) => setError(err instanceof ApiError ? err.message : '감사 로그를 불러오지 못했습니다.'))
      .finally(() => setLoading(false))
  }, [action, keyword])

  const filtered = useMemo(
    () =>
      logs.filter((l) => {
        // user_lgid는 서버에서 이미 필터링되지만, 테이블/대상 ID 검색은 클라이언트에서 보강한다
        if (
          keyword &&
          !`${l.USER_LGID}${l.TGT_TBL_NM}${l.TGT_ID ?? ''}`.toLowerCase().includes(keyword.toLowerCase())
        )
          return false
        return true
      }),
    [logs, keyword],
  )

  return (
    <div className="flex flex-col gap-4">
      {error && <p className="text-sm text-destructive">{error}</p>}
      {exportError && <p className="text-sm text-destructive">{exportError}</p>}

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <SearchInput
          value={keyword}
          onChange={setKeyword}
          placeholder="사용자 · 테이블 · 대상 검색"
          className="sm:max-w-xs"
        />
        <Select value={action} onValueChange={setAction} options={actionOptions} className="sm:w-44" />
        <span className="text-xs text-muted-foreground sm:ml-auto">전체 {total.toLocaleString()}건 중 최근 {logs.length}건 표시</span>
        <Button variant="secondary" size="sm" onClick={handleExport} disabled={exporting}>
          <Download className="size-4" />
          {exporting ? '내보내는 중...' : 'Excel 내보내기'}
        </Button>
      </div>

      <div className="overflow-hidden rounded-lg border border-border">
        <table className="w-full text-sm">
          <thead className="bg-muted/60">
            <tr>
              {['시각', '사용자', '작업', '대상 테이블', '대상 ID', 'IP', ''].map((h) => (
                <th key={h} className="px-3 py-2.5 text-left text-xs font-semibold text-muted-foreground">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 && (
              <tr>
                <td colSpan={7} className="px-3 py-6 text-center text-sm text-muted-foreground">
                  {loading ? '불러오는 중입니다...' : '조건에 맞는 로그가 없습니다.'}
                </td>
              </tr>
            )}
            {filtered.map((l) => {
              const meta = ACTION_META[l.ACT_CD] ?? { label: l.ACT_CD, variant: 'muted' as const }
              return (
                <tr
                  key={l.AUDIT_ID}
                  onClick={() => setDetail(l)}
                  className="cursor-pointer border-t border-border transition-colors hover:bg-secondary/50"
                >
                  <td className="whitespace-nowrap px-3 py-2.5 font-mono text-xs tabular-nums text-muted-foreground">
                    {l.REG_DTTM}
                  </td>
                  <td className="px-3 py-2.5 font-medium">{l.USER_LGID}</td>
                  <td className="px-3 py-2.5">
                    <Badge variant={meta.variant}>{meta.label}</Badge>
                  </td>
                  <td className="px-3 py-2.5 font-mono text-xs">{l.TGT_TBL_NM}</td>
                  <td className="px-3 py-2.5 font-mono text-xs text-muted-foreground">{l.TGT_ID ?? '-'}</td>
                  <td className="px-3 py-2.5 font-mono text-xs text-muted-foreground">{l.CLNT_IP ?? '-'}</td>
                  <td className="px-3 py-2.5 text-right">
                    <ChevronRight className="size-4 text-muted-foreground" />
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      <Dialog open={detail !== null} onClose={() => setDetail(null)} className="max-w-2xl">
        <DialogHeader
          title="감사 로그 상세"
          description={detail ? `${detail.AUDIT_ID} · ${detail.REG_DTTM}` : undefined}
          onClose={() => setDetail(null)}
        />
        {detail && (
          <DialogBody className="flex flex-col gap-4">
            <dl className="grid grid-cols-2 gap-x-6 gap-y-3 text-sm sm:grid-cols-3">
              <div>
                <dt className="text-xs text-muted-foreground">사용자</dt>
                <dd className="mt-0.5 font-medium">{detail.USER_LGID}</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">작업</dt>
                <dd className="mt-0.5">
                  <Badge variant={(ACTION_META[detail.ACT_CD]?.variant) ?? 'muted'}>
                    {ACTION_META[detail.ACT_CD]?.label ?? detail.ACT_CD}
                  </Badge>
                </dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">대상</dt>
                <dd className="mt-0.5 font-mono text-xs">
                  {detail.TGT_TBL_NM} / {detail.TGT_ID ?? '-'}
                </dd>
              </div>
            </dl>
            <div className={cn('flex flex-col gap-4 sm:flex-row')}>
              <JsonBlock title="변경 전 (before)" data={detail.BFR_VAL_JSON} />
              <JsonBlock title="변경 후 (after)" data={detail.AFT_VAL_JSON} />
            </div>
            <div>
              <p className="mb-1 text-xs font-semibold text-muted-foreground">User Agent</p>
              <p className="break-all font-mono text-xs text-muted-foreground">{detail.USER_AGT ?? '-'}</p>
            </div>
          </DialogBody>
        )}
      </Dialog>
    </div>
  )
}
