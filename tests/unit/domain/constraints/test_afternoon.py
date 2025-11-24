"""AfternoonConstraintクラスの単体テスト。"""

import pulp
from domain.constraints.afternoon import AfternoonConstraint


def test_afternoon_constraint(mock_annual_model) -> None:
    """applyメソッド。"""
    constraint = AfternoonConstraint()
    model = constraint.apply(mock_annual_model)

    expected_constraints = [
        {
            "coefficients": [
                {"name": "x_H1_tue_2_C1", "value": 1},
                {"name": "v^1_C1", "value": -3},
            ],
            "constant": -2,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [
                {"name": "x_H1_tue_2_C2", "value": 1},
                {"name": "v^1_C2", "value": -2},
            ],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [
                {"name": "x_H1_tue_2_C3", "value": 1},
                {"name": "v^1_C3", "value": -3},
            ],
            "constant": -2,
            "sense": pulp.LpConstraintLE,
        },
    ]

    actual_constraints = [v.toDict() for v in model.problem.constraints.values()]

    assert len(actual_constraints) == 3, "数が合わない"

    for expected, actual in zip(expected_constraints, actual_constraints):
        assert expected["sense"] == actual["sense"]
        assert expected["constant"] == actual["constant"]

        expected_coefficients = expected["coefficients"]
        actual_coefficients = actual["coefficients"]

        assert len(expected_coefficients) == len(actual_coefficients)

        for e, a in zip(expected_coefficients, actual_coefficients):
            assert e["name"] == a["name"]
            assert e["value"] == a["value"]
