import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils'

interface UtilizationProgressProps {
  value: number
  showLabel?: boolean
  className?: string
}

export function UtilizationProgress({
  value,
  showLabel = true,
  className,
}: UtilizationProgressProps) {
  const over = value > 100
  return (
    <div className={cn('flex items-center gap-2', className)}>
      <Progress
        value={value}
        className="min-w-16 flex-1"
        indicatorClassName={cn(
          over ? 'bg-destructive' : value === 0 ? 'bg-[#0f9d67]' : 'bg-primary',
        )}
      />
      {showLabel && (
        <span
          className={cn(
            'w-11 shrink-0 text-right text-xs font-semibold tabular-nums',
            over && 'text-destructive',
          )}
        >
          {value}%
        </span>
      )}
    </div>
  )
}

export const UtilizationBar = UtilizationProgress
