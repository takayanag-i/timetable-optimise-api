import pulp
from domain.logics.constraint_logic import get_enrolled_homeroom, is_instructor_of_course
from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel


class YofXDefinition(ConstraintApplierBase):
    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        constraints = [
            # cに関して和をとる
            model.y[d, p, i] == pulp.lpSum(
                model.x[h, d, p, c]
                for c in model.data.C
                if (h := get_enrolled_homeroom(model.data, c)) is not None
                and is_instructor_of_course(model.data, i, c)
                and (h, d, p, c) in model.x
            )

            # 任意のd, p, iに対して
            for d in model.data.D
            for p in model.data.P
            for i in model.data.I
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
