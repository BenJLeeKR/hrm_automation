'use client'

import { useState } from 'react'
import { ModalForm } from '@/components/common/modal-form'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Select } from '@/components/ui/select'
import { projectStatusOptions } from '@/lib/options'

interface ProjectFormModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const statusOptions = projectStatusOptions.filter((o) => o.value !== 'ALL')

export function ProjectFormModal({ open, onOpenChange }: ProjectFormModalProps) {
  const [name, setName] = useState('')
  const [client, setClient] = useState('')
  const [status, setStatus] = useState('PLANNED')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [desc, setDesc] = useState('')

  function close() {
    onOpenChange(false)
  }

  function handleSubmit() {
    // 프로토타입: 실제 저장 대신 폼 초기화 후 닫기
    setName('')
    setClient('')
    setStatus('PLANNED')
    setStartDate('')
    setEndDate('')
    setDesc('')
    close()
  }

  return (
    <ModalForm
      open={open}
      onClose={close}
      title="프로젝트 등록"
      description="신규 프로젝트 기본 정보를 입력합니다."
      submitText="등록"
      onSubmit={handleSubmit}
      submitDisabled={!name || !client}
    >
      <div className="flex flex-col gap-4">
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="pj-name">프로젝트명</Label>
          <Input
            id="pj-name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="예: 차세대 여신 시스템 구축"
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="pj-client">고객사</Label>
            <Input
              id="pj-client"
              value={client}
              onChange={(e) => setClient(e.target.value)}
              placeholder="예: K은행"
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label>상태</Label>
            <Select value={status} onValueChange={setStatus} options={statusOptions} />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="pj-start">시작일</Label>
            <Input
              id="pj-start"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="pj-end">종료일</Label>
            <Input
              id="pj-end"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
        </div>
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="pj-desc">개요</Label>
          <Textarea
            id="pj-desc"
            value={desc}
            onChange={(e) => setDesc(e.target.value)}
            placeholder="프로젝트 범위와 목표를 입력하세요."
            rows={3}
          />
        </div>
      </div>
    </ModalForm>
  )
}
