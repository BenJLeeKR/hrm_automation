import { cn } from '@/lib/utils'

export function SkillLevel({ level }: { level: number }) {
  return (
    <span className="inline-flex items-center gap-1" aria-label={`숙련도 ${level}단계`}>
      {[1, 2, 3, 4, 5].map((n) => (
        <span
          key={n}
          className={cn(
            'size-2 rounded-full',
            n <= level ? 'bg-primary' : 'bg-secondary',
          )}
        />
      ))}
      <span className="ml-1 text-xs font-medium text-muted-foreground">Lv.{level}</span>
    </span>
  )
}
