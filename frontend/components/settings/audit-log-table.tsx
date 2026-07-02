'use client'

import { useMemo, useState } from 'react'
import { ChevronRight } from 'lucide-react'
import { SearchInput } from '@/components/common/search-input'
import { Select } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogHeader, DialogBody } from '@/components/ui/dialog'
import { auditLogs } from '@/lib/mock-data'
import { cn } from '@/lib/utils'
import type { AuditLog } from '@/lib/types'

const ACTION_META: Record<
  string,
  { label: string; variant: 'success' | 'info' | 'warning' | 'danger' | 'muted' }
> = {
  CREATE: { label: '생성', variant: 'success' },
  UPDATE: { label: '수정', variant: 'info' },
  DELETE: { label: '삭제', variant: 'danger' },
  LOGIN: { label: '로그인', variant: 'muted' },
  IMPORT: { label: '일괄등록', variant: 'warning' },
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
  const [detail, setDetail] = useState<AuditLog | null>(null)

  const filtered = useMemo(
    () =>
      auditLogs.filter((l) => {
        if (action !== 'ALL' && l.action !== action) return false
        if (
          keyword &&
          !`${l.user}${l.targetTable}${l.targetId}`
            .toLowerCase()
            .includes(keyword.toLowerCase())
        )
          return false
        return true
      }),
    [keyword, action],
  )

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-3 sm:flex-row">
        <SearchInput
          value={keyword}
          onChange={setKeyword}
          placeholder="사용자 · 테이블 · 대상 검색"
          className="sm:max-w-xs"
        />
        <Select
          value={action}
          onValueChange={setAction}
          options={actionOptions}
          className="sm:w-44"
        />
      </div>

      <div className="overflow-hidden rounded-lg border border-border">
        <table className="w-full text-sm">
          <thead className="bg-muted/60">
            <tr>
              {['시각', '사용자', '작업', '대상 테이블', '대상 ID', 'IP', ''].map(
                (h) => (
                  <th
                    key={h}
                    className="px-3 py-2.5 text-left text-xs font-semibold text-muted-foreground"
                  >
                    {h}
                  </th>
                ),
              )}
            </tr>
          </thead>
          <tbody>
            {filtered.map((l) => {
              const meta = ACTION_META[l.action] ?? {
                label: l.action,
                variant: 'muted' as const,
              }
              return (
                <tr
                  key={l.id}
                  onClick={() => setDetail(l)}
                  className="cursor-pointer border-t border-border transition-colors hover:bg-secondary/50"
                >
                  <td className="whitespace-nowrap px-3 py-2.5 font-mono text-xs tabular-nums text-muted-foreground">
                    {l.at}
                  </td>
                  <td className="px-3 py-2.5 font-medium">{l.user}</td>
                  <td className="px-3 py-2.5">
                    <Badge variant={meta.variant}>{meta.label}</Badge>
                  </td>
                  <td className="px-3 py-2.5 font-mono text-xs">{l.targetTable}</td>
                  <td className="px-3 py-2.5 font-mono text-xs text-muted-foreground">
                    {l.targetId}
                  </td>
                  <td className="px-3 py-2.5 font-mono text-xs text-muted-foreground">
                    {l.clientIp}
                  </td>
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
          description={detail ? `${detail.id} · ${detail.at}` : undefined}
          onClose={() => setDetail(null)}
        />
        {detail && (
          <DialogBody className="flex flex-col gap-4">
            <dl className="grid grid-cols-2 gap-x-6 gap-y-3 text-sm sm:grid-cols-3">
              <div>
                <dt className="text-xs text-muted-foreground">사용자</dt>
                <dd className="mt-0.5 font-medium">{detail.user}</dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">작업</dt>
                <dd className="mt-0.5">
                  <Badge
                    variant={(ACTION_META[detail.action]?.variant) ?? 'muted'}
                  >
                    {ACTION_META[detail.action]?.label ?? detail.action}
                  </Badge>
                </dd>
              </div>
              <div>
                <dt className="text-xs text-muted-foreground">대상</dt>
                <dd className="mt-0.5 font-mono text-xs">
                  {detail.targetTable} / {detail.targetId}
                </dd>
              </div>
            </dl>
            <div className={cn('flex flex-col gap-4 sm:flex-row')}>
              <JsonBlock title="변경 전 (before)" data={detail.before} />
              <JsonBlock title="변경 후 (after)" data={detail.after} />
            </div>
            <div>
              <p className="mb-1 text-xs font-semibold text-muted-foreground">
                User Agent
              </p>
              <p className="break-all font-mono text-xs text-muted-foreground">
                {detail.userAgent}
              </p>
            </div>
          </DialogBody>
        )}
      </Dialog>
    </div>
  )
}
