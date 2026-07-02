'use client'

import { useState } from 'react'
import { Sparkles, Search, Trophy, Medal, Award } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { EmptyState } from '@/components/common/empty-state'
import { recommendations } from '@/lib/mock-data'
import { jobTypeOptions, skillOptions } from '@/lib/options'
import type { RecommendationRow } from '@/lib/types'

const SCORE_LABELS: { key: keyof RecommendationRow['detail']; label: string }[] = [
  { key: 'jobMatch', label: '직무 적합' },
  { key: 'skillMatch', label: '기술 일치' },
  { key: 'proficiency', label: '숙련도' },
  { key: 'availability', label: '가동 가능' },
  { key: 'experience', label: '경력' },
  { key: 'roleFit', label: '역할 부합' },
]

const RANK_META = [
  { icon: Trophy, cls: 'bg-[#fdf5e3] text-[#b8860b]' },
  { icon: Medal, cls: 'bg-secondary text-foreground' },
  { icon: Award, cls: 'bg-[#f4ede4] text-[#a06a3d]' },
]

function scoreColor(v: number) {
  if (v >= 90) return 'bg-[#0f7a52]'
  if (v >= 75) return 'bg-primary'
  if (v >= 60) return 'bg-[#b46708]'
  return 'bg-muted-foreground'
}

export default function RecommendationsPage() {
  const [jobType, setJobType] = useState('ALL')
  const [skill, setSkill] = useState('ALL')
  const [role, setRole] = useState('')
  const [submitted, setSubmitted] = useState(false)

  return (
    <div>
      <PageHeader
        title="리소스 추천"
        description="프로젝트 요건을 입력하면 적합도 점수 기반으로 최적 인력을 추천합니다."
      />

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="size-4 text-primary" />
              요건 입력
            </CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="req-role">요청 역할</Label>
              <Input
                id="req-role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder="예: 백엔드 아키텍트"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label>필요 직무</Label>
              <Select value={jobType} onValueChange={setJobType} options={jobTypeOptions} />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label>핵심 기술</Label>
              <Select value={skill} onValueChange={setSkill} options={skillOptions} />
            </div>
            <Button className="mt-1" onClick={() => setSubmitted(true)}>
              <Search className="size-4" />
              추천 인력 조회
            </Button>
            <p className="text-xs leading-relaxed text-muted-foreground">
              적합도는 직무·기술·숙련도·가동 가능성·경력·역할 부합도를 가중 합산하여
              산출됩니다.
            </p>
          </CardContent>
        </Card>

        <div className="flex flex-col gap-4 lg:col-span-2">
          {!submitted ? (
            <Card>
              <CardContent className="py-12">
                <EmptyState
                  title="요건을 입력하고 조회하세요"
                  description="좌측 폼에서 역할·직무·기술을 선택한 뒤 추천 인력 조회를 실행하면 순위별 추천 결과가 표시됩니다."
                />
              </CardContent>
            </Card>
          ) : (
            recommendations.map((rec, idx) => {
              const meta = RANK_META[idx] ?? RANK_META[2]
              const Icon = meta.icon
              return (
                <Card key={rec.rank}>
                  <CardContent className="pt-6">
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <div
                          className={`flex size-10 items-center justify-center rounded-full ${meta.cls}`}
                        >
                          <Icon className="size-5" />
                        </div>
                        <div>
                          <p className="flex items-center gap-2 font-semibold">
                            {rec.name}
                            <span className="text-xs font-normal text-muted-foreground">
                              {rec.jobType}
                            </span>
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {rec.reason}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold tabular-nums text-primary">
                          {rec.score}
                        </p>
                        <p className="text-xs text-muted-foreground">적합도 점수</p>
                      </div>
                    </div>

                    <div className="mt-4 flex flex-wrap items-center gap-2">
                      {rec.skills.map((s) => (
                        <Badge key={s} variant="secondary">
                          {s}
                        </Badge>
                      ))}
                      <Badge variant={rec.availableDate === '즉시' ? 'success' : 'outline'}>
                        {rec.availableDate === '즉시'
                          ? '즉시 가동'
                          : `가동 ${rec.availableDate}`}
                      </Badge>
                    </div>

                    <div className="mt-5 grid grid-cols-2 gap-x-6 gap-y-3 sm:grid-cols-3">
                      {SCORE_LABELS.map((s) => {
                        const v = rec.detail[s.key]
                        return (
                          <div key={s.key}>
                            <div className="flex items-center justify-between text-xs">
                              <span className="text-muted-foreground">{s.label}</span>
                              <span className="font-semibold tabular-nums">{v}</span>
                            </div>
                            <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-secondary">
                              <div
                                className={`h-full rounded-full ${scoreColor(v)}`}
                                style={{ width: `${v}%` }}
                              />
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </CardContent>
                </Card>
              )
            })
          )}
        </div>
      </div>
    </div>
  )
}
