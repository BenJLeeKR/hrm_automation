'use client'

import {
  Dialog,
  DialogBody,
  DialogFooter,
  DialogHeader,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

interface ModalFormProps {
  open: boolean
  onClose: () => void
  onSubmit: () => void
  title: string
  description?: string
  submitText?: string
  cancelText?: string
  submitDisabled?: boolean
  children: React.ReactNode
  className?: string
}

export function ModalForm({
  open,
  onClose,
  onSubmit,
  title,
  description,
  submitText = '저장',
  cancelText = '취소',
  submitDisabled = false,
  children,
  className,
}: ModalFormProps) {
  return (
    <Dialog open={open} onClose={onClose} className={className}>
      <DialogHeader title={title} description={description} onClose={onClose} />
      <form
        onSubmit={(e) => {
          e.preventDefault()
          onSubmit()
        }}
      >
        <DialogBody className="max-h-[70vh] overflow-y-auto scrollbar-thin">
          {children}
        </DialogBody>
        <DialogFooter>
          <Button type="button" variant="secondary" onClick={onClose}>
            {cancelText}
          </Button>
          <Button type="submit" disabled={submitDisabled}>
            {submitText}
          </Button>
        </DialogFooter>
      </form>
    </Dialog>
  )
}

interface FormFieldProps {
  label: string
  required?: boolean
  hint?: string
  children: React.ReactNode
}

export function FormField({ label, required, hint, children }: FormFieldProps) {
  return (
    <div className="mb-4 flex flex-col gap-1.5">
      <label className="text-xs font-medium text-foreground/80">
        {label}
        {required && <span className="ml-0.5 text-destructive">*</span>}
      </label>
      {children}
      {hint && <p className="text-xs text-muted-foreground">{hint}</p>}
    </div>
  )
}
