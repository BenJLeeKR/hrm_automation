'use client'

import { useRef, useState } from 'react'
import { Bot, User, Send, Sparkles, Database } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  sql?: string
  table?: { headers: string[]; rows: string[][] }
}

const SUGGESTIONS = [
  'Java와 AWS를 모두 보유한 즉시 가동 가능 인력은?',
  '10월에 투입률이 100%를 초과하는 사원을 알려줘',
  '딜리버리 조직의 평균 가동률은?',
  '아키텍트 경험이 있는 인력을 추천해줘',
]

const CANNED: Record<string, ChatMessage> = {
  java: {
    role: 'assistant',
    content:
      'Java와 AWS를 모두 보유한 인력 중 가동 가능한 사원은 다음과 같습니다. 임도현 사원은 8월 말 G사 프로젝트 종료 후 투입 가능합니다.',
    sql: "SELECT e.name, e.skills FROM HR_EMPL_MST e\nJOIN HR_EMPL_SKILL s ON e.empl_id = s.empl_id\nWHERE s.skill_nm IN ('Java', 'AWS')\nGROUP BY e.empl_id HAVING COUNT(DISTINCT s.skill_nm) = 2;",
    table: {
      headers: ['이름', '직무', '보유 기술', '가동 가능일'],
      rows: [
        ['임도현', 'AA, TA', 'Java, AWS, PostgreSQL', '2026-08-31'],
        ['홍길동', 'PM, AA', 'Java, Spring', '즉시'],
      ],
    },
  },
  over: {
    role: 'assistant',
    content:
      '10월 기준 투입률 합계가 100%를 초과하는 사원은 이영희 사원(160%)입니다. B사 그룹웨어(100%)와 C사 포털(60%)에 중복 투입되어 있어 배정 조정이 필요합니다.',
    sql: "SELECT e.name, SUM(a.alloc_rt) AS total_alloc FROM PJT_ASGN_HIS a\nJOIN HR_EMPL_MST e ON a.empl_id = e.empl_id\nWHERE '2026-10-01' BETWEEN a.start_dt AND a.end_dt\nGROUP BY e.empl_id HAVING SUM(a.alloc_rt) > 100;",
    table: {
      headers: ['이름', '투입 합계', '중복 프로젝트'],
      rows: [['이영희', '160%', 'B사 그룹웨어, C사 포털']],
    },
  },
  avg: {
    role: 'assistant',
    content:
      '딜리버리 조직의 현재 평균 가동률은 약 82%입니다. 즉시 가동 가능한 인력이 3명 있어 신규 프로젝트 대응 여력이 있습니다.',
    sql: 'SELECT AVG(alloc_rt) FROM HR_EMPL_MST WHERE team_cd = \'DELIVERY\' AND status = \'ACTIVE\';',
  },
}

function matchAnswer(q: string): ChatMessage {
  const t = q.toLowerCase()
  if (t.includes('java') || t.includes('aws')) return CANNED.java
  if (t.includes('100') || t.includes('초과') || t.includes('10월')) return CANNED.over
  if (t.includes('평균') || t.includes('가동률')) return CANNED.avg
  return {
    role: 'assistant',
    content:
      '질의를 분석했습니다. 현재 프로토타입에서는 예시 질의(기술 보유 인력, 공수 초과, 평균 가동률)에 대한 응답을 제공합니다. 좌측 예시 질문을 선택해 보세요.',
  }
}

export default function AiChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const endRef = useRef<HTMLDivElement>(null)

  function send(text: string) {
    const q = text.trim()
    if (!q) return
    const answer = matchAnswer(q)
    setMessages((prev) => [...prev, { role: 'user', content: q }, answer])
    setInput('')
    requestAnimationFrame(() =>
      endRef.current?.scrollIntoView({ behavior: 'smooth' }),
    )
  }

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col">
      <div className="px-6 pt-6">
        <PageHeader
          title="AI 질의응답"
          description="자연어로 인력 데이터를 질의하면 자동 생성된 SQL과 결과를 확인할 수 있습니다."
        />
      </div>

      <div className="flex flex-1 gap-6 overflow-hidden px-6 pb-6">
        <div className="hidden w-64 shrink-0 lg:block">
          <Card>
            <CardContent className="flex flex-col gap-2 pt-6">
              <p className="mb-1 text-xs font-semibold text-muted-foreground">
                예시 질문
              </p>
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => send(s)}
                  className="rounded-lg border border-border bg-card px-3 py-2 text-left text-sm text-foreground transition-colors hover:border-primary/40 hover:bg-accent"
                >
                  {s}
                </button>
              ))}
            </CardContent>
          </Card>
        </div>

        <Card className="flex flex-1 flex-col overflow-hidden">
          <div className="flex-1 space-y-5 overflow-y-auto scrollbar-thin p-6">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center text-center">
                <div className="flex size-12 items-center justify-center rounded-lg bg-accent">
                  <Sparkles className="size-6 text-primary" />
                </div>
                <p className="mt-4 font-semibold">무엇이든 물어보세요</p>
                <p className="mt-1 max-w-sm text-sm text-muted-foreground">
                  인력 현황, 기술 보유자, 가동 가능성 등을 자연어로 질의할 수 있습니다.
                </p>
              </div>
            ) : (
              messages.map((m, i) => (
                <div
                  key={i}
                  className={cn(
                    'flex gap-3',
                    m.role === 'user' && 'flex-row-reverse',
                  )}
                >
                  <div
                    className={cn(
                      'flex size-8 shrink-0 items-center justify-center rounded-full',
                      m.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-accent text-primary',
                    )}
                  >
                    {m.role === 'user' ? (
                      <User className="size-4" />
                    ) : (
                      <Bot className="size-4" />
                    )}
                  </div>
                  <div
                    className={cn(
                      'max-w-[80%] space-y-3',
                      m.role === 'user' && 'items-end',
                    )}
                  >
                    <div
                      className={cn(
                        'rounded-lg px-4 py-2.5 text-sm leading-relaxed',
                        m.role === 'user'
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-secondary text-foreground',
                      )}
                    >
                      {m.content}
                    </div>

                    {m.sql && (
                      <div className="overflow-hidden rounded-lg border border-border bg-[#0f172a]">
                        <div className="flex items-center gap-1.5 border-b border-white/10 px-3 py-1.5">
                          <Database className="size-3.5 text-[#7dd3fc]" />
                          <span className="text-xs font-medium text-[#cbd5e1]">
                            생성된 SQL
                          </span>
                        </div>
                        <pre className="overflow-x-auto scrollbar-thin px-3 py-2.5 font-mono text-xs leading-relaxed text-[#e2e8f0]">
                          {m.sql}
                        </pre>
                      </div>
                    )}

                    {m.table && (
                      <div className="overflow-hidden rounded-lg border border-border">
                        <table className="w-full text-sm">
                          <thead className="bg-muted/60">
                            <tr>
                              {m.table.headers.map((h) => (
                                <th
                                  key={h}
                                  className="px-3 py-2 text-left text-xs font-semibold text-muted-foreground"
                                >
                                  {h}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {m.table.rows.map((row, ri) => (
                              <tr key={ri} className="border-t border-border">
                                {row.map((cell, ci) => (
                                  <td key={ci} className="px-3 py-2">
                                    {cell}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            <div ref={endRef} />
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault()
              send(input)
            }}
            className="flex items-center gap-2 border-t border-border p-4"
          >
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="질문을 입력하세요..."
              className="h-10 flex-1 rounded-lg border border-input bg-card px-3 text-sm shadow-sm focus-visible:border-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/30"
            />
            <Button type="submit" size="icon" disabled={!input.trim()}>
              <Send className="size-4" />
            </Button>
          </form>
        </Card>
      </div>
    </div>
  )
}
