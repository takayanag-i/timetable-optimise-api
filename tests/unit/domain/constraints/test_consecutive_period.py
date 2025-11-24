import pulp
from domain.constraints.consecutive_period import ConsecutivePeriodConstraint


def test_consecutive_period(mock_annual_model):
    course_constraint = ConsecutivePeriodConstraint('C2')
    model = course_constraint.apply(mock_annual_model)

    expected_constraints = [
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "w_H1_mon_1_2_C2", "value": 1},
        #         {"name": "x_H1_mon_1_C2", "value": -1},
        #     ],
        #     "constant": 0,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "w_H1_mon_1_2_C2", "value": 1},
        #         {"name": "x_H1_mon_2_C2", "value": -1},
        #     ],
        #     "constant": 0,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "x_H1_mon_1_C2", "value": 1},
        #         {"name": "x_H1_mon_2_C2", "value": 1},
        #         {"name": "w_H1_mon_1_2_C2", "value": -1},
        #     ],
        #     "constant": -1,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "w_H1_tue_1_2_C2", "value": 1},
        #         {"name": "x_H1_tue_1_C2", "value": -1},
        #     ],
        #     "constant": 0,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "w_H1_tue_1_2_C2", "value": 1},
        #         {"name": "x_H1_tue_2_C2", "value": -1},
        #     ],
        #     "constant": 0,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "x_H1_tue_1_C2", "value": 1},
        #         {"name": "x_H1_tue_2_C2", "value": 1},
        #         {"name": "w_H1_tue_1_2_C2", "value": -1},
        #     ],
        #     "constant": -1,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "w_H2_mon_1_2_C2", "value": 1},
        #         {"name": "x_H2_mon_1_C2", "value": -1},
        #     ],
        #     "constant": 0,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "w_H2_mon_1_2_C2", "value": 1},
        #         {"name": "x_H2_mon_2_C2", "value": -1},
        #     ],
        #     "constant": 0,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "x_H2_mon_1_C2", "value": 1},
        #         {"name": "x_H2_mon_2_C2", "value": 1},
        #         {"name": "w_H2_mon_1_2_C2", "value": -1},
        #     ],
        #     "constant": -1,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "w_H2_mon_2_3_C2", "value": 1},
        #         {"name": "x_H2_mon_2_C2", "value": -1},
        #     ],
        #     "constant": 0,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "w_H2_mon_2_3_C2", "value": 1},
        #         {"name": "x_H2_mon_3_C2", "value": -1},
        #     ],
        #     "constant": 0,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "x_H2_mon_2_C2", "value": 1},
        #         {"name": "x_H2_mon_3_C2", "value": 1},
        #         {"name": "w_H2_mon_2_3_C2", "value": -1},
        #     ],
        #     "constant": -1,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "w_H2_tue_1_2_C2", "value": 1},
        #         {"name": "x_H2_tue_1_C2", "value": -1},
        #     ],
        #     "constant": 0,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "w_H2_tue_1_2_C2", "value": 1},
        #         {"name": "x_H2_tue_2_C2", "value": -1},
        #     ],
        #     "constant": 0,
        # },
        # {
        #     "sense": pulp.LpConstraintLE,
        #     "coefficients": [
        #         {"name": "x_H2_tue_1_C2", "value": 1},
        #         {"name": "x_H2_tue_2_C2", "value": 1},
        #         {"name": "w_H2_tue_1_2_C2", "value": -1},
        #     ],
        #     "constant": -1,
        # },
        {
            "sense": pulp.LpConstraintLE,
            "coefficients": [
                {"name": "x_H2_mon_1_C2", "value": 1},
                {"name": "x_H2_mon_2_C2", "value": 1},
                {"name": "x_H2_mon_3_C2", "value": 1},
            ],
            "constant": -2,
        },
        {
            "sense": pulp.LpConstraintEQ,  # 等号
            "coefficients": [
                {"name": "w_H1_mon_1_2_C2", "value": 1},
                {"name": "w_H1_tue_1_2_C2", "value": 1},
                {"name": "w_H2_mon_1_2_C2", "value": 1},
                {"name": "w_H2_mon_2_3_C2", "value": 1},
                {"name": "w_H2_tue_1_2_C2", "value": 1},
            ],
            "constant": -1,
        },
    ]

    actual_constraints = [v.toDict() for v in model.problem.constraints.values()]

    assert len(actual_constraints) == 2, "数が合わない"

    for expected, actual in zip(expected_constraints, actual_constraints):
        assert expected["sense"] == actual["sense"]
        assert expected["constant"] == actual["constant"]

        expected_coefficients = expected["coefficients"]
        actual_coefficients = actual["coefficients"]

        assert len(expected_coefficients) == len(actual_coefficients)

        for e, a in zip(expected_coefficients, actual_coefficients):
            assert e["name"] == a["name"]
            assert e["value"] == a["value"]
