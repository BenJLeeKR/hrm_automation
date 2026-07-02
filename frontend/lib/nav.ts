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
}

export const mainNav: NavItem[] = [
  { label: '대시보드', href: '/dashboard', icon: LayoutDashboard },
  { label: '사원 관리', href: '/employees', icon: Users },
  { label: '기술 관리', href: '/skills', icon: Wrench },
  { label: '직무 유형', href: '/job-types', icon: Briefcase },
  { label: '프로젝트 관리', href: '/projects', icon: FolderKanban },
  { label: '투입 관리', href: '/assignments', icon: ClipboardList },
  { label: '가동 가능 인력', href: '/availability', icon: UserCheck },
  { label: '리소스 추천', href: '/recommendations', icon: Sparkles },
  { label: 'AI 질의응답', href: '/ai-chat', icon: Bot },
  { label: '리포트', href: '/reports', icon: BarChart3 },
  { label: '설정', href: '/settings', icon: Settings },
]

export const bottomNav: NavItem[] = [
  { label: '시스템 설정', href: '/settings', icon: Settings },
  { label: '도움말', href: '/help', icon: LifeBuoy },
]
