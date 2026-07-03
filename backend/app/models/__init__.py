# 이 파일에서 각 모델 모듈을 import해야 alembic/env.py의 `import app.models`를 통해
# Base.metadata에 등록되고 autogenerate 대상에 포함된다.
#
# §8 다음 작업 5번 (7개 테이블):
from app.models.hr_dept_mst import HrDeptMst
from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_jikgup_mst import HrJikgupMst
from app.models.hr_jikmu_mst import HrJikmuMst
from app.models.hr_skill_mst import HrSkillMst
from app.models.pjt_asgn_his import PjtAsgnHis
from app.models.pjt_mst import PjtMst

# §8 다음 작업 6번 (SYS_USER_MST, SYS_ROLE_MST, SYS_AUDIT_LOG):
from app.models.sys_audit_log import SysAuditLog
from app.models.sys_role_mst import SysRoleMst
from app.models.sys_user_mst import SysUserMst

# Phase 2 후속 (ERD 16개 테이블 중 나머지, §11 데이터베이스 체크리스트):
from app.models.hr_avail_snap import HrAvailSnap
from app.models.hr_empl_role_rel import HrEmplRoleRel
from app.models.hr_empl_skill_rel import HrEmplSkillRel

# 남은 3개(PJT_RSRC_REQ, PJT_RCMD_RSLT, SYS_BATCH_HIS)는 이후 작업에서 추가 예정.

__all__ = [
    "HrDeptMst",
    "HrJikgupMst",
    "HrJikmuMst",
    "HrSkillMst",
    "HrEmplMst",
    "PjtMst",
    "PjtAsgnHis",
    "SysRoleMst",
    "SysUserMst",
    "SysAuditLog",
    "HrEmplSkillRel",
    "HrEmplRoleRel",
    "HrAvailSnap",
]
