'use client'

import { useEffect, useMemo, useState } from 'react'
import { Plus, Pencil, Power } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { FilterBar, FilterField } from '@/components/common/filter-bar'
import { SearchInput } from '@/components/common/search-input'
import { DataTable, type Column } from '@/components/common/data-table'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { apiGet, apiPatch, apiPost, ApiError } from '@/lib/api'
import { useYnOptions } from '@/lib/options'

// 백엔드 직무 유형 마스터 API(로드맵 §8 "직무 유형 관리 화면 구현", SCR-006) 응답 타입 —
// 필드명은 backend/app/schemas/hr_jikmu_mst.py와 동일하게 유지한다.
interface JobTypeOut {
  JIKMU_ID: string
  JIKMU_CD: string
  JIKMU_NM: string
  JIKMU_GRP_CD: string | null
  JIKMU_DESC: string | null
  SORT_ORD: number
  USE_YN: boolean
}

// 설계서(SCR-006 등록/수정 모달)가 명시한 3개 그룹 — HR_JIKMU_MST.JIKMU_GRP_CD는
// DB CHECK 제약이 없는 자유 문자열이지만, 등록 화면은 설계서 기준으로 이 3종만 제공한다.
const groupFilterOptions = [
  { label: '전체', value: 'ALL' },
  { label: 'TECHNICAL', value: 'TECHNICAL' },
  { label: 'MANAGEMENT', value: 'MANAGEMENT' },
  { label: 'ANALYSIS', value: 'ANALYSIS' },
]
const groupSelectOptions = groupFilterOptions.filter((o) => o.value !== 'ALL')
const useYnSelectOptions = useYnOptions.filter((o) => o.value !== 'ALL')

async function loadJobTypes(): Promise<JobTypeOut[]> {
  // 백엔드 GET /job-types는 use_yn 생략 시 사용중(true)인 직무만 반환하므로,
  // "전체"(사용중+미사용) 목록을 보여주기 위해 두 상태를 각각 조회해 병합한다.
  const [active, inactive] = await Promise.all([
    apiGet<JobTypeOut[]>('/api/v1/job-types?use_yn=true'),
    apiGet<JobTypeOut[]>('/api/v1/job-types?use_yn=false'),
  ])
  return [...active, ...inactive]
}

export default function JobTypesPage() {
  const [keyword, setKeyword] = useState('')
  const [group, setGroup] = useState('ALL')
  const [useYn, setUseYn] = useState('ALL')
  const [jobTypes, setJobTypes] = useState<JobTypeOut[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState<JobTypeOut | null>(null)
  const [openForm, setOpenForm] = useState(false)

  function reload() {
    setLoading(true)
    loadJobTypes()
      .then((data) => {
        setJobTypes(data)
        setError(null)
      })
      .catch(() => setError('직무 유형 목록을 불러오지 못했습니다. 잠시 후 다시 시도하세요.'))
      .finally(() => setLoading(false))
  }

  useEffect(reload, [])

  const filtered = useMemo(
    () =>
      jobTypes.filter((j) => {
        if (keyword && !j.JIKMU_NM.toLowerCase().includes(keyword.toLowerCase())) return false
        if (group !== 'ALL' && j.JIKMU_GRP_CD !== group) return false
        if (useYn !== 'ALL' && String(j.USE_YN) !== useYn) return false
        return true
      }),
    [jobTypes, keyword, group, useYn],
  )

  function openEdit(jobType: JobTypeOut) {
    setEditing(jobType)
    setOpenForm(true)
  }
  function openCreate() {
    setEditing(null)
    setOpenForm(true)
  }

  async function toggleUseYn(jobType: JobTypeOut) {
    try {
      await apiPatch(`/api/v1/job-types/${jobType.JIKMU_ID}`, { USE_YN: !jobType.USE_YN })
      reload()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : '사용 여부 변경에 실패했습니다.')
    }
  }

  const columns: Column<JobTypeOut>[] = [
    { key: 'code', header: '코드', className: 'w-32', render: (j) => <span className="text-sm tabular-nums text-muted-foreground">{j.JIKMU_CD}</span> },
    { key: 'name', header: '직무명', render: (j) => <span className="font-medium">{j.JIKMU_NM}</span> },
    { key: 'group', header: '그룹', render: (j) => (j.JIKMU_GRP_CD ? <Badge variant="soft">{j.JIKMU_GRP_CD}</Badge> : <span className="text-sm text-muted-foreground">-</span>) },
    { key: 'desc', header: '설명', className: 'max-w-xs', render: (j) => <span className="text-sm text-muted-foreground">{j.JIKMU_DESC ?? '-'}</span> },
    { key: 'useYn', header: '사용 여부', render: (j) => <Badge variant={j.USE_YN ? 'success' : 'muted'}>{j.USE_YN ? '사용중' : '미사용'}</Badge> },
    {
      key: 'actions',
      header: '',
      className: 'w-24 text-right',
      render: (j) => (
        <div className="flex justify-end gap-1">
          <Button size="icon-sm" variant="ghost" onClick={(e) => { e.stopPropagation(); openEdit(j) }} aria-label="수정">
            <Pencil className="size-4" />
          </Button>
          <Button size="icon-sm" variant="ghost" onClick={(e) => { e.stopPropagation(); toggleUseYn(j) }} aria-label={j.USE_YN ? '비활성화' : '활성화'}>
            <Power className="size-4" />
          </Button>
        </div>
      ),
    },
  ]

  return (
    <div>
      <PageHeader
        title="직무 유형"
        description="프로젝트 투입 시 사용되는 표준 직무(Role) 유형을 관리합니다."
      >
        <Button onClick={openCreate}>
          <Plus className="size-4" />직무 등록
        </Button>
      </PageHeader>

      {error && <p className="mb-4 text-sm text-destructive">{error}</p>}

      <FilterBar>
        <FilterField label="검색" className="min-w-56 flex-1">
          <SearchInput value={keyword} onChange={setKeyword} placeholder="직무명 검색" />
        </FilterField>
        <FilterField label="그룹">
          <Select value={group} onValueChange={setGroup} options={groupFilterOptions} />
        </FilterField>
        <FilterField label="사용 여부">
          <Select value={useYn} onValueChange={setUseYn} options={useYnOptions} />
        </FilterField>
      </FilterBar>

      <DataTable
        columns={columns}
        data={filtered}
        rowKey={(j) => j.JIKMU_ID}
        emptyTitle={loading ? '불러오는 중입니다...' : '조건에 맞는 직무가 없습니다'}
        footer={<span>전체 {jobTypes.length}개 중 {filtered.length}개 표시</span>}
      />

      <JobTypeFormModal
        key={editing?.JIKMU_ID ?? 'new'}
        open={openForm}
        onClose={() => setOpenForm(false)}
        jobType={editing}
        onSaved={reload}
      />
    </div>
  )
}

function JobTypeFormModal({
  open,
  onClose,
  jobType,
  onSaved,
}: {
  open: boolean
  onClose: () => void
  jobType: JobTypeOut | null
  onSaved: () => void
}) {
  const [code, setCode] = useState(jobType?.JIKMU_CD ?? '')
  const [name, setName] = useState(jobType?.JIKMU_NM ?? '')
  const [group, setGroup] = useState(jobType?.JIKMU_GRP_CD ?? groupSelectOptions[0].value)
  const [desc, setDesc] = useState(jobType?.JIKMU_DESC ?? '')
  const [sortOrd, setSortOrd] = useState(String(jobType?.SORT_ORD ?? 0))
  const [useYn, setUseYn] = useState(String(jobType?.USE_YN ?? true))
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  async function handleSubmit() {
    setSubmitting(true)
    setFormError(null)
    try {
      const payload = {
        JIKMU_NM: name,
        JIKMU_GRP_CD: group,
        JIKMU_DESC: desc || null,
        SORT_ORD: Number(sortOrd) || 0,
        USE_YN: useYn === 'true',
      }
      if (jobType) {
        await apiPatch(`/api/v1/job-types/${jobType.JIKMU_ID}`, payload)
      } else {
        // JIKMU_CD는 등록 시에만 입력받는다 — 설계서(SCR-006)상 직무 코드는 수정 대상이 아님
        await apiPost('/api/v1/job-types', { ...payload, JIKMU_CD: code.toUpperCase() })
      }
      onSaved()
      onClose()
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : '저장에 실패했습니다. 잠시 후 다시 시도하세요.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <ModalForm
      open={open}
      onClose={onClose}
      onSubmit={handleSubmit}
      title={jobType ? '직무 유형 수정' : '직무 유형 등록'}
      submitText={jobType ? '수정 저장' : '등록'}
      submitDisabled={submitting || !name.trim() || (!jobType && !code.trim())}
    >
      {formError && <p className="mb-3 text-sm text-destructive">{formError}</p>}
      {!jobType && (
        <FormField label="직무 코드" required>
          <Input value={code} onChange={(e) => setCode(e.target.value)} placeholder="예: TECH_WRITER (영문 대문자, 최대 50자)" />
        </FormField>
      )}
      <FormField label="직무명" required>
        <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="예: 테크니컬 라이터" />
      </FormField>
      <FormField label="그룹" required>
        <Select value={group} onValueChange={setGroup} options={groupSelectOptions} />
      </FormField>
      <FormField label="설명">
        <Textarea value={desc} onChange={(e) => setDesc(e.target.value)} rows={3} placeholder="직무에 대한 설명을 입력하세요." />
      </FormField>
      <FormField label="정렬 순서">
        <Input type="number" value={sortOrd} onChange={(e) => setSortOrd(e.target.value)} />
      </FormField>
      <FormField label="사용 여부" required>
        <Select value={useYn} onValueChange={setUseYn} options={useYnSelectOptions} />
      </FormField>
    </ModalForm>
  )
}
