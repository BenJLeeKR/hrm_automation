// MVP 임시 인증 상태 헬퍼 — 백엔드 JWT 인증 API(로드맵 §4 Phase 3 "JWT 인증 API 구현")가
// 아직 구현되지 않아, 로그인 화면·공통 네비게이션 완성을 위해 localStorage 기반 세션
// 마커로 임시 대체한다. JWT API 연동 시 이 파일을 실제 토큰 저장/검증 로직으로 교체해야 한다.
const AUTH_STORAGE_KEY = 'hrm_auth_session'

export function isAuthenticated(): boolean {
  if (typeof window === 'undefined') return false
  return window.localStorage.getItem(AUTH_STORAGE_KEY) === '1'
}

export function setAuthenticated(): void {
  if (typeof window === 'undefined') return
  window.localStorage.setItem(AUTH_STORAGE_KEY, '1')
}

export function clearAuthenticated(): void {
  if (typeof window === 'undefined') return
  window.localStorage.removeItem(AUTH_STORAGE_KEY)
}
