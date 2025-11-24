import pulp
from domain.constraints.consecutive_day import ConsecutiveDayConstraint
from domain.models.annual_lp_model import AnnualLpModel
from infrastructure.solvers.gurobi_solver import GurobiSolver


def test_consecutive_day_constraint(mock_annual_model):
    """2単位と3単位の科目でConsecutiveDayConstraintをテストする。"""
    constraint = ConsecutiveDayConstraint()
    model = constraint.apply(mock_annual_model)

    actual_constraints = [c.toDict() for c in model.problem.constraints.values()]

    # テストデータには'mon'と'tue'のみがあるため、月-火のパターンのみ適用される
    # 2単位以上の各科目に対して、月-火パターンの制約を1つ取得する:
    # sum of x[homeroom, mon, p, course] + x[homeroom, tue, p, course] <= 1

    # 各科目の期待される制約 (C1=3単位、C2=2単位、C3=3単位):
    expected_constraints = [
        # C1 (3単位): 月-火パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_mon_1_C1", "value": 1},
                {"name": "x_H1_mon_2_C1", "value": 1},
                {"name": "x_H1_tue_1_C1", "value": 1},
                {"name": "x_H1_tue_2_C1", "value": 1},
                {"name": "v^2_C1", "value": -5},  # ペナルティ変数
            ],
            "constant": -1,  # <= 1 は定数が -1 を意味する
        },
        # C2 (2単位): 月-火パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_mon_1_C2", "value": 1},
                {"name": "x_H1_mon_2_C2", "value": 1},
                {"name": "x_H1_tue_1_C2", "value": 1},
                {"name": "x_H1_tue_2_C2", "value": 1},
                {"name": "v^2_C2", "value": -5},  # ペナルティ変数
            ],
            "constant": -1,  # <= 1 は定数が -1 を意味する
        },
        # C3 (3単位): 月-火パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_mon_1_C3", "value": 1},
                {"name": "x_H1_mon_2_C3", "value": 1},
                {"name": "x_H1_tue_1_C3", "value": 1},
                {"name": "x_H1_tue_2_C3", "value": 1},
                {"name": "v^2_C3", "value": -5},  # ペナルティ変数
            ],
            "constant": -1,  # <= 1 は定数が -1 を意味する
        }
    ]

    # 制約の数を確認する
    expected_count = 3
    assert len(actual_constraints) == expected_count, f"数が合わない。期待: {expected_count}, 実際: {len(actual_constraints)}"

    for expected, actual in zip(expected_constraints, actual_constraints):
        assert expected["sense"] == actual["sense"]
        assert expected["constant"] == actual["constant"]

        expected_coefficients = expected["coefficients"]
        actual_coefficients = actual["coefficients"]

        assert len(expected_coefficients) == len(actual_coefficients)

        for e, a in zip(expected_coefficients, actual_coefficients):
            assert e["name"] == a["name"]
            assert e["value"] == a["value"]


def test_consecutive_day_constraint_with_full_week(mock_annual_data):
    """全ての曜日でConsecutiveDayConstraintをテストして、全パターンが動作することを検証する。"""

    # 全ての曜日を持つデータを作成する
    full_week_data = mock_annual_data.model_copy(update={
        "D": ["mon", "tue", "wed", "thu", "fri"],
        "homeroom_day_dict": {
            "H1": {"mon": [1, 2], "tue": [1, 2], "wed": [1, 2], "thu": [1, 2], "fri": [1, 2]},
            "H2": {"mon": [1, 2, 3], "tue": [1, 2], "wed": [1, 2], "thu": [1, 2], "fri": [1, 2]},
            "H3": {"mon": [1], "tue": [1], "wed": [1], "thu": [1], "fri": [1]}
        },
        "school_day_dict": {
            "mon": {"am_periods": 2, "pm_periods": 1},
            "tue": {"am_periods": 1, "pm_periods": 1},
            "wed": {"am_periods": 1, "pm_periods": 1},
            "thu": {"am_periods": 1, "pm_periods": 1},
            "fri": {"am_periods": 1, "pm_periods": 1}
        },
        "credit_dict": {"C1": 3, "C2": 2, "C3": 3}  # C1とC3は3単位、C2は2単位
    })

    full_week_model = AnnualLpModel(full_week_data, [], GurobiSolver())

    constraint = ConsecutiveDayConstraint()
    model = constraint.apply(full_week_model)

    actual_constraints = [c.toDict() for c in model.problem.constraints.values()]

    # 期待される制約を具体的に列挙する
    expected_constraints = [
        # C1 (3単位): 2日パターン
        # 月-火パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_mon_1_C1", "value": 1},
                {"name": "x_H1_mon_2_C1", "value": 1},
                {"name": "x_H1_tue_1_C1", "value": 1},
                {"name": "x_H1_tue_2_C1", "value": 1},
                {"name": "v^2_C1", "value": -5},
            ],
            "constant": -1,
        },
        # 火-水パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_tue_1_C1", "value": 1},
                {"name": "x_H1_tue_2_C1", "value": 1},
                {"name": "x_H1_wed_1_C1", "value": 1},
                {"name": "x_H1_wed_2_C1", "value": 1},
                {"name": "v^2_C1", "value": -5},
            ],
            "constant": -1,
        },
        # 水-木パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_wed_1_C1", "value": 1},
                {"name": "x_H1_wed_2_C1", "value": 1},
                {"name": "x_H1_thu_1_C1", "value": 1},
                {"name": "x_H1_thu_2_C1", "value": 1},
                {"name": "v^2_C1", "value": -5},
            ],
            "constant": -1,
        },
        # 木-金パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_thu_1_C1", "value": 1},
                {"name": "x_H1_thu_2_C1", "value": 1},
                {"name": "x_H1_fri_1_C1", "value": 1},
                {"name": "x_H1_fri_2_C1", "value": 1},
                {"name": "v^2_C1", "value": -5},
            ],
            "constant": -1,
        },
        # C1 (3単位): 3日パターン
        # 月-火-水パターン <= 2
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_mon_1_C1", "value": 1},
                {"name": "x_H1_mon_2_C1", "value": 1},
                {"name": "x_H1_tue_1_C1", "value": 1},
                {"name": "x_H1_tue_2_C1", "value": 1},
                {"name": "x_H1_wed_1_C1", "value": 1},
                {"name": "x_H1_wed_2_C1", "value": 1},
                {"name": "v^2_C1", "value": -5},
            ],
            "constant": -2,
        },
        # 火-水-木パターン <= 2
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_tue_1_C1", "value": 1},
                {"name": "x_H1_tue_2_C1", "value": 1},
                {"name": "x_H1_wed_1_C1", "value": 1},
                {"name": "x_H1_wed_2_C1", "value": 1},
                {"name": "x_H1_thu_1_C1", "value": 1},
                {"name": "x_H1_thu_2_C1", "value": 1},
                {"name": "v^2_C1", "value": -5},
            ],
            "constant": -2,
        },
        # 水-木-金パターン <= 2
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_wed_1_C1", "value": 1},
                {"name": "x_H1_wed_2_C1", "value": 1},
                {"name": "x_H1_thu_1_C1", "value": 1},
                {"name": "x_H1_thu_2_C1", "value": 1},
                {"name": "x_H1_fri_1_C1", "value": 1},
                {"name": "x_H1_fri_2_C1", "value": 1},
                {"name": "v^2_C1", "value": -5},
            ],
            "constant": -2,
        },
        # C2 (2単位): 2日パターンのみ
        # 月-火パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_mon_1_C2", "value": 1},
                {"name": "x_H1_mon_2_C2", "value": 1},
                {"name": "x_H1_tue_1_C2", "value": 1},
                {"name": "x_H1_tue_2_C2", "value": 1},
                {"name": "v^2_C2", "value": -5},
            ],
            "constant": -1,
        },
        # 火-水パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_tue_1_C2", "value": 1},
                {"name": "x_H1_tue_2_C2", "value": 1},
                {"name": "x_H1_wed_1_C2", "value": 1},
                {"name": "x_H1_wed_2_C2", "value": 1},
                {"name": "v^2_C2", "value": -5},
            ],
            "constant": -1,
        },
        # 水-木パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_wed_1_C2", "value": 1},
                {"name": "x_H1_wed_2_C2", "value": 1},
                {"name": "x_H1_thu_1_C2", "value": 1},
                {"name": "x_H1_thu_2_C2", "value": 1},
                {"name": "v^2_C2", "value": -5},
            ],
            "constant": -1,
        },
        # 木-金パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_thu_1_C2", "value": 1},
                {"name": "x_H1_thu_2_C2", "value": 1},
                {"name": "x_H1_fri_1_C2", "value": 1},
                {"name": "x_H1_fri_2_C2", "value": 1},
                {"name": "v^2_C2", "value": -5},
            ],
            "constant": -1,
        },
        # C3 (3単位): 2日パターン
        # 月-火パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_mon_1_C3", "value": 1},
                {"name": "x_H1_mon_2_C3", "value": 1},
                {"name": "x_H1_tue_1_C3", "value": 1},
                {"name": "x_H1_tue_2_C3", "value": 1},
                {"name": "v^2_C3", "value": -5},
            ],
            "constant": -1,
        },
        # 火-水パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_tue_1_C3", "value": 1},
                {"name": "x_H1_tue_2_C3", "value": 1},
                {"name": "x_H1_wed_1_C3", "value": 1},
                {"name": "x_H1_wed_2_C3", "value": 1},
                {"name": "v^2_C3", "value": -5},
            ],
            "constant": -1,
        },
        # 水-木パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_wed_1_C3", "value": 1},
                {"name": "x_H1_wed_2_C3", "value": 1},
                {"name": "x_H1_thu_1_C3", "value": 1},
                {"name": "x_H1_thu_2_C3", "value": 1},
                {"name": "v^2_C3", "value": -5},
            ],
            "constant": -1,
        },
        # 木-金パターン <= 1
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_thu_1_C3", "value": 1},
                {"name": "x_H1_thu_2_C3", "value": 1},
                {"name": "x_H1_fri_1_C3", "value": 1},
                {"name": "x_H1_fri_2_C3", "value": 1},
                {"name": "v^2_C3", "value": -5},
            ],
            "constant": -1,
        },
        # C3 (3単位): 3日パターン
        # 月-火-水パターン <= 2
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_mon_1_C3", "value": 1},
                {"name": "x_H1_mon_2_C3", "value": 1},
                {"name": "x_H1_tue_1_C3", "value": 1},
                {"name": "x_H1_tue_2_C3", "value": 1},
                {"name": "x_H1_wed_1_C3", "value": 1},
                {"name": "x_H1_wed_2_C3", "value": 1},
                {"name": "v^2_C3", "value": -5},
            ],
            "constant": -2,
        },
        # 火-水-木パターン <= 2
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_tue_1_C3", "value": 1},
                {"name": "x_H1_tue_2_C3", "value": 1},
                {"name": "x_H1_wed_1_C3", "value": 1},
                {"name": "x_H1_wed_2_C3", "value": 1},
                {"name": "x_H1_thu_1_C3", "value": 1},
                {"name": "x_H1_thu_2_C3", "value": 1},
                {"name": "v^2_C3", "value": -5},
            ],
            "constant": -2,
        },
        # 水-木-金パターン <= 2
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H1_wed_1_C3", "value": 1},
                {"name": "x_H1_wed_2_C3", "value": 1},
                {"name": "x_H1_thu_1_C3", "value": 1},
                {"name": "x_H1_thu_2_C3", "value": 1},
                {"name": "x_H1_fri_1_C3", "value": 1},
                {"name": "x_H1_fri_2_C3", "value": 1},
                {"name": "v^2_C3", "value": -5},
            ],
            "constant": -2,
        },
    ]

    # 制約の数を確認する
    expected_count = 18  # 7 (C1) + 4 (C2) + 7 (C3)
    assert len(actual_constraints) == expected_count, f"数が合わない。期待: {expected_count}, 実際: {len(actual_constraints)}"

    for expected, actual in zip(expected_constraints, actual_constraints):
        assert expected["sense"] == actual["sense"]
        assert expected["constant"] == actual["constant"]

        expected_coefficients = expected["coefficients"]
        actual_coefficients = actual["coefficients"]

        assert len(expected_coefficients) == len(actual_coefficients)

        for e, a in zip(expected_coefficients, actual_coefficients):
            assert e["name"] == a["name"]
            assert e["value"] == a["value"]
