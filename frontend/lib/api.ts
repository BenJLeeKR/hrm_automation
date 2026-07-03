// 인증이 필요한 백엔드 API 호출 공통 헬퍼 — 화면마다 `fetch` + `Authorization` 헤더 조립
// 로직을 반복하지 않도록 추출한다 (대시보드 화면부터 사용, 로드맵 §8 "대시보드 화면 구현").
import { getAccessToken } from './auth'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? ''

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message)
  }
}

export async function apiGet<T>(path: string): Promise<T> {
  const accessToken = getAccessToken()
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {},
  })
  if (!res.ok) {
    throw new ApiError(res.status, `API 요청에 실패했습니다: ${path} (${res.status})`)
  }
  return res.json() as Promise<T>
}

async function apiSend<T>(method: 'POST' | 'PATCH', path: string, body?: unknown): Promise<T> {
  const accessToken = getAccessToken()
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  })
  if (!res.ok) {
    // 등록/수정 화면은 서버가 내려주는 상세 사유(예: 중복 값 409)를 그대로 보여줘야 하므로
    // 응답 본문의 `detail`을 최대한 추출해 에러 메시지에 담는다.
    const detail = await res.json().catch(() => null)
    const message = typeof detail?.detail === 'string' ? detail.detail : `API 요청에 실패했습니다 (${res.status})`
    throw new ApiError(res.status, message)
  }
  return res.json() as Promise<T>
}

export function apiPost<T>(path: string, body?: unknown): Promise<T> {
  return apiSend<T>('POST', path, body)
}

export function apiPatch<T>(path: string, body?: unknown): Promise<T> {
  return apiSend<T>('PATCH', path, body)
}
