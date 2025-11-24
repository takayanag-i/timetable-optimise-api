import pulp
from domain.constraints.course import CourseConstraint


def test_course_constraint(mock_annual_model):
    course_constraint = CourseConstraint()
    model = course_constraint.apply(mock_annual_model)

    expected_constraints = [
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_1_C1", "value": 1},
                {"name": "x_H2_mon_1_C1", "value": -1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_1_C1", "value": 1},
                {"name": "x_H3_mon_1_C1", "value": -1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_2_C1", "value": 1},
                {"name": "x_H2_mon_2_C1", "value": -1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_tue_1_C1", "value": 1},
                {"name": "x_H2_tue_1_C1", "value": -1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_tue_1_C1", "value": 1},
                {"name": "x_H3_tue_1_C1", "value": -1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_tue_2_C1", "value": 1},
                {"name": "x_H2_tue_2_C1", "value": -1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_1_C2", "value": 1},
                {"name": "x_H2_mon_1_C2", "value": -1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_2_C2", "value": 1},
                {"name": "x_H2_mon_2_C2", "value": -1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_tue_1_C2", "value": 1},
                {"name": "x_H2_tue_1_C2", "value": -1},
            ],
            "constant": 0,
        },
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_tue_2_C2", "value": 1},
                {"name": "x_H2_tue_2_C2", "value": -1},
            ],
            "constant": 0,
        },
    ]

    actual_constraints = [v.toDict() for v in model.problem.constraints.values()]

    assert len(actual_constraints) == 10, "数が合わない"

    for expected, actual in zip(expected_constraints, actual_constraints):
        assert expected["sense"] == actual["sense"]
        assert expected["constant"] == actual["constant"]

        expected_coefficients = expected["coefficients"]
        actual_coefficients = actual["coefficients"]

        assert len(expected_coefficients) == len(actual_coefficients)

        for e, a in zip(expected_coefficients, actual_coefficients):
            assert e["name"] == a["name"]
            assert e["value"] == a["value"]
