'use client'

import { Calendar } from 'lucide-react'
import { cn } from '@/lib/utils'

interface DateRangePickerProps {
  from?: string
  to?: string
  onFromChange?: (v: string) => void
  onToChange?: (v: string) => void
  className?: string
}

export function DateRangePicker({
  from,
  to,
  onFromChange,
  onToChange,
  className,
}: DateRangePickerProps) {
  return (
    <div
      className={cn(
        'flex items-center gap-2 rounded-lg border border-input bg-card px-3 shadow-sm',
        className,
      )}
    >
      <Calendar className="size-4 shrink-0 text-muted-foreground" />
      <input
        type="date"
        value={from}
        onChange={(e) => onFromChange?.(e.target.value)}
        className="h-9 bg-transparent text-sm outline-none"
      />
      <span className="text-muted-foreground">~</span>
      <input
        type="date"
        value={to}
        onChange={(e) => onToChange?.(e.target.value)}
        className="h-9 bg-transparent text-sm outline-none"
      />
    </div>
  )
}
