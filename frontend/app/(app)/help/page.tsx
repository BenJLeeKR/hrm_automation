'use client'

import { LifeBuoy, BookOpen, Mail, MessageCircle } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { Card, CardContent } from '@/components/ui/card'

const FAQ = [
  {
    q: '투입률 합계가 100%를 초과하면 어떻게 되나요?',
    a: '설정 > 가동률 정책에서 지정한 방식(경고 표시/배정 차단)에 따라 처리되며, 투입 관리 화면 상단에 초과 배정 경고가 표시됩니다.',
  },
  {
    q: '가동 가능 인력은 어떤 기준으로 분류되나요?',
    a: '즉시(미투입), 부분(잔여 공수 보유), 기간 종료 예정(진행 프로젝트 종료 임박)의 세 가지로 자동 분류됩니다.',
  },
  {
    q: '리소스 추천 점수는 어떻게 계산되나요?',
    a: '직무 적합, 기술 일치, 숙련도, 가동 가능성, 경력, 역할 부합도 6개 지표를 가중 합산하여 100점 만점으로 산출합니다.',
  },
  {
    q: 'AI 질의응답은 어떤 데이터를 참조하나요?',
    a: '사원, 기술, 프로젝트, 투입 이력 등 인력 마스터 데이터를 참조하며, 생성된 SQL과 결과 테이블을 함께 제공합니다.',
  },
]

const LINKS = [
  { icon: BookOpen, title: '사용자 가이드', desc: '기능별 상세 매뉴얼 문서' },
  { icon: MessageCircle, title: '문의 채널', desc: '사내 헬프데스크 채널 연결' },
  { icon: Mail, title: '이메일 지원', desc: 'support@bwware.co.kr' },
]

export default function HelpPage() {
  return (
    <div>
      <PageHeader
        title="도움말"
        description="HRM 자동화 시스템 사용에 대한 안내와 지원 채널을 제공합니다."
      />

      <div className="mb-6 grid gap-4 sm:grid-cols-3">
        {LINKS.map((l) => (
          <Card key={l.title}>
            <CardContent className="flex items-start gap-3 pt-6">
              <div className="flex size-10 items-center justify-center rounded-lg bg-accent">
                <l.icon className="size-5 text-primary" />
              </div>
              <div>
                <p className="font-medium">{l.title}</p>
                <p className="text-sm text-muted-foreground">{l.desc}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardContent className="pt-6">
          <div className="mb-4 flex items-center gap-2">
            <LifeBuoy className="size-4 text-primary" />
            <h2 className="font-semibold">자주 묻는 질문</h2>
          </div>
          <div className="flex flex-col divide-y divide-border">
            {FAQ.map((item) => (
              <div key={item.q} className="py-4 first:pt-0 last:pb-0">
                <p className="font-medium text-foreground">{item.q}</p>
                <p className="mt-1.5 text-sm leading-relaxed text-muted-foreground">
                  {item.a}
                </p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
