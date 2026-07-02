'use client'

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { skillDistributionTop10 } from '@/lib/mock-data'

export function SkillBarChart() {
  return (
    <ResponsiveContainer width="100%" height={320}>
      <BarChart
        data={skillDistributionTop10}
        layout="vertical"
        margin={{ left: 12, right: 16, top: 4, bottom: 4 }}
      >
        <CartesianGrid horizontal={false} stroke="var(--border)" />
        <XAxis
          type="number"
          tick={{ fontSize: 12, fill: 'var(--muted-foreground)' }}
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          type="category"
          dataKey="name"
          width={90}
          tick={{ fontSize: 12, fill: 'var(--muted-foreground)' }}
          axisLine={false}
          tickLine={false}
        />
        <Tooltip
          cursor={{ fill: 'var(--secondary)' }}
          contentStyle={{
            borderRadius: 8,
            border: '1px solid var(--border)',
            fontSize: 12,
          }}
          formatter={(v) => [`${v}명`, '보유 인원']}
        />
        <Bar dataKey="count" fill="var(--primary)" radius={[0, 4, 4, 0]} barSize={16} />
      </BarChart>
    </ResponsiveContainer>
  )
}
