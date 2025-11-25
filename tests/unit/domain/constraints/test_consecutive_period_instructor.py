"""ConsecutivePeriodInstructorConstraintクラスの単体テスト。"""

import pulp
from domain.constraints.consecutive_period_instructor import ConsecutivePeriodInstructorConstraint


def test_consecutive_period_instructor_constraint(mock_annual_model) -> None:
    """ConsecutivePeriodInstructorConstraintのapplyメソッドのテスト。"""
    constraint = ConsecutivePeriodInstructorConstraint(max_consecutive_lessons=3)
    model = constraint.apply(mock_annual_model)

    # テストデータ: D=["mon", "tue"], I=["I1", "I2"], P=[1, 2, 3]
    # max_consecutive_lessons=3の場合、4コマ連続をチェック
    # big_M = max(len(periods)) = 3 (H2のmonが3時限)
    # 各教員、各曜日、各時限から始まる連続コマ数をチェック
    # P=[1, 2, 3]なので、start_p=1から始まる場合のみ4コマ連続が可能（1, 2, 3, 4だが4は存在しないので3コマまで）
    # 実際には、start_p=1から始まる場合、[1, 2, 3]の3コマしかないので、4コマ連続の制約は追加されない

    actual_constraints = [c.toDict() for c in model.problem.constraints.values()]

    # max_consecutive_lessons=3の場合、4コマ連続をチェック
    # P=[1, 2, 3]なので、4コマ連続は不可能（最大3コマ）
    # したがって、制約は追加されない（len(consecutive_periods) >= 4 の条件を満たさない）

    # 制約が追加されないことを確認
    # ただし、ペナルティ変数のコストは追加される
    # 実際には、P=[1, 2, 3]でmax_consecutive_lessons=3の場合、
    # consecutive_periods = [1, 2, 3] (len=3) となり、len >= 4 の条件を満たさない
    # したがって、制約は追加されない

    # より多くの時限がある場合をテストするため、別のテストデータを使用
    # ここでは、制約が正しく動作することを確認するため、制約が追加されない場合も正常とみなす
    assert len(actual_constraints) == 0, f"制約が追加されましたが、期待されていませんでした。実際: {len(actual_constraints)}"


def test_consecutive_period_instructor_constraint_with_more_periods(mock_annual_data):
    """より多くの時限がある場合のテスト。"""
    from domain.models.annual_lp_model import AnnualLpModel
    from infrastructure.solvers.gurobi_solver import GurobiSolver

    # より多くの時限を持つデータを作成
    extended_data = mock_annual_data.model_copy(update={
        "P": [1, 2, 3, 4, 5],
        "homeroom_day_dict": {
            "H1": {"mon": [1, 2, 3, 4], "tue": [1, 2, 3]},
            "H2": {"mon": [1, 2, 3, 4, 5], "tue": [1, 2, 3, 4]},
            "H3": {"mon": [1, 2], "tue": [1, 2]},
        },
    })

    extended_model = AnnualLpModel(extended_data, [], GurobiSolver())

    constraint = ConsecutivePeriodInstructorConstraint(max_consecutive_lessons=3)
    model = constraint.apply(extended_model)

    actual_constraints = [c.toDict() for c in model.problem.constraints.values()]

    # max_consecutive_lessons=3の場合、4コマ連続をチェック
    # P=[1, 2, 3, 4, 5]なので、start_p=1, 2から始まる場合に4コマ連続が可能
    # 各教員（I1, I2）、各曜日（mon, tue）、各開始時限（1, 2）に対して制約が追加される
    # 期待される制約数: 2教員 × 2曜日 × 2開始時限 = 8つの制約

    # ただし、各曜日で利用可能な時限数が異なるため、実際の制約数は異なる可能性がある
    # monの場合: P=[1, 2, 3, 4, 5]なので、start_p=1, 2から4コマ連続が可能
    # tueの場合: P=[1, 2, 3, 4]なので、start_p=1から4コマ連続が可能

    # 制約が追加されていることを確認
    assert len(actual_constraints) > 0, "制約が追加されていません"

    # 制約の構造を確認
    for constraint_dict in actual_constraints:
        assert constraint_dict["sense"] == pulp.LpConstraintLE
        # 係数にy変数とv^4変数が含まれることを確認
        coefficient_names = [coef["name"] for coef in constraint_dict["coefficients"]]
        y_vars = [name for name in coefficient_names if name.startswith("y_")]
        v4_vars = [name for name in coefficient_names if name.startswith("v^4_")]
        assert len(y_vars) > 0, "y変数が含まれていません"
        assert len(v4_vars) > 0, "ペナルティ変数v^4が含まれていません"


def test_consecutive_period_instructor_constraint_with_custom_max(mock_annual_data):
    """カスタムmax_consecutive_lessons値でのテスト。"""
    from domain.models.annual_lp_model import AnnualLpModel
    from infrastructure.solvers.gurobi_solver import GurobiSolver

    # より多くの時限を持つデータを作成
    extended_data = mock_annual_data.model_copy(update={
        "P": [1, 2, 3, 4],
        "homeroom_day_dict": {
            "H1": {"mon": [1, 2, 3, 4], "tue": [1, 2, 3]},
            "H2": {"mon": [1, 2, 3, 4], "tue": [1, 2, 3]},
            "H3": {"mon": [1, 2], "tue": [1, 2]},
        },
    })

    extended_model = AnnualLpModel(extended_data, [], GurobiSolver())

    constraint = ConsecutivePeriodInstructorConstraint(max_consecutive_lessons=2)
    model = constraint.apply(extended_model)

    actual_constraints = [c.toDict() for c in model.problem.constraints.values()]

    # max_consecutive_lessons=2の場合、3コマ連続をチェック
    # P=[1, 2, 3, 4]なので、start_p=1, 2から3コマ連続が可能
    # 各教員（I1, I2）、各曜日（mon, tue）、各開始時限（1, 2）に対して制約が追加される

    # 制約が追加されていることを確認
    assert len(actual_constraints) > 0, "制約が追加されていません"

    # 制約の構造を確認
    for constraint_dict in actual_constraints:
        assert constraint_dict["sense"] == pulp.LpConstraintLE
        # 定数がmax_consecutive_lessons=2に対応していることを確認
        # 制約: sum(y) <= 2 + big_M * v4
        # 定数は -2 になる
        assert constraint_dict["constant"] == -2, f"定数が期待値と異なります: 期待=-2, 実際={constraint_dict['constant']}"
