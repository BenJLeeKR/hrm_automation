from fastapi import APIRouter

from app.api.v1 import employees

# 향후 §8 다음 작업 8번 이후 추가되는 API 라우터도 여기에 include한다.
api_router = APIRouter()
api_router.include_router(employees.router)
