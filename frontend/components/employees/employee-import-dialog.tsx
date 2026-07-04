'use client'

import { useRef, useState } from 'react'
import { Upload } from 'lucide-react'
import { Dialog, DialogHeader, DialogBody, DialogFooter } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { apiUploadFile, ApiError } from '@/lib/api'

// SCR-003 "Excel 가져오기" 모달 — 백엔드 POST /api/v1/employees/import는 전체
// 검증 실패(422) 시 개별 행 오류를 한꺼번에 내려주는 all-or-nothing 방식이므로,
// 성공/실패 여부와 함께 행별 오류 목록을 그대로 보여준다.
interface ImportErrorItem {
  row: number
  column: string
  value: string | null
  reason: string
}
interface ImportErrorDetail {
  total_rows: number
  error_count: number
  errors: ImportErrorItem[]
}
interface ImportResult {
  total_rows: number
  created_count: number
  updated_count: number
}

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function EmployeeImportDialog({ open, onOpenChange }: Props) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [errorDetail, setErrorDetail] = useState<ImportErrorDetail | null>(null)
  const [result, setResult] = useState<ImportResult | null>(null)

  function reset() {
    setFile(null)
    setErrorMessage(null)
    setErrorDetail(null)
    setResult(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  function handleClose() {
    reset()
    onOpenChange(false)
  }

  async function handleSubmit() {
    if (!file) return
    setSubmitting(true)
    setErrorMessage(null)
    setErrorDetail(null)
    setResult(null)
    try {
      const res = await apiUploadFile<ImportResult>('/api/v1/employees/import', file)
      setResult(res)
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMessage(err.message)
        if (err.detail && typeof err.detail === 'object' && 'errors' in (err.detail as object)) {
          setErrorDetail(err.detail as ImportErrorDetail)
        }
      } else {
        setErrorMessage('Excel 가져오기에 실패했습니다.')
      }
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Dialog open={open} onClose={handleClose} className="max-w-xl">
      <DialogHeader
        title="Excel 가져오기"
        description="인력마스터 시트 형식의 Excel 파일을 업로드해 사원 정보를 일괄 등록/수정합니다."
        onClose={handleClose}
      />
      <DialogBody className="flex flex-col gap-4">
        <label className="flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border border-dashed border-border bg-muted/30 px-4 py-8 text-center text-sm text-muted-foreground transition-colors hover:bg-muted/50">
          <Upload className="size-5" />
          {file ? file.name : '.xlsx 파일을 선택하세요'}
          <input
            ref={fileInputRef}
            type="file"
            accept=".xlsx"
            className="hidden"
            onChange={(e) => {
              setFile(e.target.files?.[0] ?? null)
              setErrorMessage(null)
              setErrorDetail(null)
              setResult(null)
            }}
          />
        </label>

        {result && (
          <p className="text-sm text-success">
            전체 {result.total_rows}행 중 신규 {result.created_count}건, 수정 {result.updated_count}건을
            반영했습니다.
          </p>
        )}

        {errorMessage && <p className="text-sm text-destructive">{errorMessage}</p>}

        {errorDetail && errorDetail.errors.length > 0 && (
          <div className="max-h-64 overflow-y-auto scrollbar-thin rounded-lg border border-border">
            <table className="w-full text-xs">
              <thead className="bg-muted/60">
                <tr>
                  {['행', '컬럼', '값', '사유'].map((h) => (
                    <th key={h} className="px-2.5 py-2 text-left font-semibold text-muted-foreground">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {errorDetail.errors.map((e, i) => (
                  <tr key={i} className="border-t border-border">
                    <td className="px-2.5 py-1.5 tabular-nums">{e.row}</td>
                    <td className="px-2.5 py-1.5">{e.column}</td>
                    <td className="px-2.5 py-1.5 text-muted-foreground">{e.value ?? '-'}</td>
                    <td className="px-2.5 py-1.5">{e.reason}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </DialogBody>
      <DialogFooter>
        <Button variant="outline" onClick={handleClose}>
          닫기
        </Button>
        <Button onClick={handleSubmit} disabled={!file || submitting}>
          {submitting ? '업로드 중...' : '가져오기'}
        </Button>
      </DialogFooter>
    </Dialog>
  )
}
