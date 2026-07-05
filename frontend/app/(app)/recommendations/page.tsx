'use client'

import { useEffect, useMemo, useState } from 'react'
import { Sparkles, Search, Trophy, Medal, Award, X, UserPlus } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { EmptyState } from '@/components/common/empty-state'
import { AssignmentFormModal } from '@/components/projects/assignment-form-modal'
import { apiGet, apiPost, ApiError } from '@/lib/api'

// 백엔드 리소스 추천 API(로드맵 §8 "리소스 추천 화면 구현", SCR-011) 응답 타입 —
// 필드명은 backend/app/schemas/pjt_rcmd_rslt.py, pjt_rsrc_req.py와 동일하게 유지한다.
interface ProjectOut {
  PJT_ID: string
  PJT_NM: string
}
interface ProjectListResponse {
  items: ProjectOut[]
}
interface JobTypeOut {
  JIKMU_ID: string
  JIKMU_NM: string
}
interface SkillOut {
  SKILL_ID: string
  SKILL_NM: string
}
interface EmployeeOut {
  EMPL_ID: string
  EMPL_NO: string
  EMPL_NM: string
  JIKMU_ID: string | null
}
interface EmployeeListResponse {
  items: EmployeeOut[]
}
interface EmployeeSkillOut {
  EMPL_ID: string
  SKILL_ID: string
}
interface ResourceRequestOut {
  REQ_ID: string
}
interface RecommendationResultOut {
  RCMD_ID: string
  EMPL_ID: string
  RCMD_RANK: number
  TOT_SCORE: number
  SCORE_DTL_JSON: {
    job_match: number
    skill_match: number
    proficiency: number
    availability: number
    experience: number
    role_fit: number
  } | null
  RCMD_RSN: string | null
}

interface ResultRow extends RecommendationResultOut {
  empName: string
  jobTypeName: string | null
  skillNames: string[]
}

// 상세 점수 카드에 표시할 6개 항목 — 가중치는 backend/app/repositories/pjt_rcmd_rslt.py와 동일
const SCORE_LABELS: { key: keyof NonNullable<RecommendationResultOut['SCORE_DTL_JSON']>; label: string; max: number }[] = [
  { key: 'job_match', label: '직무 적합', max: 15 },
  { key: 'skill_match', label: '기술 일치', max: 35 },
  { key: 'proficiency', label: '숙련도', max: 25 },
  { key: 'availability', label: '가동 가능', max: 15 },
  { key: 'experience', label: '경력', max: 7 },
  { key: 'role_fit', label: '역할 부합', max: 3 },
]

const RANK_META = [
  { icon: Trophy, cls: 'bg-[#fdf5e3] text-[#b8860b]' },
  { icon: Medal, cls: 'bg-secondary text-foreground' },
  { icon: Award, cls: 'bg-[#f4ede4] text-[#a06a3d]' },
]

function scoreColor(ratio: number) {
  if (ratio >= 0.9) return 'bg-[#0f7a52]'
  if (ratio >= 0.75) return 'bg-primary'
  if (ratio >= 0.6) return 'bg-[#b46708]'
  return 'bg-muted-foreground'
}

export default function RecommendationsPage() {
  const [projects, setProjects] = useState<ProjectOut[]>([])
  const [jobTypes, setJobTypes] = useState<JobTypeOut[]>([])
  const [skills, setSkills] = useState<SkillOut[]>([])
  const [loadError, setLoadError] = useState<string | null>(null)

  const [projectId, setProjectId] = useState('')
  const [jobType, setJobType] = useState('')
  // 필요 기술은 백엔드 REQ_SKILL_JSON.SKILL_IDS가 배열을 지원하는데도 프론트엔드가
  // 단일 Select(`skill: string`)로 제한하고 있던 것을 다중 칩 선택으로 교체한다(§9-1).
  const [skillIds, setSkillIds] = useState<string[]>([])
  const [skillToAdd, setSkillToAdd] = useState('')
  const [role, setRole] = useState('')
  const [availDate, setAvailDate] = useState('')
  const [minAllocRt, setMinAllocRt] = useState('50')

  const [results, setResults] = useState<ResultRow[] | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  // "이 후보로 투입 요청"(§9-1) — 추천 결과를 실제 투입 등록으로 이어주기 위해 요청
  // 시점에 조회한 사원 목록을 보관해 등록 모달(`AssignmentFormModal`)에 재사용한다.
  const [employees, setEmployees] = useState<EmployeeOut[]>([])
  const [assignTarget, setAssignTarget] = useState<ResultRow | null>(null)

  useEffect(() => {
    Promise.all([
      apiGet<ProjectListResponse>('/api/v1/projects?limit=200'),
      apiGet<JobTypeOut[]>('/api/v1/job-types'),
      apiGet<SkillOut[]>('/api/v1/skills'),
    ])
      .then(([projectsRes, jobTypesRes, skillsRes]) => {
        setProjects(projectsRes.items)
        setJobTypes(jobTypesRes)
        setSkills(skillsRes)
      })
      .catch(() => setLoadError('요건 입력에 필요한 목록(프로젝트/직무/기술)을 불러오지 못했습니다.'))
  }, [])

  const projectOptions = useMemo(() => projects.map((p) => ({ label: p.PJT_NM, value: p.PJT_ID })), [projects])
  const jobTypeOptions = useMemo(
    () => [{ label: '전체', value: '' }, ...jobTypes.map((j) => ({ label: j.JIKMU_NM, value: j.JIKMU_ID }))],
    [jobTypes],
  )
  const skillNameById = useMemo(() => new Map(skills.map((s) => [s.SKILL_ID, s.SKILL_NM])), [skills])
  // 이미 선택된 기술은 추가 선택지에서 제외한다(사원 상세 화면의 "기술 추가" 모달과
  // 동일하게 중복 선택을 UI에서 방지).
  const skillOptions = useMemo(
    () =>
      skills.filter((s) => !skillIds.includes(s.SKILL_ID)).map((s) => ({ label: s.SKILL_NM, value: s.SKILL_ID })),
    [skills, skillIds],
  )

  function addSkill() {
    if (!skillToAdd || skillIds.includes(skillToAdd)) return
    setSkillIds((prev) => [...prev, skillToAdd])
    setSkillToAdd('')
  }

  function removeSkill(skillId: string) {
    setSkillIds((prev) => prev.filter((id) => id !== skillId))
  }

  async function handleSubmit() {
    setSubmitting(true)
    setSubmitError(null)
    try {
      const resourceRequest = await apiPost<ResourceRequestOut>('/api/v1/resource-requests', {
        PJT_ID: projectId,
        REQ_JIKMU_ID: jobType || null,
        REQ_ROLE_NM: role,
        REQ_SKILL_JSON: skillIds.length > 0 ? { SKILL_IDS: skillIds } : {},
        MIN_ALLOC_RT: Number(minAllocRt),
        REQ_AVAIL_DT: availDate,
      })

      const scored = await apiPost<RecommendationResultOut[]>('/api/v1/recommendations/score', {
        req_id: resourceRequest.REQ_ID,
      })

      // 결과에 등장하는 사원의 이름·직무·기술을 조인해 표시한다(다른 화면들과 동일한
      // 클라이언트 조인 패턴 — 별도 집계 API 없이 기존 조회 API를 재사용).
      const [employeesRes, employeeSkills] = await Promise.all([
        apiGet<EmployeeListResponse>('/api/v1/employees?limit=200'),
        apiGet<EmployeeSkillOut[]>('/api/v1/employee-skills'),
      ])
      setEmployees(employeesRes.items)
      const employeeById = new Map(employeesRes.items.map((e) => [e.EMPL_ID, e]))
      const jobTypeById = new Map(jobTypes.map((j) => [j.JIKMU_ID, j]))
      const skillNameById = new Map(skills.map((s) => [s.SKILL_ID, s.SKILL_NM]))
      const skillNamesByEmpId = new Map<string, string[]>()
      for (const es of employeeSkills) {
        const name = skillNameById.get(es.SKILL_ID)
        if (!name) continue
        const list = skillNamesByEmpId.get(es.EMPL_ID) ?? []
        list.push(name)
        skillNamesByEmpId.set(es.EMPL_ID, list)
      }

      setResults(
        scored.map((r) => {
          const employee = employeeById.get(r.EMPL_ID)
          return {
            ...r,
            empName: employee?.EMPL_NM ?? r.EMPL_ID,
            jobTypeName: employee?.JIKMU_ID ? (jobTypeById.get(employee.JIKMU_ID)?.JIKMU_NM ?? null) : null,
            skillNames: skillNamesByEmpId.get(r.EMPL_ID) ?? [],
          }
        }),
      )
    } catch (err) {
      setSubmitError(err instanceof ApiError ? err.message : '추천 실행에 실패했습니다. 잠시 후 다시 시도하세요.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <PageHeader
        title="리소스 추천"
        description="프로젝트 요건을 입력하면 적합도 점수 기반으로 최적 인력을 추천합니다."
      />

      {loadError && <p className="mb-4 text-sm text-destructive">{loadError}</p>}

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="size-4 text-primary" />
              요건 입력
            </CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            {submitError && <p className="text-sm text-destructive">{submitError}</p>}
            <div className="flex flex-col gap-1.5">
              <Label>프로젝트</Label>
              <Select value={projectId} onValueChange={setProjectId} options={projectOptions} placeholder="프로젝트 선택" />
            </div>
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
              <Label>필요 기술</Label>
              <div className="flex gap-2">
                <Select
                  value={skillToAdd}
                  onValueChange={setSkillToAdd}
                  options={skillOptions}
                  placeholder="기술 선택"
                  className="flex-1"
                />
                <Button type="button" variant="secondary" onClick={addSkill} disabled={!skillToAdd}>
                  추가
                </Button>
              </div>
              {skillIds.length > 0 && (
                <div className="mt-1.5 flex flex-wrap gap-1.5">
                  {skillIds.map((id) => (
                    <Badge key={id} variant="secondary" className="gap-1.5">
                      {skillNameById.get(id) ?? id}
                      <button
                        type="button"
                        onClick={() => removeSkill(id)}
                        aria-label="기술 제거"
                        className="rounded-full hover:text-destructive"
                      >
                        <X className="size-3" />
                      </button>
                    </Badge>
                  ))}
                </div>
              )}
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="req-avail-date">투입 시작 희망일</Label>
              <Input id="req-avail-date" type="date" value={availDate} onChange={(e) => setAvailDate(e.target.value)} />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="req-min-alloc">최소 투입 가능률(%)</Label>
              <Input
                id="req-min-alloc"
                type="number"
                min={0}
                max={100}
                value={minAllocRt}
                onChange={(e) => setMinAllocRt(e.target.value)}
              />
            </div>
            <Button
              className="mt-1"
              onClick={handleSubmit}
              disabled={submitting || !projectId || !role.trim() || !availDate}
            >
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
          {results === null ? (
            <Card>
              <CardContent className="py-12">
                <EmptyState
                  title="요건을 입력하고 조회하세요"
                  description="좌측 폼에서 역할·직무·기술을 선택한 뒤 추천 인력 조회를 실행하면 순위별 추천 결과가 표시됩니다."
                />
              </CardContent>
            </Card>
          ) : results.length === 0 ? (
            <Card>
              <CardContent className="py-12">
                <EmptyState title="추천 가능한 인력이 없습니다" description="조건을 조정해 다시 조회해 보세요." />
              </CardContent>
            </Card>
          ) : (
            results.map((rec, idx) => {
              const meta = RANK_META[idx] ?? RANK_META[2]
              const Icon = meta.icon
              return (
                <Card key={rec.RCMD_ID}>
                  <CardContent className="pt-6">
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <div className={`flex size-10 items-center justify-center rounded-full ${meta.cls}`}>
                          <Icon className="size-5" />
                        </div>
                        <div>
                          <p className="flex items-center gap-2 font-semibold">
                            {rec.empName}
                            <span className="text-xs font-normal text-muted-foreground">
                              {rec.jobTypeName ?? '-'}
                            </span>
                          </p>
                          <p className="text-xs text-muted-foreground">{rec.RCMD_RSN}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold tabular-nums text-primary">{rec.TOT_SCORE}</p>
                        <p className="text-xs text-muted-foreground">적합도 점수</p>
                      </div>
                    </div>

                    <div className="mt-4 flex flex-wrap items-center gap-2">
                      {rec.skillNames.length === 0 ? (
                        <span className="text-xs text-muted-foreground">보유 기술 없음</span>
                      ) : (
                        rec.skillNames.map((s) => (
                          <Badge key={s} variant="secondary">
                            {s}
                          </Badge>
                        ))
                      )}
                    </div>

                    {rec.SCORE_DTL_JSON && (
                      <div className="mt-5 grid grid-cols-2 gap-x-6 gap-y-3 sm:grid-cols-3">
                        {SCORE_LABELS.map((s) => {
                          const v = rec.SCORE_DTL_JSON![s.key]
                          return (
                            <div key={s.key}>
                              <div className="flex items-center justify-between text-xs">
                                <span className="text-muted-foreground">{s.label}</span>
                                <span className="font-semibold tabular-nums">
                                  {v}/{s.max}
                                </span>
                              </div>
                              <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-secondary">
                                <div
                                  className={`h-full rounded-full ${scoreColor(v / s.max)}`}
                                  style={{ width: `${(v / s.max) * 100}%` }}
                                />
                              </div>
                            </div>
                          )
                        })}
                      </div>
                    )}

                    <div className="mt-5 flex justify-end">
                      <Button size="sm" variant="secondary" onClick={() => setAssignTarget(rec)}>
                        <UserPlus className="size-4" />
                        이 후보로 투입 요청
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              )
            })
          )}
        </div>
      </div>

      {assignTarget && (
        <AssignmentFormModal
          open
          onOpenChange={(open) => {
            if (!open) setAssignTarget(null)
          }}
          onSaved={() => setAssignTarget(null)}
          employees={employees}
          fixedPjtId={projectId}
          fixedPjtName={projects.find((p) => p.PJT_ID === projectId)?.PJT_NM}
          presetEmplId={assignTarget.EMPL_ID}
          presetRoleNm={role}
          presetStartDate={availDate}
          presetAllocRt={minAllocRt}
        />
      )}
    </div>
  )
}
