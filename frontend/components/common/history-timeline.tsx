import type { AuditTrail } from '@/lib/types'
import { EmptyState } from './empty-state'

export function HistoryTimeline({ items }: { items: AuditTrail[] }) {
  if (items.length === 0) {
    return <EmptyState title="변경 이력이 없습니다" description="기록된 변경 사항이 아직 없습니다." />
  }
  return (
    <ol className="relative ml-2 border-l border-border">
      {items.map((item, i) => (
        <li key={i} className="mb-5 ml-5 last:mb-0">
          <span className="absolute -left-[6.5px] mt-1 size-3 rounded-full border-2 border-card bg-primary" />
          <div className="flex flex-wrap items-center gap-x-2 gap-y-0.5">
            <span className="text-sm font-medium text-foreground">{item.message}</span>
          </div>
          <p className="mt-0.5 text-xs text-muted-foreground">
            {item.at} · <span className="font-medium">{item.user}</span>
          </p>
        </li>
      ))}
    </ol>
  )
}
