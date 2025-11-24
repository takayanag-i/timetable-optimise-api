import pulp
from domain.constraints.credit import CreditConstraint


def test_credit_constraint(mock_annual_model):
    credit_constraint = CreditConstraint()
    model = credit_constraint.apply(mock_annual_model)

    expected_constraints = [
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_1_C1", "value": 1},
                {"name": "x_H1_mon_2_C1", "value": 1},
                {"name": "x_H1_tue_1_C1", "value": 1},
                {"name": "x_H1_tue_2_C1", "value": 1},
            ],
            "constant": -3,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_1_C2", "value": 1},
                {"name": "x_H1_mon_2_C2", "value": 1},
                {"name": "x_H1_tue_1_C2", "value": 1},
                {"name": "x_H1_tue_2_C2", "value": 1},
            ],
            "constant": -2,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_1_C3", "value": 1},
                {"name": "x_H1_mon_2_C3", "value": 1},
                {"name": "x_H1_tue_1_C3", "value": 1},
                {"name": "x_H1_tue_2_C3", "value": 1},
            ],
            "constant": -3,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H2_mon_1_C1", "value": 1},
                {"name": "x_H2_mon_2_C1", "value": 1},
                {"name": "x_H2_mon_3_C1", "value": 1},
                {"name": "x_H2_tue_1_C1", "value": 1},
                {"name": "x_H2_tue_2_C1", "value": 1},
            ],
            "constant": -3,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H2_mon_1_C2", "value": 1},
                {"name": "x_H2_mon_2_C2", "value": 1},
                {"name": "x_H2_mon_3_C2", "value": 1},
                {"name": "x_H2_tue_1_C2", "value": 1},
                {"name": "x_H2_tue_2_C2", "value": 1},
            ],
            "constant": -2,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H3_mon_1_C1", "value": 1},
                {"name": "x_H3_tue_1_C1", "value": 1},
            ],
            "constant": -3,
        },
    ]

    actual_constraints = [v.toDict() for v in model.problem.constraints.values()]

    assert len(actual_constraints) == 6, "数が合わない"

    for expected, acutual in zip(expected_constraints, actual_constraints):
        assert expected["sense"] == acutual["sense"]
        assert expected["constant"] == acutual["constant"]

        expected_coefficients = expected["coefficients"]
        acutual_coefficients = acutual["coefficients"]

        assert len(expected_coefficients) == len(acutual_coefficients)

        for e, a in zip(expected_coefficients, acutual_coefficients):
            assert e["name"] == a["name"]
            assert e["value"] == a["value"]
