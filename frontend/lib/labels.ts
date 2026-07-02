// 코드값 → 한국어 표시명 매핑 및 뱃지 스타일 헬퍼

import type {
  AssignmentStatus,
  AssignmentType,
  AvailabilityKind,
  EmployeeStatus,
  ProjectStatus,
  RoleCode,
  TeamCode,
  UserStatus,
} from './types'

export const teamLabel: Record<TeamCode, string> = {
  DELIVERY: '딜리버리',
  SALES_PARTNER: '세일즈파트너',
  SALES: '영업',
}

export const employeeStatusLabel: Record<EmployeeStatus, string> = {
  ACTIVE: '재직',
  LEAVE: '휴직',
  RETIRED: '퇴직',
}

export const projectStatusLabel: Record<ProjectStatus, string> = {
  PLANNED: '계획',
  RUNNING: '수행중',
  HOLD: '보류',
  CLOSED: '종료',
}

export const assignmentTypeLabel: Record<AssignmentType, string> = {
  RUNNING: '수행중',
  COMMITTED: '투입준비중',
  PROPOSED: '제안중',
}

export const assignmentStatusLabel: Record<AssignmentStatus, string> = {
  PLANNED: '계획',
  ACTIVE: '진행',
  DONE: '완료',
  CANCELED: '취소',
}

export const availabilityKindLabel: Record<AvailabilityKind, string> = {
  IMMEDIATE: '즉시',
  PARTIAL: '부분',
  TERM: '기간',
}

export const roleLabel: Record<RoleCode, string> = {
  ADMIN: '시스템 관리자',
  HR_MGR: 'HR 관리자',
  PM: '프로젝트 관리자',
  TEAM_LEAD: '팀장',
  EXEC: '임원',
  VIEWER: '조회자',
}

export const userStatusLabel: Record<UserStatus, string> = {
  ACTIVE: '활성',
  INACTIVE: '비활성',
}

// 투입률 → 라벨/뱃지 변형
export function allocationBadge(allocation: number): {
  label: string
  variant: 'success' | 'warning' | 'default' | 'danger'
} {
  if (allocation <= 0) return { label: '즉시 가동', variant: 'success' }
  if (allocation < 100) return { label: '부분 가동', variant: 'warning' }
  if (allocation === 100) return { label: '풀 투입', variant: 'default' }
  return { label: '초과 투입', variant: 'danger' }
}

export const projectStatusVariant: Record<
  ProjectStatus,
  'success' | 'warning' | 'muted' | 'info'
> = {
  RUNNING: 'success',
  PLANNED: 'info',
  HOLD: 'warning',
  CLOSED: 'muted',
}

export const employeeStatusVariant: Record<
  EmployeeStatus,
  'success' | 'warning' | 'muted'
> = {
  ACTIVE: 'success',
  LEAVE: 'warning',
  RETIRED: 'muted',
}
