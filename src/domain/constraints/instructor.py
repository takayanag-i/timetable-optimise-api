from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel


class InstructorConstraint(ConstraintApplierBase):
    """教員制約の制約定義クラス。"""

    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        def is_available(d, p, i) -> bool:
            return p not in model.data.attendance_day_dict[i][d]

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
