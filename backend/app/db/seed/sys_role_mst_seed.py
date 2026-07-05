# SYS_ROLE_MST 초기 Seed — MVP 확정본 (2026-07-02, v2)
# 배경: 로드맵 §9 리스크 "인증/권한 범위 미정" 대응. 설계서 §5.3.13에는 ROLE_CD 6종
#       (ADMIN/HR_MGR/PM/TEAM_LEAD/EXEC/VIEWER)만 값 목록으로 제시되어 있고 ROLE_NM/
#       ROLE_DESC/PERM_JSON 상세는 없어, Phase 2 Alembic Seed 작성이 가능하도록 MVP
#       기준으로 확정한다.
#
# PERM_JSON 구조 (v2): 화면 접근은 화면 설계서(`[DESIGN]HRM_Screen_Design.md`)
# "화면 목록" 표의 역할 기준을 따르고, 버튼 권한은 6개 카테고리로 표현한다.
#   {"screens": {"<screen_key>": {
#       "view": bool,    # 조회
#       "create": bool,  # 등록
#       "update": bool,  # 수정
#       "delete": bool,  # 삭제
#       "excel": bool,   # Excel Import/Export
#       "admin": bool,   # 관리자 기능
#   }}}
# 상세 근거·역할별 매트릭스는 `backend/docs/PERMISSION_MATRIX.md` 참조.
#
# `codes` 화면 키 (2026-07-03, 운영팀 확인 완료): 부서(`departments`)/직급(`positions`)은
# MVP에서 독립 화면으로 보지 않고 "공통 코드/기준정보"로 취급하기로 확정 — 별도 화면 키를
# 만들지 않고 `codes` 키 하나로 통합한다. `codes.view`는 전 역할 허용, `codes.create`/
# `update`/`delete`는 ADMIN/HR_MGR만 허용. `job_types`(직무 유형)는 기존 화면 키를 그대로
# 유지하며(관리 화면의 등록/수정/삭제는 `job_types.*` 권한 유지), 조회(`GET /job-types`)는
# `codes.view`와 동일하게 전 역할에 허용한다(§9 리스크 "departments/positions/job-types
# 화면 권한 키 미정" 해소 처리 근거).
#
# 주의:
#   1. TEAM_LEAD의 employees.update 등 "본인팀만" 같은 row-level 스코프는 이 구조로
#      표현하지 않는다 — 화면/버튼 노출 여부만 다루며, 데이터 스코프는 API 레이어에서
#      별도 구현해야 한다.
#   2. 화면 설계서에 역할 제한이 명시되지 않은 일부 버튼(예: projects.create,
#      reports.excel/admin)은 같은 화면의 인접 권한 그룹과 동일하게 보수적으로
#      추정했다 — `PERMISSION_MATRIX.md` §5 "운영팀 확인 필요 사항" 참조.
#   3. 이 Seed는 MVP 초안이며 운영팀 최종 확정 전까지 조정될 수 있다.


def _perm(view=False, create=False, update=False, delete=False, excel=False, admin=False):
    return {
        "view": view,
        "create": create,
        "update": update,
        "delete": delete,
        "excel": excel,
        "admin": admin,
    }


def _screens(**screen_perms):
    return {"screens": screen_perms}


SYS_ROLE_MST_SEED = [
    {
        "ROLE_CD": "ADMIN",
        "ROLE_NM": "시스템 관리자",
        "ROLE_DESC": "시스템 전체 설정, 사용자/권한 관리, 전 화면 조회 및 수정 권한을 가진 최고 관리자",
        "PERM_JSON": _screens(
            dashboard=_perm(view=True),
            employees=_perm(view=True, create=True, update=True, delete=True, excel=True),
            skills=_perm(view=True, create=True, update=True, delete=True),
            job_types=_perm(view=True, create=True, update=True, delete=True),
            codes=_perm(view=True, create=True, update=True, delete=True),
            projects=_perm(view=True, create=True, update=True),
            assignments=_perm(view=True, create=True, update=True, excel=True),
            availability=_perm(view=True),
            recommendations=_perm(view=True, create=True),
            ai_chat=_perm(view=True),
            reports=_perm(view=True, excel=True, admin=True),
            settings=_perm(view=True),
            settings_users=_perm(view=True, create=True, update=True, delete=True, admin=True),
            settings_audit_logs=_perm(view=True, excel=True, admin=True),
            settings_notification=_perm(view=True, update=True, admin=True),
        ),
    },
    {
        "ROLE_CD": "HR_MGR",
        "ROLE_NM": "인사 담당자",
        "ROLE_DESC": "사원 정보, 기술/직무 마스터 관리 및 사용자 계정 관리를 담당하는 인사 담당자",
        "PERM_JSON": _screens(
            dashboard=_perm(view=True),
            employees=_perm(view=True, create=True, update=True, delete=True, excel=True),
            skills=_perm(view=True, create=True, update=True, delete=True),
            job_types=_perm(view=True, create=True, update=True, delete=True),
            codes=_perm(view=True, create=True, update=True, delete=True),
            projects=_perm(view=True, create=True, update=True),
            assignments=_perm(view=True, create=True, update=True, excel=True),
            availability=_perm(view=True),
            recommendations=_perm(view=True, create=True),
            ai_chat=_perm(view=True),
            reports=_perm(view=True, excel=True, admin=True),
            settings=_perm(view=True),
            # settings_users/settings_audit_logs: 화면 설계서상 Admin 전용 (A) — HR_MGR 접근 불가
            settings_users=_perm(),
            settings_audit_logs=_perm(),
            settings_notification=_perm(),
        ),
    },
    {
        "ROLE_CD": "PM",
        "ROLE_NM": "프로젝트 매니저",
        "ROLE_DESC": "담당 프로젝트의 투입 관리, 리소스 요청/추천 조회 및 등록 권한을 가진 프로젝트 매니저",
        "PERM_JSON": _screens(
            dashboard=_perm(view=True),
            employees=_perm(view=True),
            skills=_perm(),
            job_types=_perm(),
            codes=_perm(view=True),
            projects=_perm(view=True, create=True, update=True),
            assignments=_perm(view=True, create=True, update=True, excel=True),
            availability=_perm(view=True),
            recommendations=_perm(view=True, create=True),
            ai_chat=_perm(view=True),
            reports=_perm(view=True, excel=True, admin=True),
            settings=_perm(),
            settings_users=_perm(),
            settings_audit_logs=_perm(),
            settings_notification=_perm(),
        ),
    },
    {
        "ROLE_CD": "TEAM_LEAD",
        "ROLE_NM": "팀장",
        "ROLE_DESC": "소속 팀 인력의 투입 현황 및 가동률을 조회·관리하는 팀장",
        "PERM_JSON": _screens(
            dashboard=_perm(view=True),
            # employees.update: 화면 설계서상 "본인팀"만 수정 가능 — row-level 스코프는
            # API 레이어에서 별도 구현 필요 (이 플래그는 화면/버튼 노출 여부만 의미)
            employees=_perm(view=True, update=True),
            skills=_perm(),
            job_types=_perm(),
            codes=_perm(view=True),
            projects=_perm(view=True),
            assignments=_perm(view=True),  # 투입 관리 화면 접근은 가능하나 등록/수정은 A H P만
            availability=_perm(view=True),
            recommendations=_perm(view=True),
            ai_chat=_perm(view=True),
            reports=_perm(),  # 화면 설계서상 리포트 화면 접근 불가
            settings=_perm(),
            settings_users=_perm(),
            settings_audit_logs=_perm(),
            settings_notification=_perm(),
        ),
    },
    {
        "ROLE_CD": "EXEC",
        "ROLE_NM": "임원",
        "ROLE_DESC": "조직 전체 인력·프로젝트 현황을 조회하는 임원 (수정 권한 없음)",
        "PERM_JSON": _screens(
            dashboard=_perm(view=True),
            employees=_perm(view=True),
            skills=_perm(),
            job_types=_perm(),
            codes=_perm(view=True),
            projects=_perm(view=True),
            assignments=_perm(),  # 화면 설계서상 투입 관리 화면 접근 불가 (A H P T만)
            availability=_perm(view=True),
            recommendations=_perm(view=True),
            ai_chat=_perm(view=True),
            reports=_perm(view=True, excel=True, admin=True),
            settings=_perm(),
            settings_users=_perm(),
            settings_audit_logs=_perm(),
            settings_notification=_perm(),
        ),
    },
    {
        "ROLE_CD": "VIEWER",
        "ROLE_NM": "조회자",
        "ROLE_DESC": "제한된 화면만 조회 가능한 최소 권한 사용자 (외부 협력사 등)",
        "PERM_JSON": _screens(
            dashboard=_perm(view=True),
            employees=_perm(view=True),
            skills=_perm(),
            job_types=_perm(),
            codes=_perm(view=True),
            projects=_perm(view=True),
            assignments=_perm(),
            availability=_perm(),  # 화면 설계서상 VIEWER 제외
            recommendations=_perm(),  # 화면 설계서상 VIEWER 제외
            ai_chat=_perm(view=True),
            reports=_perm(),  # 화면 설계서상 VIEWER 제외
            settings=_perm(),
            settings_users=_perm(),
            settings_audit_logs=_perm(),
            settings_notification=_perm(),
        ),
    },
]
