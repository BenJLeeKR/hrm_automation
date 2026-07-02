'use client'

import { useMemo, useState } from 'react'
import { Plus, Pencil, Briefcase } from 'lucide-react'
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
import { jobTypes } from '@/lib/mock-data'
import { useYnOptions } from '@/lib/options'
import type { JobType } from '@/lib/types'

const groupLabel: Record<JobType['group'], string> = {
  TECHNICAL: '기술직군',
  MANAGEMENT: '관리직군',
  ANALYSIS: '분석직군',
}
const groupVariant: Record<JobType['group'], 'info' | 'soft' | 'warning'> = {
  TECHNICAL: 'info',
  MANAGEMENT: 'soft',
  ANALYSIS: 'warning',
}

const groupFilterOptions = [
  { label: '전체', value: 'ALL' },
  { label: '기술직군', value: 'TECHNICAL' },
  { label: '관리직군', value: 'MANAGEMENT' },
  { label: '분석직군', value: 'ANALYSIS' },
]

export default function JobTypesPage() {
  const [keyword, setKeyword] = useState('')
  const [group, setGroup] = useState('ALL')
  const [useYn, setUseYn] = useState('ALL')
  const [editing, setEditing] = useState<JobType | null>(null)
  const [openForm, setOpenForm] = useState(false)

  const filtered = useMemo(
    () =>
      jobTypes.filter((j) => {
        if (keyword && !j.name.toLowerCase().includes(keyword.toLowerCase())) return false
        if (group !== 'ALL' && j.group !== group) return false
        if (useYn !== 'ALL' && String(j.useYn) !== useYn) return false
        return true
      }),
    [keyword, group, useYn],
  )

  const columns: Column<JobType>[] = [
    { key: 'code', header: '코드', className: 'w-32', render: (j) => <span className="text-sm tabular-nums text-muted-foreground">{j.code}</span> },
    { key: 'name', header: '직무명', render: (j) => <span className="font-medium">{j.name}</span> },
    { key: 'group', header: '직군', render: (j) => <Badge variant={groupVariant[j.group]}>{groupLabel[j.group]}</Badge> },
    { key: 'desc', header: '설명', className: 'max-w-xs', render: (j) => <span className="text-sm text-muted-foreground">{j.desc}</span> },
    { key: 'useYn', header: '사용 여부', render: (j) => <Badge variant={j.useYn ? 'success' : 'muted'}>{j.useYn ? '사용중' : '미사용'}</Badge> },
    {
      key: 'actions',
      header: '',
      className: 'w-16 text-right',
      render: (j) => (
        <Button
          size="icon-sm"
          variant="ghost"
          onClick={(e) => {
            e.stopPropagation()
            setEditing(j)
            setOpenForm(true)
          }}
          aria-label="수정"
        >
          <Pencil className="size-4" />
        </Button>
      ),
    },
  ]

  return (
    <div>
      <PageHeader
        title="직무 유형"
        description="프로젝트 투입 시 사용되는 표준 직무(Role) 유형을 관리합니다."
      >
        <Button
          onClick={() => {
            setEditing(null)
            setOpenForm(true)
          }}
        >
          <Plus className="size-4" />직무 등록
        </Button>
      </PageHeader>

      <FilterBar>
        <FilterField label="검색" className="min-w-56 flex-1">
          <SearchInput value={keyword} onChange={setKeyword} placeholder="직무명 검색" />
        </FilterField>
        <FilterField label="직군">
          <Select value={group} onValueChange={setGroup} options={groupFilterOptions} />
        </FilterField>
        <FilterField label="사용 여부">
          <Select value={useYn} onValueChange={setUseYn} options={useYnOptions} />
        </FilterField>
      </FilterBar>

      <DataTable
        columns={columns}
        data={filtered}
        rowKey={(j) => String(j.code)}
        emptyTitle="조건에 맞는 직무가 없습니다"
        footer={<span>전체 {jobTypes.length}개 중 {filtered.length}개 표시</span>}
      />

      <JobTypeFormModal
        key={editing?.code ?? 'new'}
        open={openForm}
        onClose={() => setOpenForm(false)}
        jobType={editing}
      />
    </div>
  )
}

function JobTypeFormModal({
  open,
  onClose,
  jobType,
}: {
  open: boolean
  onClose: () => void
  jobType: JobType | null
}) {
  const [name, setName] = useState(jobType?.name ?? '')
  const [group, setGroup] = useState<JobType['group']>(jobType?.group ?? 'TECHNICAL')
  const [desc, setDesc] = useState(jobType?.desc ?? '')

  return (
    <ModalForm
      open={open}
      onClose={onClose}
      onSubmit={onClose}
      title={jobType ? '직무 유형 수정' : '직무 유형 등록'}
      submitText={jobType ? '수정 저장' : '등록'}
    >
      <FormField label="직무명" required>
        <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="예: 테크니컬 라이터" />
      </FormField>
      <FormField label="직군" required>
        <Select
          value={group}
          onValueChange={(v) => setGroup(v as JobType['group'])}
          options={groupFilterOptions.filter((o) => o.value !== 'ALL')}
        />
      </FormField>
      <FormField label="설명">
        <Textarea value={desc} onChange={(e) => setDesc(e.target.value)} rows={3} placeholder="직무에 대한 설명을 입력하세요." />
      </FormField>
    </ModalForm>
  )
}
