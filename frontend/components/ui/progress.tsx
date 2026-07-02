import * as React from 'react'
import { cn } from '@/lib/utils'

interface ProgressProps extends React.ComponentProps<'div'> {
  value?: number
  indicatorClassName?: string
}

function Progress({
  value = 0,
  className,
  indicatorClassName,
  ...props
}: ProgressProps) {
  return (
    <div
      className={cn(
        'relative h-2 w-full overflow-hidden rounded-full bg-secondary',
        className,
      )}
      {...props}
    >
      <div
        className={cn(
          'h-full rounded-full bg-primary transition-all',
          indicatorClassName,
        )}
        style={{ width: `${Math.min(Math.max(value, 0), 100)}%` }}
      />
    </div>
  )
}

export { Progress }
