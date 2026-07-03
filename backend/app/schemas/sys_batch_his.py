import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BatchHistoryOut(BaseModel):
    """배치 실행 이력 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.15, `SYS_BATCH_HIS` 컬럼 기준)

    ERD상 이 테이블만 유일하게 제약 표기가 없어(모델과 동일) `BATCH_ID`를 제외한 전 필드가
    선택값이다.
    """

    model_config = ConfigDict(from_attributes=True)

    BATCH_ID: uuid.UUID
    BATCH_NM: str | None
    EXEC_STAT_CD: str | None
    EXEC_STRT_DTTM: datetime | None
    EXEC_END_DTTM: datetime | None
    RSLT_SUMR: str | None
    ERR_MSG: str | None
    CRT_CNT: int | None
    UPD_CNT: int | None
    FAIL_CNT: int | None
    REG_DTTM: datetime
