// JWT 인증 API 연동 (로드맵 §4 Phase 4 "로그인 JWT API 연동") — 이전에는 localStorage에
// 세션 마커('1')만 저장하는 임시 방식이었으나, 실제 액세스/리프레시 토큰을 저장하고
// 백엔드 JWT API(`POST /api/v1/auth/{login,refresh,logout}`)를 호출하도록 교체한다.
//
// 토큰 저장 방식은 MVP 단계에서 기존 아키텍처(localStorage)를 그대로 유지한다 — HttpOnly
// Cookie 전환은 백엔드가 Set-Cookie로 토큰을 내려주도록 별도 변경이 필요해 이번 범위에서는
// 다루지 않으며, 로드맵 §6 "인증 방식" 항목에 후속 작업으로 기록되어 있다.
const ACCESS_TOKEN_KEY = 'hrm_access_token'
const REFRESH_TOKEN_KEY = 'hrm_refresh_token'
// 로그인 응답의 SYS_USER_MST.PWD_CHG_YN(임시 비밀번호 상태) — 최초 로그인 강제 비밀번호
// 변경 리다이렉트 판단에 사용한다(설계서 §5.3.9, §8 큐 1-5). 토큰과 함께 저장하되,
// 서버 측 상태가 원본이라 이 값은 "다음 화면 이동을 막을지"를 빠르게 판단하는 캐시일
// 뿐이다 — 실제 비밀번호 변경 완료 여부는 항상 백엔드 검증을 거친다.
const PWD_CHG_YN_KEY = 'hrm_pwd_chg_yn'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? ''

export function isAuthenticated(): boolean {
  if (typeof window === 'undefined') return false
  return Boolean(window.localStorage.getItem(ACCESS_TOKEN_KEY))
}

export function getAccessToken(): string | null {
  if (typeof window === 'undefined') return null
  return window.localStorage.getItem(ACCESS_TOKEN_KEY)
}

/** 최초 로그인 강제 비밀번호 변경이 필요한 상태인지 확인한다. */
export function requiresPasswordChange(): boolean {
  if (typeof window === 'undefined') return false
  return window.localStorage.getItem(PWD_CHG_YN_KEY) === 'true'
}

/** 비밀번호 변경 완료 후 강제 리다이렉트 플래그를 해제한다. */
export function clearPasswordChangeRequirement(): void {
  if (typeof window === 'undefined') return
  window.localStorage.setItem(PWD_CHG_YN_KEY, 'false')
}

function setSession(accessToken: string, refreshToken: string, pwdChgYn: boolean): void {
  if (typeof window === 'undefined') return
  window.localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
  window.localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
  window.localStorage.setItem(PWD_CHG_YN_KEY, String(pwdChgYn))
}

function clearSession(): void {
  if (typeof window === 'undefined') return
  window.localStorage.removeItem(ACCESS_TOKEN_KEY)
  window.localStorage.removeItem(REFRESH_TOKEN_KEY)
  window.localStorage.removeItem(PWD_CHG_YN_KEY)
}

export interface LoginResult {
  ok: boolean
  error?: string
  pwdChgYn?: boolean
}

export async function login(userLoginId: string, password: string): Promise<LoginResult> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ USER_LGID: userLoginId, password }),
    })

    if (!res.ok) {
      if (res.status === 401) {
        return { ok: false, error: '아이디 또는 비밀번호가 올바르지 않습니다.' }
      }
      return { ok: false, error: '로그인 중 오류가 발생했습니다. 잠시 후 다시 시도하세요.' }
    }

    const data = (await res.json()) as { access_token: string; refresh_token: string; pwd_chg_yn: boolean }
    setSession(data.access_token, data.refresh_token, data.pwd_chg_yn)
    return { ok: true, pwdChgYn: data.pwd_chg_yn }
  } catch {
    return { ok: false, error: '서버에 연결할 수 없습니다. 네트워크 상태를 확인하세요.' }
  }
}

export interface CurrentUser {
  USER_ID: string
  USER_LGID: string
  EMAIL_ADDR: string
  ROLE_CD: string
  ROLE_NM: string
  PERM_JSON: { screens?: Record<string, { view?: boolean }> } | null
}

/** 현재 로그인 사용자 정보와 역할 권한(`PERM_JSON`)을 조회한다 — 사이드바 메뉴를
 * 역할별로 필터링하는 데 사용한다 (로드맵 §8 "권한별 메뉴 제어"). 인증 실패·네트워크
 * 오류 시 `null`을 반환하며, 호출부에서 메뉴 필터링을 생략(전체 노출)하도록 한다. */
export async function getMe(): Promise<CurrentUser | null> {
  const accessToken = getAccessToken()
  if (!accessToken) return null

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    })
    if (!res.ok) return null
    return (await res.json()) as CurrentUser
  } catch {
    return null
  }
}

export async function logout(): Promise<void> {
  const accessToken = getAccessToken()
  const refreshToken = typeof window === 'undefined' ? null : window.localStorage.getItem(REFRESH_TOKEN_KEY)
  clearSession()
  if (!accessToken) return

  // 로그아웃 API 호출은 최선 노력(best-effort)으로 처리한다 — 실패해도 클라이언트 세션은
  // 이미 삭제되었으므로 사용자 경험에는 영향이 없다. 액세스/리프레시 토큰을 함께 전달하면
  // 백엔드가 Redis 블랙리스트에 즉시 등록해 서버 측 무효화까지 수행한다
  // (backend/app/core/token_blacklist.py, §9-1 "로그아웃 시 서버 측 즉시 토큰 무효화 미구현" 해소).
  try {
    await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    })
  } catch {
    // 네트워크 오류는 무시 — 클라이언트 세션 삭제만으로 로그아웃 처리를 완료한다
  }
}
