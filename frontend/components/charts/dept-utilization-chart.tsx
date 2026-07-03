'use client'

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

function barColor(v: number) {
  if (v >= 80) return '#004799'
  if (v >= 60) return '#3b82f6'
  return '#8ab4e8'
}

export interface DeptUtilizationPoint {
  team: string
  value: number
}

export function DeptUtilizationChart({ data: deptUtilization }: { data: DeptUtilizationPoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart
        data={deptUtilization}
        layout="vertical"
        margin={{ top: 4, right: 24, left: 8, bottom: 4 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#eef1f5" horizontal={false} />
        <XAxis
          type="number"
          domain={[0, 100]}
          tick={{ fontSize: 11, fill: '#6b7280' }}
          axisLine={false}
          tickLine={false}
          unit="%"
        />
        <YAxis
          type="category"
          dataKey="team"
          tick={{ fontSize: 12, fill: '#16181d' }}
          axisLine={false}
          tickLine={false}
          width={80}
        />
        <Tooltip
          cursor={{ fill: '#f1f4f8' }}
          contentStyle={{
            borderRadius: 12,
            border: '1px solid #e4e8ee',
            fontSize: 12,
          }}
          formatter={(v) => [`${v}%`, '가동률']}
        />
        <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={22}>
          {deptUtilization.map((d, i) => (
            <Cell key={i} fill={barColor(d.value)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
