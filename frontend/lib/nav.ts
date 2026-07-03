import {
  LayoutDashboard,
  Users,
  Wrench,
  Briefcase,
  FolderKanban,
  ClipboardList,
  UserCheck,
  Sparkles,
  Bot,
  BarChart3,
  Settings,
  LifeBuoy,
  type LucideIcon,
} from 'lucide-react'

export interface NavItem {
  label: string
  href: string
  icon: LucideIcon
  /** `SYS_ROLE_MST.PERM_JSON.screens`의 화면 키 — 없으면 권한 필터링 대상이 아니라 항상 노출한다. */
  permKey?: string
}

export const mainNav: NavItem[] = [
  { label: '대시보드', href: '/dashboard', icon: LayoutDashboard, permKey: 'dashboard' },
  { label: '사원 관리', href: '/employees', icon: Users, permKey: 'employees' },
  { label: '기술 관리', href: '/skills', icon: Wrench, permKey: 'skills' },
  { label: '직무 유형', href: '/job-types', icon: Briefcase, permKey: 'job_types' },
  { label: '프로젝트 관리', href: '/projects', icon: FolderKanban, permKey: 'projects' },
  { label: '투입 관리', href: '/assignments', icon: ClipboardList, permKey: 'assignments' },
  { label: '가동 가능 인력', href: '/availability', icon: UserCheck, permKey: 'availability' },
  { label: '리소스 추천', href: '/recommendations', icon: Sparkles, permKey: 'recommendations' },
  { label: 'AI 질의응답', href: '/ai-chat', icon: Bot, permKey: 'ai_chat' },
  { label: '리포트', href: '/reports', icon: BarChart3, permKey: 'reports' },
  { label: '설정', href: '/settings', icon: Settings, permKey: 'settings' },
]

export const bottomNav: NavItem[] = [
  { label: '시스템 설정', href: '/settings', icon: Settings, permKey: 'settings' },
  { label: '도움말', href: '/help', icon: LifeBuoy },
]

/** `PERM_JSON.screens[permKey].view`가 true인 항목만 남긴다. `permKey`가 없는 항목은 항상 노출한다. */
export function filterNavByPermissions(items: NavItem[], permJson: PermJson | null): NavItem[] {
  if (!permJson) return items
  const screens = permJson.screens ?? {}
  return items.filter((item) => !item.permKey || screens[item.permKey]?.view === true)
}

export interface ScreenPerm {
  view?: boolean
  create?: boolean
  update?: boolean
  delete?: boolean
  excel?: boolean
  admin?: boolean
}

export interface PermJson {
  screens?: Record<string, ScreenPerm>
}
