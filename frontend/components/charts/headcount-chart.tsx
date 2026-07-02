'use client'

import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  ComposedChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { headcountTrend } from '@/lib/mock-data'

export function HeadcountChart() {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <ComposedChart
        data={headcountTrend}
        margin={{ top: 8, right: 8, left: -16, bottom: 0 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#eef1f5" vertical={false} />
        <XAxis
          dataKey="month"
          tick={{ fontSize: 11, fill: '#6b7280' }}
          axisLine={{ stroke: '#e4e8ee' }}
          tickLine={false}
        />
        <YAxis
          tick={{ fontSize: 11, fill: '#6b7280' }}
          axisLine={false}
          tickLine={false}
        />
        <Tooltip
          contentStyle={{
            borderRadius: 12,
            border: '1px solid #e4e8ee',
            fontSize: 12,
            boxShadow: '0 8px 24px rgba(0,0,0,0.08)',
          }}
          formatter={(v, name) => {
            const labels: Record<string, string> = {
              total: '전체 인원',
              hires: '신규 입사',
              exits: '퇴사',
            }
            return [`${v}명`, labels[String(name)] ?? String(name)]
          }}
        />
        <Legend
          formatter={(value) => {
            const labels: Record<string, string> = {
              total: '전체 인원',
              hires: '신규 입사',
              exits: '퇴사',
            }
            return (
              <span style={{ fontSize: 12, color: '#6b7280' }}>
                {labels[value] ?? value}
              </span>
            )
          }}
        />
        <Bar dataKey="hires" fill="#8ab4e8" radius={[4, 4, 0, 0]} barSize={14} />
        <Bar dataKey="exits" fill="#e4e8ee" radius={[4, 4, 0, 0]} barSize={14} />
        <Line
          type="monotone"
          dataKey="total"
          stroke="#004799"
          strokeWidth={2.5}
          dot={{ r: 3, fill: '#004799' }}
          activeDot={{ r: 5 }}
        />
      </ComposedChart>
    </ResponsiveContainer>
  )
}
