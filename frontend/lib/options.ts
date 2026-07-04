import type { SelectOption } from '@/components/ui/select'
import { departments, positions, jobTypes, skills } from './mock-data'

export const teamOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  ...departments.map((d) => ({ label: d.name, value: d.code })),
]

export const roleOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  { label: 'AA', value: 'AA' },
  { label: 'TA', value: 'TA' },
  { label: 'BA', value: 'BA' },
  { label: 'DBA', value: 'DBA' },
  { label: 'PM', value: 'PM' },
  { label: '컨설턴트', value: '컨설턴트' },
  { label: '사업관리', value: '사업관리' },
]

export const employeeStatusOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  { label: '재직', value: 'ACTIVE' },
  { label: '휴직', value: 'LEAVE' },
  { label: '퇴직', value: 'RETIRED' },
]

export const positionOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  ...positions.map((p) => ({ label: p.name, value: p.code })),
]

export const jobTypeOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  ...jobTypes.map((j) => ({ label: j.name, value: j.code })),
]

export const skillOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  ...skills
    .filter((s) => s.useYn)
    .map((s) => ({ label: s.name, value: s.name })),
]

export const useYnOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  { label: '사용중', value: 'true' },
  { label: '미사용', value: 'false' },
]

export const projectStatusOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  { label: '계획', value: 'PLANNED' },
  { label: '수행중', value: 'RUNNING' },
  { label: '보류', value: 'HOLD' },
  { label: '종료', value: 'CLOSED' },
]

export const assignmentTypeOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  { label: '수행중', value: 'RUNNING' },
  { label: '투입준비중', value: 'COMMITTED' },
  { label: '제안중', value: 'PROPOSED' },
]

export const assignmentStatusOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  { label: '계획', value: 'PLANNED' },
  { label: '진행', value: 'ACTIVE' },
  { label: '완료', value: 'DONE' },
  { label: '취소', value: 'CANCELED' },
]

export const proficiencyOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  { label: 'Lv.1 이상', value: '1' },
  { label: 'Lv.2 이상', value: '2' },
  { label: 'Lv.3 이상', value: '3' },
  { label: 'Lv.4 이상', value: '4' },
  { label: 'Lv.5', value: '5' },
]

export const userRoleOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  { label: '시스템 관리자', value: 'ADMIN' },
  { label: 'HR 관리자', value: 'HR_MGR' },
  { label: '프로젝트 관리자', value: 'PM' },
  { label: '팀장', value: 'TEAM_LEAD' },
  { label: '임원', value: 'EXEC' },
  { label: '조회자', value: 'VIEWER' },
]

export const userStatusOptions: SelectOption[] = [
  { label: '전체', value: 'ALL' },
  { label: '활성', value: 'ACTIVE' },
  { label: '비활성', value: 'INACTIVE' },
]
