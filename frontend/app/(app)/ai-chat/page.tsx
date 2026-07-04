'use client'

import { useRef, useState } from 'react'
import { Bot, User, Send, Sparkles } from 'lucide-react'
import { PageHeader } from '@/components/common/page-header'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { apiPost, ApiError } from '@/lib/api'

// AI Chat 1차 구현 범위(로드맵 §8 "AI Chat 화면 구현", 사용자 확정 — §9 리스크 참조):
// LLM 단순 호출/응답만 다룬다. 설계서(SCR-012)가 요구하는 자연어 조건 파싱 → SQL 조회 →
// 결과 요약 흐름(예시 응답에 SQL·결과 테이블을 함께 보여주던 이전 프로토타입 목데이터)은
// 후속 작업으로 분리되어 이번 화면에서는 대화 텍스트만 주고받는다.
interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}
interface ChatResponse {
  reply: string
}

const SUGGESTIONS = [
  'Java와 AWS를 모두 보유한 즉시 가동 가능 인력은?',
  '10월에 투입률이 100%를 초과하는 사원을 알려줘',
  '딜리버리 조직의 평균 가동률은?',
  '아키텍트 경험이 있는 인력을 추천해줘',
]

export default function AiChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const endRef = useRef<HTMLDivElement>(null)

  async function send(text: string) {
    const q = text.trim()
    if (!q || sending) return

    setMessages((prev) => [...prev, { role: 'user', content: q }])
    setInput('')
    setSending(true)
    requestAnimationFrame(() => endRef.current?.scrollIntoView({ behavior: 'smooth' }))

    try {
      const res = await apiPost<ChatResponse>('/api/v1/ai/chat', { message: q })
      setMessages((prev) => [...prev, { role: 'assistant', content: res.reply }])
    } catch (err) {
      const message = err instanceof ApiError ? err.message : 'AI 응답을 받지 못했습니다. 잠시 후 다시 시도하세요.'
      setMessages((prev) => [...prev, { role: 'assistant', content: message }])
    } finally {
      setSending(false)
      requestAnimationFrame(() => endRef.current?.scrollIntoView({ behavior: 'smooth' }))
    }
  }

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col">
      <div className="px-6 pt-6">
        <PageHeader
          title="AI 질의응답"
          description="자연어로 질문하면 AI가 답변합니다."
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
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                현재는 LLM과의 자유 대화만 지원합니다. 인력 데이터 기반 자동 조회·요약
                기능은 준비 중입니다.
              </p>
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
                  좌측 예시 질문을 선택하거나 자유롭게 질문을 입력해 보세요.
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
                        'rounded-lg px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap',
                        m.role === 'user'
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-secondary text-foreground',
                      )}
                    >
                      {m.content}
                    </div>
                  </div>
                </div>
              ))
            )}
            {sending && (
              <div className="flex gap-3">
                <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-accent text-primary">
                  <Bot className="size-4" />
                </div>
                <div className="rounded-lg bg-secondary px-4 py-2.5 text-sm text-muted-foreground">
                  응답을 생성하는 중입니다...
                </div>
              </div>
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
              disabled={sending}
              className="h-10 flex-1 rounded-lg border border-input bg-card px-3 text-sm shadow-sm focus-visible:border-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/30"
            />
            <Button type="submit" size="icon" disabled={!input.trim() || sending}>
              <Send className="size-4" />
            </Button>
          </form>
        </Card>
      </div>
    </div>
  )
}
