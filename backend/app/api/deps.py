import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import ACCESS_TOKEN_TYPE, TokenError, decode_token
from app.db.session import get_db
from app.models.sys_role_mst import SysRoleMst
from app.models.sys_user_mst import SysUserMst
from app.repositories.sys_user_mst import get_user

_bearer_scheme = HTTPBearer(auto_error=False)
_UNAUTHORIZED_HEADERS = {"WWW-Authenticate": "Bearer"}


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> SysUserMst:
    """`Authorization: Bearer <access_token>` 헤더를 검증해 현재 사용자를 조회한다."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="인증 토큰이 필요합니다.", headers=_UNAUTHORIZED_HEADERS
        )
    try:
        payload = decode_token(credentials.credentials, expected_type=ACCESS_TOKEN_TYPE)
        user_id = uuid.UUID(payload["sub"])
    except (TokenError, ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않거나 만료된 토큰입니다.",
            headers=_UNAUTHORIZED_HEADERS,
        ) from exc

    user = get_user(db, user_id)
    if user is None or not user.USE_YN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없거나 비활성 상태입니다.",
            headers=_UNAUTHORIZED_HEADERS,
        )
    return user


def has_permission(db: Session, current_user: SysUserMst, screen: str, action: str) -> bool:
    """`current_user`의 역할이 화면(`screen`)×버튼(`action`) 권한을 갖는지 불리언으로 반환한다.

    `require_permission`과 동일한 `SYS_ROLE_MST.PERM_JSON` 조회 로직을 공유한다 — 라우터
    안에서 "이 요청은 허용하되, 다른 화면의 데이터까지는 못 보여준다"처럼 조건부로 권한을
    확인해야 하는 경우(예: AI Chat의 리소스 검색 결과가 `availability` 화면 데이터를
    노출하므로, 응답 전에 `availability.view` 권한을 확인) 403 예외 대신 값으로 받아
    분기하고 싶을 때 사용한다.
    """
    role = db.get(SysRoleMst, current_user.ROLE_ID)
    screens = (role.PERM_JSON or {}).get("screens", {}) if role else {}
    return bool(screens.get(screen, {}).get(action, False))


def require_permission(screen: str, action: str):
    """화면(`screen`)×버튼(`action`) 권한 검사 의존성 팩토리.

    `SYS_ROLE_MST.PERM_JSON`(`{"screens": {"<screen>": {"view"/"create"/"update"/"delete"/
    "excel"/"admin": bool}}}`) 기준으로 검사하며, 화면/버튼 키 정의는
    `backend/docs/PERMISSION_MATRIX.md` 참조. 권한이 없으면 403을 반환한다.

    행 단위(row-level) 스코프(예: TEAM_LEAD의 "본인 팀만" 수정)는 이 화면/버튼 단위
    권한으로 표현할 수 없어 이번 구현 범위에서 다루지 않는다 — Seed 주석과 동일한
    한계이며, 필요 시 각 라우터에서 추가 검증한다.
    """

    def _check(current_user: SysUserMst = Depends(get_current_user), db: Session = Depends(get_db)) -> SysUserMst:
        if not has_permission(db, current_user, screen, action):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="해당 작업에 대한 권한이 없습니다.")
        return current_user

    return _check
