import pulp
from domain.constraints.instructor import InstructorConstraint


def test_instructor_constraint(mock_annual_model) -> None:
    """InstructorConstraintのapplyメソッドのテスト。"""
    constraint = InstructorConstraint()
    model = constraint.apply(mock_annual_model)

    expected_constraints = [
        {
            "coefficients": [{"name": "y_mon_1_I1", "value": 1}],
            "constant": 0,
            "sense": pulp.LpConstraintEQ,
        },
        {
            "coefficients": [{"name": "y_mon_1_I2", "value": 1}],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [{"name": "y_mon_2_I1", "value": 1}],
            "constant": 0,
            "sense": pulp.LpConstraintEQ,
        },
        {
            "coefficients": [{"name": "y_mon_2_I2", "value": 1}],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [{"name": "y_mon_3_I1", "value": 1}],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [{"name": "y_mon_3_I2", "value": 1}],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [{"name": "y_tue_1_I1", "value": 1}],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [{"name": "y_tue_1_I2", "value": 1}],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [{"name": "y_tue_2_I1", "value": 1}],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [{"name": "y_tue_2_I2", "value": 1}],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [{"name": "y_tue_3_I1", "value": 1}],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
        {
            "coefficients": [{"name": "y_tue_3_I2", "value": 1}],
            "constant": -1,
            "sense": pulp.LpConstraintLE,
        },
    ]

    actual_constraints = [v.toDict() for v in model.problem.constraints.values()]

    assert len(actual_constraints) == len(expected_constraints), "数が合わない"

    for expected, actual in zip(expected_constraints, actual_constraints):
        assert expected["sense"] == actual["sense"]
        assert expected["constant"] == actual["constant"]

        expected_coefficients = expected["coefficients"]
        actual_coefficients = actual["coefficients"]

        assert len(expected_coefficients) == len(actual_coefficients)

        for e, a in zip(expected_coefficients, actual_coefficients):
            assert e["name"] == a["name"]
            assert e["value"] == a["value"]
