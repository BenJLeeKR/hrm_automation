'use client'

import { useMemo, useState } from 'react'
import { Plus, Wrench, Users2, Pencil } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { FilterBar, FilterField } from '@/components/common/filter-bar'
import { SearchInput } from '@/components/common/search-input'
import { DataTable, type Column } from '@/components/common/data-table'
import { Select } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { StatCard } from '@/components/common/stat-card'
import { ModalForm, FormField } from '@/components/common/modal-form'
import { Input } from '@/components/ui/input'
import { skills } from '@/lib/mock-data'
import { skillGroupOptions, useYnOptions } from '@/lib/options'
import type { Skill } from '@/lib/types'

const groupSelectOptions = skillGroupOptions.filter((o) => o.value !== 'ALL')

export default function SkillsPage() {
  const [keyword, setKeyword] = useState('')
  const [group, setGroup] = useState('ALL')
  const [useYn, setUseYn] = useState('ALL')
  const [editing, setEditing] = useState<Skill | null>(null)
  const [openForm, setOpenForm] = useState(false)

  const filtered = useMemo(
    () =>
      skills.filter((s) => {
        if (keyword && !s.name.toLowerCase().includes(keyword.toLowerCase())) return false
        if (group !== 'ALL' && s.group !== group) return false
        if (useYn !== 'ALL' && String(s.useYn) !== useYn) return false
        return true
      }),
    [keyword, group, useYn],
  )

  const activeCount = skills.filter((s) => s.useYn).length
  const totalUsers = skills.reduce((sum, s) => sum + s.userCount, 0)

  function openEdit(skill: Skill) {
    setEditing(skill)
    setOpenForm(true)
  }
  function openCreate() {
    setEditing(null)
    setOpenForm(true)
  }

  const columns: Column<Skill>[] = [
    { key: 'id', header: '코드', className: 'w-24', render: (s) => <span className="text-sm tabular-nums text-muted-foreground">{s.id}</span> },
    { key: 'name', header: '기술명', render: (s) => <span className="font-medium">{s.name}</span> },
    { key: 'group', header: '기술 그룹', render: (s) => <Badge variant="secondary">{s.group}</Badge> },
    {
      key: 'userCount',
      header: '보유 인원',
      render: (s) => (
        <span className="inline-flex items-center gap-1 text-sm tabular-nums">
          <Users2 className="size-3.5 text-muted-foreground" />
          {s.userCount}명
        </span>
      ),
    },
    {
      key: 'useYn',
      header: '사용 여부',
      render: (s) => (
        <Badge variant={s.useYn ? 'success' : 'muted'}>{s.useYn ? '사용중' : '미사용'}</Badge>
      ),
    },
    {
      key: 'actions',
      header: '',
      className: 'w-16 text-right',
      render: (s) => (
        <Button
          size="icon-sm"
          variant="ghost"
          onClick={(e) => {
            e.stopPropagation()
            openEdit(s)
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
        title="기술 관리"
        description="조직에서 관리하는 표준 기술 스택을 등록하고 유지보수합니다."
      >
        <Button onClick={openCreate}>
          <Plus className="size-4" />기술 등록
        </Button>
      </PageHeader>

      <div className="mb-4 grid grid-cols-2 gap-4 lg:grid-cols-3">
        <StatCard label="전체 기술" value={String(skills.length)} unit="개" icon={Wrench} tone="primary" />
        <StatCard label="사용중 기술" value={String(activeCount)} unit="개" icon={Wrench} tone="success" />
        <StatCard label="누적 보유 인원" value={String(totalUsers)} unit="명" icon={Users2} tone="info" />
      </div>

      <FilterBar>
        <FilterField label="검색" className="min-w-56 flex-1">
          <SearchInput value={keyword} onChange={setKeyword} placeholder="기술명 검색" />
        </FilterField>
        <FilterField label="기술 그룹">
          <Select value={group} onValueChange={setGroup} options={skillGroupOptions} />
        </FilterField>
        <FilterField label="사용 여부">
          <Select value={useYn} onValueChange={setUseYn} options={useYnOptions} />
        </FilterField>
      </FilterBar>

      <DataTable
        columns={columns}
        data={filtered}
        rowKey={(s) => s.id}
        emptyTitle="조건에 맞는 기술이 없습니다"
        footer={<span>전체 {skills.length}개 중 {filtered.length}개 표시</span>}
      />

      <SkillFormModal
        key={editing?.id ?? 'new'}
        open={openForm}
        onClose={() => setOpenForm(false)}
        skill={editing}
      />
    </div>
  )
}

function SkillFormModal({
  open,
  onClose,
  skill,
}: {
  open: boolean
  onClose: () => void
  skill: Skill | null
}) {
  const [name, setName] = useState(skill?.name ?? '')
  const [group, setGroup] = useState(skill?.group ?? 'BACKEND')

  return (
    <ModalForm
      open={open}
      onClose={onClose}
      onSubmit={onClose}
      title={skill ? '기술 수정' : '기술 등록'}
      submitText={skill ? '수정 저장' : '등록'}
    >
      <FormField label="기술명" required>
        <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="예: Kotlin" />
      </FormField>
      <FormField label="기술 그룹" required>
        <Select value={group} onValueChange={(v) => setGroup(v as Skill['group'])} options={groupSelectOptions} />
      </FormField>
    </ModalForm>
  )
}
