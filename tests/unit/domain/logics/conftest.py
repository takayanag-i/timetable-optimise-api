import pytest

from domain.models.annual_lp_model import AnnualLpModel
from domain.vo.annual_data import AnnualDataVo, CourseDetailVo
from infrastructure.solvers.gurobi_solver import GurobiSolver


@pytest.fixture
def mock_annual_data() -> AnnualDataVo:
    """年次LPモデルのテスト用の年次データを生成する。"""
    return AnnualDataVo(
        H=["H1", "H2", "H3"],
        D=["mon", "tue"],
        P=[1, 2, 3],
        C=["C1", "C2", "C3"],
        I=["I1", "I2"],
        homeroom_day_dict={
            "H1": {"mon": [1, 2], "tue": [1, 2]},
            "H2": {"mon": [1, 2, 3], "tue": [1, 2]},
            "H3": {"mon": [1], "tue": [1]}
        },
        curriculum_dict={
            "H1": [[["C1"]], [["C2"]]],
            "H2": [[["C2", "C3"]]],
            "H3": [[["C3"]]],
        },
        credit_dict={
            "C1": 3,
            "C2": 2,
            "C3": 1,
        },
        course_details_dict={
            "C1": [
                CourseDetailVo(instructor_id="I1", room_id="R1")
            ],
            "C2": [
                CourseDetailVo(instructor_id="I1", room_id="R1"),
                CourseDetailVo(instructor_id="I2", room_id="R2")
            ],
            "C3": [
                CourseDetailVo(instructor_id="I2", room_id="R2")
            ],
        },
        school_day_dict={
            "mon": {
                "am_periods": 2,
                "pm_periods": 1,
            },
            "tue": {
                "am_periods": 1,
                "pm_periods": 1,
            }
        },
        attendance_day_dict={
            "I1": {
                "mon": [1, 2],
                "tue": []
            },
            "I2": {
                "mon": [],
                "tue": []
            }
        }
    )


@pytest.fixture
def mock_annual_model(mock_annual_data: AnnualDataVo) -> AnnualLpModel:
    """制約タイプのテスト用の年次LPモデルを生成する。"""
    solver = GurobiSolver()
    return AnnualLpModel(mock_annual_data, [], solver)
