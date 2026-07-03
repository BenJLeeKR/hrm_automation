import uuid

from pydantic import BaseModel, ConfigDict


class RoleOut(BaseModel):
    """역할 마스터 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.13, `SYS_ROLE_MST` 컬럼 기준)

    ERD상 REG_DTTM/UPD_DTTM 컬럼이 없어(모델과 동일하게 설계서 원본 그대로) 다른 조회
    스키마와 달리 등록/수정 일시 필드를 포함하지 않는다.
    """

    model_config = ConfigDict(from_attributes=True)

    ROLE_ID: uuid.UUID
    ROLE_CD: str
    ROLE_NM: str
    ROLE_DESC: str | None
    PERM_JSON: dict | None
    USE_YN: bool
