import type { LucideIcon } from 'lucide-react'
import { TrendingUp, TrendingDown } from 'lucide-react'
import { Card } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface StatCardProps {
  label: string
  value: string
  unit?: string
  icon: LucideIcon
  tone?: 'primary' | 'success' | 'warning' | 'info' | 'muted' | 'danger'
  trend?: { value: string; up: boolean }
  hint?: string
}

const toneStyles: Record<
  NonNullable<StatCardProps['tone']>,
  { bg: string; fg: string }
> = {
  primary: { bg: 'bg-accent', fg: 'text-primary' },
  success: { bg: 'bg-[#e5f6ee]', fg: 'text-[#0f7a52]' },
  warning: { bg: 'bg-[#fdf0dc]', fg: 'text-[#b46708]' },
  info: { bg: 'bg-[#dcf5f2]', fg: 'text-[#0b7268]' },
  muted: { bg: 'bg-secondary', fg: 'text-muted-foreground' },
  danger: { bg: 'bg-[#fde8e8]', fg: 'text-[#c0392b]' },
}

export function StatCard({
  label,
  value,
  unit,
  icon: Icon,
  tone = 'primary',
  trend,
  hint,
}: StatCardProps) {
  const t = toneStyles[tone]
  return (
    <Card className="p-4">
      <div className="flex items-start justify-between gap-2">
        <div className={cn('flex size-9 items-center justify-center rounded-lg', t.bg)}>
          <Icon className={cn('size-[18px]', t.fg)} />
        </div>
        {trend && (
          <span
            className={cn(
              'inline-flex items-center gap-0.5 rounded-md px-1.5 py-0.5 text-xs font-medium',
              trend.up ? 'bg-[#e5f6ee] text-[#0f7a52]' : 'bg-[#fde8e8] text-[#c0392b]',
            )}
          >
            {trend.up ? (
              <TrendingUp className="size-3" />
            ) : (
              <TrendingDown className="size-3" />
            )}
            {trend.value}
          </span>
        )}
      </div>
      <p className="mt-3 text-xs font-medium text-muted-foreground">{label}</p>
      <p className="mt-1 flex items-baseline gap-1">
        <span className="text-2xl font-bold tracking-tight">{value}</span>
        {unit && <span className="text-sm text-muted-foreground">{unit}</span>}
      </p>
      {hint && <p className="mt-1 text-xs text-muted-foreground">{hint}</p>}
    </Card>
  )
}
