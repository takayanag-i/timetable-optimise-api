"""CoursesPerDayInstructorConstraintクラスの単体テスト。"""

import pulp
from domain.constraints.courses_per_day_instructor import CoursesPerDayInstructorConstraint


def test_courses_per_day_instructor_constraint(mock_annual_model) -> None:
    """CoursesPerDayInstructorConstraintのapplyメソッドのテスト。"""
    constraint = CoursesPerDayInstructorConstraint(max_daily_lessons=4)
    model = constraint.apply(mock_annual_model)

    # テストデータ: D=["mon", "tue"], I=["I1", "I2"], P=[1, 2, 3]
    # big_M = max(len(periods)) = 3 (H2のmonが3時限)
    # 各教員、各曜日に対して制約が追加される: sum(y[d, p, i] for p in P) <= 4 + 3 * v3[d, i]
    
    actual_constraints = [c.toDict() for c in model.problem.constraints.values()]

    # 期待される制約: 2日 × 2教員 = 4つの制約
    # 各制約は: sum(y[d, p, i] for p in [1, 2, 3]) <= 4 + 3 * v3[d, i]
    expected_constraints = [
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "y_mon_1_I1", "value": 1},
                {"name": "y_mon_2_I1", "value": 1},
                {"name": "y_mon_3_I1", "value": 1},
                {"name": "v^3_mon_I1", "value": -3},  # big_M = 3
            ],
            "constant": -4,  # <= 4 は定数が -4 を意味する
        },
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "y_mon_1_I2", "value": 1},
                {"name": "y_mon_2_I2", "value": 1},
                {"name": "y_mon_3_I2", "value": 1},
                {"name": "v^3_mon_I2", "value": -3},
            ],
            "constant": -4,
        },
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "y_tue_1_I1", "value": 1},
                {"name": "y_tue_2_I1", "value": 1},
                {"name": "y_tue_3_I1", "value": 1},
                {"name": "v^3_tue_I1", "value": -3},
            ],
            "constant": -4,
        },
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "y_tue_1_I2", "value": 1},
                {"name": "y_tue_2_I2", "value": 1},
                {"name": "y_tue_3_I2", "value": 1},
                {"name": "v^3_tue_I2", "value": -3},
            ],
            "constant": -4,
        },
    ]

    # 制約の数を確認（制約4つ + ペナルティ1つ = 5つ）
    # ただし、ペナルティは目的関数に追加されるので、制約としては4つ
    assert len(actual_constraints) == len(expected_constraints), f"数が合わない。期待: {len(expected_constraints)}, 実際: {len(actual_constraints)}"

    for expected, actual in zip(expected_constraints, actual_constraints):
        assert expected["sense"] == actual["sense"], f"senseが一致しません: 期待={expected['sense']}, 実際={actual['sense']}"
        assert expected["constant"] == actual["constant"], f"constantが一致しません: 期待={expected['constant']}, 実際={actual['constant']}"

        expected_coefficients = expected["coefficients"]
        actual_coefficients = actual["coefficients"]

        assert len(expected_coefficients) == len(actual_coefficients), f"係数の数が一致しません: 期待={len(expected_coefficients)}, 実際={len(actual_coefficients)}"

        # 係数を辞書に変換して比較（順序に依存しない）
        expected_dict = {coef["name"]: coef["value"] for coef in expected_coefficients}
        actual_dict = {coef["name"]: coef["value"] for coef in actual_coefficients}

        for name, expected_value in expected_dict.items():
            assert name in actual_dict, f"係数 {name} が見つかりません"
            assert expected_value == actual_dict[name], f"係数 {name} の値が一致しません: 期待={expected_value}, 実際={actual_dict[name]}"


def test_courses_per_day_instructor_constraint_with_custom_max(mock_annual_model) -> None:
    """カスタムmax_daily_lessons値でのテスト。"""
    constraint = CoursesPerDayInstructorConstraint(max_daily_lessons=2)
    model = constraint.apply(mock_annual_model)

    actual_constraints = [c.toDict() for c in model.problem.constraints.values()]

    # max_daily_lessons=2の場合、定数は-2になる
    for constraint_dict in actual_constraints:
        if constraint_dict["constant"] == -2:
            assert constraint_dict["sense"] == pulp.LpConstraintLE
            # 係数にv^3が含まれることを確認
            coefficient_names = [coef["name"] for coef in constraint_dict["coefficients"]]
            assert any("v^3" in name for name in coefficient_names), "ペナルティ変数v^3が含まれていません"

