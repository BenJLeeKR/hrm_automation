from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """목록 조회 공통 페이지네이션 응답 (로드맵 §8 다음 작업 1번).

    기존 `EmployeeListResponse`/`ProjectListResponse`/`AssignmentListResponse`가 각자
    동일한 `total`/`skip`/`limit`/`items` 구조를 중복 정의하고 있어 이 제네릭으로 추출한다.
    응답 JSON 형태는 기존과 동일하게 유지된다.
    """

    total: int
    skip: int
    limit: int
    items: list[T]
