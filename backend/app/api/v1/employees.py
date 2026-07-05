import io
import uuid
from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile, status
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.core.pagination import PaginationParams
from app.core.security import hash_password, resolve_initial_password
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.hr_empl_mst import (
    create_employee,
    get_employee,
    list_employees,
    list_employees_for_export,
    retire_employee,
    update_employee,
)
from app.repositories.sys_role_mst import get_role_by_code
from app.repositories.sys_user_mst import deactivate_user, get_user_by_empl_id
from app.schemas.hr_empl_mst import EmployeeCreate, EmployeeCreateOut, EmployeeListResponse, EmployeeOut, EmployeeUpdate
from app.schemas.sys_user_mst import SysUserOut
from app.services.employee_import import EmployeeImportValidationError, apply_import, parse_and_validate

_EMPLOYEE_ROLE_CD = "EMPLOYEE"

_TGT_TBL_NM = "HR_EMPL_MST"

# SCR-003 "인력마스터_ResourceTable" 시트 컬럼 매핑([DESIGN]HRM_Screen_Design.md 참조) 그대로 사용
_EXPORT_HEADERS = ["사번", "성명", "팀", "직급", "보유역할", "주요기술", "숙련도", "입사일", "재직상태", "휴대폰번호"]
_EMPL_STAT_LABELS = {"ACTIVE": "재직", "LEAVE": "휴직", "RETIRED": "퇴직"}

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=EmployeeListResponse, dependencies=[Depends(require_permission("employees", "view"))])
def get_employees(
    pagination: PaginationParams = Depends(),
    dept_id: uuid.UUID | None = Query(None, description="부서 ID로 필터링 (HR_DEPT_MST.DEPT_ID)"),
    jikmu_id: uuid.UUID | None = Query(None, description="직무 유형 ID로 필터링 (HR_JIKMU_MST.JIKMU_ID)"),
    empl_stat_cd: str | None = Query(None, description="재직 상태 코드 (ACTIVE/LEAVE/RETIRED)"),
    db: Session = Depends(get_db),
) -> EmployeeListResponse:
    """사원 목록 조회 (로드맵 §8 다음 작업 7번)"""
    items, total = list_employees(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        dept_id=dept_id,
        jikmu_id=jikmu_id,
        empl_stat_cd=empl_stat_cd,
    )
    return EmployeeListResponse(total=total, skip=pagination.skip, limit=pagination.limit, items=items)


@router.get("/export")
def export_employees(
    request: Request,
    dept_id: uuid.UUID | None = Query(None, description="부서 ID로 필터링 (HR_DEPT_MST.DEPT_ID)"),
    jikmu_id: uuid.UUID | None = Query(None, description="직무 유형 ID로 필터링 (HR_JIKMU_MST.JIKMU_ID)"),
    empl_stat_cd: str | None = Query(None, description="재직 상태 코드 (ACTIVE/LEAVE/RETIRED)"),
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("employees", "excel")),
) -> StreamingResponse:
    """사원 목록 Excel 내보내기 (SCR-003 "인력마스터_ResourceTable" 시트 형식).

    현재 필터 결과 전체(페이지네이션 없이)를 내보낸다. 숙련도는 원본 Excel 서식 자체가
    "전체 기술에 동일 숙련도" 한 칸만 두는 손실 매핑이라, 여러 기술의 숙련도가 다르면
    최댓값을 대표로 내보낸다 (`list_employees_for_export` 주석 참조).

    `/{empl_id}`(UUID 경로) 라우트보다 반드시 먼저 등록해야 한다 — FastAPI는 등록 순서대로
    매칭하므로, 뒤에 두면 "export"가 UUID로 파싱되어 422로 가로채인다.
    """
    rows = list_employees_for_export(db, dept_id=dept_id, jikmu_id=jikmu_id, empl_stat_cd=empl_stat_cd)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "인력마스터_ResourceTable"
    sheet.append(_EXPORT_HEADERS)
    for row in rows:
        employee = row["employee"]
        sheet.append(
            [
                employee.EMPL_NO,
                employee.EMPL_NM,
                row["DEPT_NM"],
                row["JIKGUP_NM"],
                row["ROLES"],
                row["SKILLS"],
                row["PRFCY_LEVL"],
                employee.HIRE_DT.isoformat() if employee.HIRE_DT else None,
                _EMPL_STAT_LABELS.get(employee.EMPL_STAT_CD, employee.EMPL_STAT_CD),
                employee.MPHONE_NO,
            ]
        )

    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    record_audit(db, request, current_user, act_cd="EXPORT", tgt_tbl_nm=_TGT_TBL_NM, aft_val_json={"row_count": len(rows)})

    filename = f"employees_{date.today().isoformat()}.xlsx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/import")
async def import_employees(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("employees", "excel")),
) -> dict:
    """사원 목록 Excel 가져오기 (SCR-003 "인력마스터_ResourceTable" 시트 형식).

    정책(로드맵 §7/§9 확정 사항):
    - 팀/직급/역할/기술 명칭이 마스터에 없으면 자동 생성하지 않고 전체 Import를 실패
      처리한다(오타·비표준 명칭 유입 방지). 행 번호/컬럼/입력값/사유를 상세히 반환한다.
    - `EMPL_NO` 기준 Upsert. 단, 파일 내부에 `EMPL_NO`가 중복되면 전체 실패 처리한다.
    - 일부 행만 검증 실패해도 부분 반영하지 않는다 — 검증 오류가 1건이라도 있으면
      DB 변경 없이 422로 응답하고, 전체 통과 시에만 하나의 트랜잭션으로 반영한다.
    """
    content = await file.read()

    try:
        rows = parse_and_validate(db, content)
    except EmployeeImportValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"total_rows": exc.total_rows, "error_count": len(exc.errors), "errors": exc.errors},
        ) from None

    result = apply_import(db, rows)

    record_audit(db, request, current_user, act_cd="IMPORT", tgt_tbl_nm=_TGT_TBL_NM, aft_val_json=result)
    return result


@router.get(
    "/{empl_id}", response_model=EmployeeOut, dependencies=[Depends(require_permission("employees", "view"))]
)
def get_employee_detail(empl_id: uuid.UUID, db: Session = Depends(get_db)) -> EmployeeOut:
    """사원 상세 조회 (로드맵 §8 다음 작업 1번, SCR-004 "사원 상세" 기본 정보)"""
    employee = get_employee(db, empl_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사원을 찾을 수 없습니다.")
    return employee


@router.post("", response_model=EmployeeCreateOut, status_code=status.HTTP_201_CREATED)
def post_employee(
    payload: EmployeeCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("employees", "create")),
) -> EmployeeCreateOut:
    """사원 등록 (로드맵 §8 다음 작업 8번) — 등록과 동시에 `SYS_USER_MST` 계정을 자동
    생성한다(설계서 §5.5 "사원 계정 자동 생성", §8 큐 1-2). `USER_LGID`/`EMAIL_ADDR`는
    사원의 이메일을 그대로 사용, 기본 역할은 `EMPLOYEE`, 임시 비밀번호는 서버가 생성해
    해시만 저장하고 응답에 평문으로 1회 노출한다 — 이메일 발송 인프라가 없어(§9 리스크)
    등록자가 화면에서 확인 후 신규 사원에게 직접 전달해야 한다. 계정 생성이 실패하면
    사원 등록도 함께 실패해야 하므로(트랜잭션 일관성 유지) 두 INSERT를 하나의 커밋으로
    묶는다."""
    employee_role = get_role_by_code(db, _EMPLOYEE_ROLE_CD)
    if employee_role is None:
        # SYS_ROLE_MST Seed가 정상 적용됐다면 발생할 수 없는 상태 — 운영 환경 설정 오류.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="EMPLOYEE 역할이 설정되어 있지 않아 계정을 생성할 수 없습니다.",
        )

    temp_password = resolve_initial_password()
    try:
        employee = create_employee(db, payload.model_dump())
        user = SysUserMst(
            EMPL_ID=employee.EMPL_ID,
            USER_LGID=employee.EMAIL_ADDR,
            EMAIL_ADDR=employee.EMAIL_ADDR,
            ENCR_PWD=hash_password(temp_password),
            ROLE_ID=employee_role.ROLE_ID,
            PWD_CHG_YN=True,
        )
        db.add(user)
        db.commit()
    except IntegrityError:
        # EMPL_NO/EMAIL_ADDR UNIQUE 위반(사원 또는 계정) 또는 DEPT_ID/JIKGUP_ID/JIKMU_ID FK 위반
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="사번/이메일 중복이거나 부서·직급·직무 ID가 유효하지 않습니다.",
        ) from None
    db.refresh(employee)
    db.refresh(user)

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=employee.EMPL_ID,
        aft_val_json=EmployeeOut.model_validate(employee).model_dump(mode="json"),
    )
    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm="SYS_USER_MST",
        tgt_id=user.USER_ID,
        aft_val_json=SysUserOut.model_validate(user).model_dump(mode="json"),
    )
    return EmployeeCreateOut(**EmployeeOut.model_validate(employee).model_dump(), temp_password=temp_password)


@router.patch("/{empl_id}", response_model=EmployeeOut)
def patch_employee(
    empl_id: uuid.UUID,
    payload: EmployeeUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("employees", "update")),
) -> EmployeeOut:
    """사원 수정 (로드맵 §8 다음 작업 8번) — 전달된 필드만 갱신"""
    employee = get_employee(db, empl_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사원을 찾을 수 없습니다.")

    before_snapshot = EmployeeOut.model_validate(employee).model_dump(mode="json")
    try:
        employee = update_employee(db, employee, payload.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="사번/이메일 중복이거나 부서·직급·직무 ID가 유효하지 않습니다.",
        ) from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=employee.EMPL_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=EmployeeOut.model_validate(employee).model_dump(mode="json"),
    )
    return employee


@router.delete("/{empl_id}", response_model=EmployeeOut)
def delete_employee(
    empl_id: uuid.UUID,
    request: Request,
    retir_dt: date | None = Query(None, description="퇴직일 — 생략 시 오늘 날짜로 기록"),
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("employees", "delete")),
) -> EmployeeOut:
    """사원 퇴직 처리 (로드맵 §8 다음 작업 1번) — 로우를 삭제하지 않고
    `EMPL_STAT_CD='RETIRED'` 전환 + `RETIR_DT` 기록만 수행하는 소프트 삭제. 연동된
    `SYS_USER_MST` 계정이 있으면 함께 비활성화한다(설계서 §5.5 "퇴직자 계정 처리",
    §8 큐 1-3 — 설계서에는 이미 명시돼 있었으나 지금까지 미구현 상태였음)."""
    employee = get_employee(db, empl_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사원을 찾을 수 없습니다.")
    if employee.EMPL_STAT_CD == "RETIRED":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 퇴직 처리된 사원입니다.")

    before_snapshot = EmployeeOut.model_validate(employee).model_dump(mode="json")
    employee = retire_employee(db, employee, retir_dt)

    linked_user = get_user_by_empl_id(db, employee.EMPL_ID)
    if linked_user is not None and linked_user.USE_YN:
        user_before_snapshot = SysUserOut.model_validate(linked_user).model_dump(mode="json")
        linked_user = deactivate_user(db, linked_user)
        record_audit(
            db,
            request,
            current_user,
            act_cd="UPDATE",
            tgt_tbl_nm="SYS_USER_MST",
            tgt_id=linked_user.USER_ID,
            bfr_val_json=user_before_snapshot,
            aft_val_json=SysUserOut.model_validate(linked_user).model_dump(mode="json"),
        )

    record_audit(
        db,
        request,
        current_user,
        act_cd="DELETE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=employee.EMPL_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=EmployeeOut.model_validate(employee).model_dump(mode="json"),
    )
    return employee
