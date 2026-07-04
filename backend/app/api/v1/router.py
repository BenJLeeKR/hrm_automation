from fastapi import APIRouter

from app.api.v1 import (
    ai_chat,
    assignments,
    audit_logs,
    auth,
    availability,
    codes,
    dashboard,
    employee_skills,
    employees,
    projects,
    recommendations,
    reports,
    skills,
    users,
)

# 향후 추가되는 API 라우터도 여기에 include한다.
api_router = APIRouter()
api_router.include_router(employees.router)
api_router.include_router(codes.router)
api_router.include_router(skills.router)
api_router.include_router(employee_skills.router)
api_router.include_router(projects.router)
api_router.include_router(assignments.router)
api_router.include_router(auth.router)
api_router.include_router(availability.router)
api_router.include_router(dashboard.router)
api_router.include_router(recommendations.router)
api_router.include_router(ai_chat.router)
api_router.include_router(reports.router)
api_router.include_router(users.router)
api_router.include_router(audit_logs.router)
