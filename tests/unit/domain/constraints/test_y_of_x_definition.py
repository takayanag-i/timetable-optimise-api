import pulp
from domain.constraints.y_of_x_definition import YofXDefinition


def test_y_of_x_definition(mock_annual_model):
    course_constraint = YofXDefinition()
    model = course_constraint.apply(mock_annual_model)

    expected_constraints = [
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_mon_1_I1", "value": 1},
                {"name": "x_H1_mon_1_C1", "value": -1},
                {"name": "x_H1_mon_1_C2", "value": -1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_mon_1_I2", "value": 1},
                {"name": "x_H1_mon_1_C2", "value": -1},
                {"name": "x_H1_mon_1_C3", "value": -1},

            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_mon_2_I1", "value": 1},
                {"name": "x_H1_mon_2_C1", "value": -1},
                {"name": "x_H1_mon_2_C2", "value": -1},

            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_mon_2_I2", "value": 1},
                {"name": "x_H1_mon_2_C2", "value": -1},
                {"name": "x_H1_mon_2_C3", "value": -1},

            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_mon_3_I1", "value": 1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_mon_3_I2", "value": 1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_tue_1_I1", "value": 1},
                {"name": "x_H1_tue_1_C1", "value": -1},
                {"name": "x_H1_tue_1_C2", "value": -1},

            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_tue_1_I2", "value": 1},
                {"name": "x_H1_tue_1_C2", "value": -1},
                {"name": "x_H1_tue_1_C3", "value": -1},

            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_tue_2_I1", "value": 1},
                {"name": "x_H1_tue_2_C1", "value": -1},
                {"name": "x_H1_tue_2_C2", "value": -1},

            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_tue_2_I2", "value": 1},
                {"name": "x_H1_tue_2_C2", "value": -1},
                {"name": "x_H1_tue_2_C3", "value": -1},

            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_tue_3_I1", "value": 1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "y_tue_3_I2", "value": 1},
            ],
            "constant": 0,
        },
    ]

    actual_constraints = [v.toDict() for v in model.problem.constraints.values()]

    assert len(expected_constraints) == len(actual_constraints), "数が合わない"

    for expected, actual in zip(expected_constraints, actual_constraints):
        assert expected["sense"] == actual["sense"]
        assert expected["constant"] == actual["constant"]

        expected_coefficients = expected["coefficients"]
        actual_coefficients = actual["coefficients"]

        assert len(expected_coefficients) == len(actual_coefficients)

        for e, a in zip(expected_coefficients, actual_coefficients):
            assert e["name"] == a["name"]
            assert e["value"] == a["value"]
