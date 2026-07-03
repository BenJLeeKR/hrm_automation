# Phase 2에서 테이블별 ORM 모델을 추가할 때 이 파일에서 각 모델 모듈을 import한다.
# alembic/env.py가 `import app.models`를 통해 이 파일을 로드하므로, 여기서 import되지
# 않은 모델은 Base.metadata에 등록되지 않아 autogenerate 대상에서 누락된다.
#
# 예시 (Phase 2 §8 다음 작업 5~6번에서 추가 예정):
# from app.models.hr_dept_mst import HrDeptMst
# from app.models.hr_empl_mst import HrEmplMst
# ...
