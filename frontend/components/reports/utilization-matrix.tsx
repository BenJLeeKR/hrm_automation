'use client'

import { utilizationMatrix, matrixMonths } from '@/lib/mock-data'
import { cn } from '@/lib/utils'

function cellStyle(v: number): string {
  if (v <= 0) return 'bg-secondary text-muted-foreground'
  if (v > 100) return 'bg-[#c0392b] text-white'
  if (v >= 100) return 'bg-[#004799] text-white'
  if (v >= 80) return 'bg-[#3d6fb0] text-white'
  if (v >= 50) return 'bg-[#9db8d8] text-[#0f2540]'
  return 'bg-[#dbe6f3] text-[#0f2540]'
}

export function UtilizationMatrix() {
  return (
    <div className="overflow-x-auto scrollbar-thin">
      <table className="w-full border-separate border-spacing-0 text-sm">
        <thead>
          <tr>
            <th className="sticky left-0 z-10 bg-card px-3 py-2 text-left text-xs font-semibold text-muted-foreground">
              사원 / 프로젝트
            </th>
            {matrixMonths.map((m) => (
              <th
                key={m}
                className="min-w-12 px-1 py-2 text-center text-xs font-medium text-muted-foreground"
              >
                {m}
              </th>
            ))}
            <th className="px-2 py-2 text-center text-xs font-semibold text-muted-foreground">
              평균
            </th>
          </tr>
        </thead>
        <tbody>
          {utilizationMatrix.map((row) => (
            <tr key={row.empNo}>
              <td className="sticky left-0 z-10 bg-card px-3 py-1.5">
                <div className="whitespace-nowrap">
                  <span className="font-medium">{row.name}</span>
                  <span className="ml-2 text-xs text-muted-foreground">
                    {row.project}
                  </span>
                </div>
              </td>
              {row.months.map((v, i) => (
                <td key={i} className="px-0.5 py-0.5">
                  <div
                    className={cn(
                      'flex h-8 items-center justify-center rounded text-xs font-medium tabular-nums',
                      cellStyle(v),
                    )}
                    title={`${matrixMonths[i]}: ${v}%`}
                  >
                    {v > 0 ? v : ''}
                  </div>
                </td>
              ))}
              <td className="px-2 text-center">
                <span
                  className={cn(
                    'text-sm font-semibold tabular-nums',
                    row.avg > 100 && 'text-[#c0392b]',
                  )}
                >
                  {row.avg}%
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-4 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
        <span className="font-medium">범례:</span>
        {[
          { label: '대기(0%)', cls: 'bg-secondary' },
          { label: '~50%', cls: 'bg-[#dbe6f3]' },
          { label: '50~80%', cls: 'bg-[#9db8d8]' },
          { label: '80~100%', cls: 'bg-[#3d6fb0]' },
          { label: '100%', cls: 'bg-[#004799]' },
          { label: '초과', cls: 'bg-[#c0392b]' },
        ].map((l) => (
          <span key={l.label} className="flex items-center gap-1.5">
            <span className={cn('size-3 rounded', l.cls)} />
            {l.label}
          </span>
        ))}
      </div>
    </div>
  )
}
