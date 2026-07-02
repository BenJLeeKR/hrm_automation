import type { LucideIcon } from 'lucide-react'
import { Card } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface SectionCardProps {
  title: string
  icon?: LucideIcon
  action?: React.ReactNode
  children: React.ReactNode
  className?: string
  bodyClassName?: string
}

export function SectionCard({
  title,
  icon: Icon,
  action,
  children,
  className,
  bodyClassName,
}: SectionCardProps) {
  return (
    <Card className={cn('flex flex-col', className)}>
      <div className="flex items-center justify-between gap-2 px-5 pt-4 pb-3">
        <div className="flex items-center gap-2">
          {Icon && (
            <span className="flex size-7 items-center justify-center rounded-md bg-accent text-primary">
              <Icon className="size-4" />
            </span>
          )}
          <h3 className="text-sm font-semibold tracking-tight">{title}</h3>
        </div>
        {action}
      </div>
      <div className={cn('flex-1 px-5 pb-5', bodyClassName)}>{children}</div>
    </Card>
  )
}
