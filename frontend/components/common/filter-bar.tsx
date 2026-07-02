import { Card } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface FilterBarProps {
  children: React.ReactNode
  className?: string
}

export function FilterBar({ children, className }: FilterBarProps) {
  return (
    <Card className={cn('mb-4 p-4', className)}>
      <div className="flex flex-wrap items-end gap-3">{children}</div>
    </Card>
  )
}

interface FilterFieldProps {
  label: string
  children: React.ReactNode
  className?: string
}

export function FilterField({ label, children, className }: FilterFieldProps) {
  return (
    <div className={cn('flex min-w-36 flex-col gap-1.5', className)}>
      <span className="text-xs font-medium text-muted-foreground">{label}</span>
      {children}
    </div>
  )
}
