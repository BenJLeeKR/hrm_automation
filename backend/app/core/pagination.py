from fastapi import Query


class PaginationParams:
    """목록 조회 공통 skip/limit 의존성 (로드맵 §8 다음 작업 1번).

    `employees.py`/`projects.py`/`assignments.py`에 각자 중복 선언되어 있던
    `Query(0, ge=0)`/`Query(20, ge=1, le=200)` 파라미터를 하나로 추출한다.
    FastAPI "classes as dependencies" 패턴 — `pagination: PaginationParams = Depends()`로 주입한다.
    """

    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=200),
    ) -> None:
        self.skip = skip
        self.limit = limit
