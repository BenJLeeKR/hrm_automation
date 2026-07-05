// 인증이 필요한 백엔드 API 호출 공통 헬퍼 — 화면마다 `fetch` + `Authorization` 헤더 조립
// 로직을 반복하지 않도록 추출한다 (대시보드 화면부터 사용, 로드맵 §8 "대시보드 화면 구현").
import { getAccessToken } from './auth'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? ''

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    // Excel Import 검증 실패(422) 시 서버가 내려주는 구조화된 오류 목록 등,
    // 단순 문자열 메시지로 표현할 수 없는 상세 정보를 담기 위한 선택적 필드.
    public detail?: unknown,
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

async function apiSend<T>(method: 'POST' | 'PATCH' | 'PUT', path: string, body?: unknown): Promise<T> {
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

export function apiPut<T>(path: string, body?: unknown): Promise<T> {
  return apiSend<T>('PUT', path, body)
}

export async function apiDelete<T>(path: string): Promise<T> {
  const accessToken = getAccessToken()
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: 'DELETE',
    headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {},
  })
  if (!res.ok) {
    const detail = await res.json().catch(() => null)
    const message = typeof detail?.detail === 'string' ? detail.detail : `API 요청에 실패했습니다 (${res.status})`
    throw new ApiError(res.status, message)
  }
  return res.json() as Promise<T>
}

export async function apiUploadFile<T>(path: string, file: File): Promise<T> {
  const accessToken = getAccessToken()
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {},
    body: formData,
  })
  if (!res.ok) {
    // Import 검증 실패(422)는 {total_rows, error_count, errors: [...]}} 형태의 상세
    // 오류 목록을 함께 내려주므로, 화면에서 활용할 수 있도록 detail에 그대로 담는다.
    const body = await res.json().catch(() => null)
    const message = typeof body?.detail === 'string' ? body.detail : `업로드에 실패했습니다 (${res.status})`
    throw new ApiError(res.status, message, body?.detail)
  }
  return res.json() as Promise<T>
}

export async function apiDownloadFile(path: string, fallbackFilename: string): Promise<void> {
  const accessToken = getAccessToken()
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {},
  })
  if (!res.ok) {
    const detail = await res.json().catch(() => null)
    const message = typeof detail?.detail === 'string' ? detail.detail : `다운로드에 실패했습니다 (${res.status})`
    throw new ApiError(res.status, message)
  }
  const disposition = res.headers.get('Content-Disposition') ?? ''
  const filenameMatch = disposition.match(/filename="?([^";]+)"?/)
  const filename = filenameMatch?.[1] ?? fallbackFilename
  const blob = await res.blob()
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}
