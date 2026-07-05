// HRM 자동화 시스템 — 도메인 타입 정의
// DB 컬럼/코드값은 영문, 화면 표시명은 한국어로 매핑한다.

export type EmployeeStatus = 'ACTIVE' | 'LEAVE' | 'RETIRED'
export type AssignmentType = 'RUNNING' | 'COMMITTED' | 'PROPOSED'
export type AssignmentStatus = 'PLANNED' | 'ACTIVE' | 'DONE' | 'CANCELED'
export type ProjectStatus = 'PLANNED' | 'RUNNING' | 'CLOSED' | 'HOLD'
export type AvailabilityKind = 'IMMEDIATE' | 'PARTIAL' | 'TERM'
// EMPLOYEE(일반 사원)는 사원-계정 연동 설계(2026-07-06, §8 큐 1번)로 7번째 역할로
// 추가되었다 — 이 타입과 roleLabel/roleVariant(components/common/status-badge.tsx)를
// 함께 갱신해야 화면에 배지가 정상 표시된다.
export type RoleCode = 'ADMIN' | 'HR_MGR' | 'PM' | 'TEAM_LEAD' | 'EXEC' | 'EMPLOYEE' | 'VIEWER'
export type UserStatus = 'ACTIVE' | 'INACTIVE'

export type TeamCode = 'DELIVERY' | 'SALES_PARTNER' | 'SALES'

export type JikmuCode =
  | 'ARCHITECT'
  | 'TECH_LEAD'
  | 'BA'
  | 'DBA'
  | 'PM'
  | 'CONSULTANT'
  | 'PMO'
  | 'DEVELOPER'
  | 'QA'
  | 'DEVOPS'
  | 'DESIGNER'

export type SkillGroup =
  | 'BACKEND'
  | 'FRONTEND'
  | 'DB'
  | 'CLOUD'
  | 'DEVOPS'
  | 'DESIGN'
  | 'BUSINESS'

export interface Department {
  code: TeamCode
  name: string
}

export interface Position {
  code: string
  name: string
  order: number
}

export interface JobType {
  code: JikmuCode | string
  name: string
  group: 'TECHNICAL' | 'MANAGEMENT' | 'ANALYSIS'
  desc: string
  useYn: boolean
}

export interface Skill {
  id: string
  group: SkillGroup
  name: string
  userCount: number
  useYn: boolean
}

export interface EmployeeSkill {
  skillName: string
  group: SkillGroup
  level: number // 1~5
  years: number
  lastUsed: string
}

export interface EmployeeAssignment {
  projectName: string
  role: string
  allocation: number
  startDate: string
  endDate: string
  status: AssignmentStatus
  type: AssignmentType
}

export interface AuditTrail {
  at: string
  user: string
  message: string
}

export interface Employee {
  id: string
  empNo: string
  name: string
  team: TeamCode
  position: string // 직급 코드
  roles: string[] // 보유역할 (AA, TA 등)
  skills: EmployeeSkill[]
  allocation: number // 현재 투입률 합계
  availableDate: string // 가동 가능일 ('즉시' or YYYY-MM-DD)
  status: EmployeeStatus
  email: string
  phone: string
  hireDate: string
  assignments: EmployeeAssignment[]
  history: AuditTrail[]
}

export interface Project {
  id: string
  code: string
  name: string
  client: string
  status: ProjectStatus
  startDate: string
  endDate: string
  memberCount: number
  desc: string
  members: {
    empNo: string
    name: string
    role: string
    allocation: number
    type: AssignmentType
    startDate: string
    endDate: string
  }[]
  history: AuditTrail[]
}

export interface Assignment {
  id: string
  type: AssignmentType
  empNo: string
  name: string
  projectName: string
  role: string
  startDate: string
  endDate: string
  allocation: number
  status: AssignmentStatus
  remark: string
}

export interface AvailabilityRow {
  kind: AvailabilityKind
  empNo: string
  name: string
  team: TeamCode
  jobType: string
  skills: string[]
  allocation: number
  availableDate: string
}

export interface RecommendationRow {
  rank: number
  name: string
  jobType: string
  skills: string[]
  allocation: number
  availableDate: string
  reason: string
  score: number
  detail: {
    jobMatch: number
    skillMatch: number
    proficiency: number
    availability: number
    experience: number
    roleFit: number
  }
}

export interface SystemUser {
  id: string
  loginId: string
  email: string
  role: RoleCode
  linkedEmployee: string
  lastLogin: string
  status: UserStatus
}

export interface AuditLog {
  id: string
  at: string
  user: string
  action: string
  targetTable: string
  targetId: string
  clientIp: string
  before: Record<string, unknown> | null
  after: Record<string, unknown> | null
  userAgent: string
}
