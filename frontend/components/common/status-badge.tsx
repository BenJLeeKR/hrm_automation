import { Badge } from '@/components/ui/badge'
import {
  assignmentTypeLabel,
  employeeStatusLabel,
  employeeStatusVariant,
  projectStatusLabel,
  projectStatusVariant,
  roleLabel,
} from '@/lib/labels'
import type {
  AssignmentType,
  EmployeeStatus,
  ProjectStatus,
  RoleCode,
} from '@/lib/types'

export function ProjectStatusBadge({ status }: { status: ProjectStatus }) {
  return (
    <Badge variant={projectStatusVariant[status]}>
      {projectStatusLabel[status]}
    </Badge>
  )
}

export function EmployeeStatusBadge({ status }: { status: EmployeeStatus }) {
  return (
    <Badge variant={employeeStatusVariant[status]}>
      {employeeStatusLabel[status]}
    </Badge>
  )
}

const assignmentTypeVariant: Record<
  AssignmentType,
  'default' | 'warning' | 'info'
> = {
  RUNNING: 'default',
  COMMITTED: 'warning',
  PROPOSED: 'info',
}

export function AssignmentTypeBadge({ type }: { type: AssignmentType }) {
  return (
    <Badge variant={assignmentTypeVariant[type]}>
      {assignmentTypeLabel[type]}
    </Badge>
  )
}

const roleVariant: Record<RoleCode, 'default' | 'soft' | 'secondary' | 'muted'> = {
  ADMIN: 'default',
  HR_MGR: 'soft',
  PM: 'soft',
  TEAM_LEAD: 'secondary',
  EXEC: 'secondary',
  VIEWER: 'muted',
}

export function RoleBadge({ role }: { role: RoleCode }) {
  return <Badge variant={roleVariant[role]}>{roleLabel[role]}</Badge>
}
