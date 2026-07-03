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
