'use client'

import { AlertTriangle } from 'lucide-react'
import {
  Dialog,
  DialogBody,
  DialogFooter,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

interface ConfirmDialogProps {
  open: boolean
  onClose: () => void
  onConfirm: () => void
  title?: string
  description?: string
  confirmText?: string
  cancelText?: string
  destructive?: boolean
}

export function ConfirmDialog({
  open,
  onClose,
  onConfirm,
  title = '정말 진행하시겠습니까?',
  description,
  confirmText = '확인',
  cancelText = '취소',
  destructive = false,
}: ConfirmDialogProps) {
  return (
    <Dialog open={open} onClose={onClose} className="max-w-md">
      <DialogBody className="flex gap-4 pt-6">
        <div className="flex size-10 shrink-0 items-center justify-center rounded-full bg-[#fdf0dc]">
          <AlertTriangle className="size-5 text-[#b46708]" />
        </div>
        <div>
          <h2 className="text-base font-semibold">{title}</h2>
          {description && (
            <p className="mt-1 text-sm text-muted-foreground">{description}</p>
          )}
        </div>
      </DialogBody>
      <DialogFooter>
        <Button variant="secondary" onClick={onClose}>
          {cancelText}
        </Button>
        <Button
          variant={destructive ? 'destructive' : 'default'}
          onClick={() => {
            onConfirm()
            onClose()
          }}
        >
          {confirmText}
        </Button>
      </DialogFooter>
    </Dialog>
  )
}
