import * as React from 'react'
import { cn } from '@/lib/utils'

interface AvatarProps extends React.ComponentProps<'div'> {
  name?: string
}

function Avatar({ name, className, children, ...props }: AvatarProps) {
  const initials = name ? name.trim().slice(0, 2) : ''
  return (
    <div
      className={cn(
        'flex size-9 shrink-0 select-none items-center justify-center overflow-hidden rounded-full bg-accent text-xs font-semibold text-accent-foreground',
        className,
      )}
      {...props}
    >
      {children ?? initials}
    </div>
  )
}

export { Avatar }
