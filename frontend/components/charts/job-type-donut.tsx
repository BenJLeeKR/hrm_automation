'use client'

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'

const COLORS = [
  '#004799',
  '#3b82f6',
  '#0d9488',
  '#ea8a0c',
  '#8ab4e8',
  '#64748b',
  '#b91c1c',
]

export interface JobTypeDistributionPoint {
  name: string
  value: number
}

export function JobTypeDonut({ data: jobTypeDistribution }: { data: JobTypeDistributionPoint[] }) {
  const total = jobTypeDistribution.reduce((s, d) => s + d.value, 0)
  return (
    <div className="flex flex-col items-center gap-4 sm:flex-row">
      <div className="relative h-[180px] w-[180px] shrink-0">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={jobTypeDistribution}
              dataKey="value"
              nameKey="name"
              innerRadius={54}
              outerRadius={80}
              paddingAngle={2}
              stroke="none"
            >
              {jobTypeDistribution.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                borderRadius: 12,
                border: '1px solid #e4e8ee',
                fontSize: 12,
              }}
              formatter={(v) => [`${v}명`, '인원']}
            />
          </PieChart>
        </ResponsiveContainer>
        <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-xs text-muted-foreground">전체</span>
          <span className="text-xl font-bold">{total}명</span>
        </div>
      </div>
      <ul className="grid flex-1 grid-cols-1 gap-1.5">
        {jobTypeDistribution.map((d, i) => (
          <li key={d.name} className="flex items-center justify-between gap-2 text-xs">
            <span className="flex items-center gap-2">
              <span
                className="size-2.5 rounded-full"
                style={{ backgroundColor: COLORS[i % COLORS.length] }}
              />
              <span className="text-foreground">{d.name}</span>
            </span>
            <span className="font-semibold tabular-nums">{d.value}명</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
