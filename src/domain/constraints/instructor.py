from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel


class InstructorConstraint(ConstraintApplierBase):
    """教員制約の制約定義クラス。"""

    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        def is_available(d, p, i) -> bool:
            instructor_days = model.data.attendance_day_dict.get(i, {})
            unavailable_periods = instructor_days.get(d, [])
            return p not in unavailable_periods

        constraints = [
            (model.y[d, p, i] <= 1) if is_available(d, p, i)
            else (model.y[d, p, i] == 0)
            for d in model.data.D
            for p in model.data.P
            for i in model.data.I
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
