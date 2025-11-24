from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel
import pulp


class CreditConstraint(ConstraintApplierBase):
    """単位数制約の制約定義クラス。"""

    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        constraints = [
            pulp.lpSum(
                [model.x[h, d, p, c] for d in model.data.D for p in model.data.homeroom_day_dict[h][d]]
            ) == model.data.credit_dict[c]
            for h in model.data.H
            for block in model.data.curriculum_dict[h]
            for lane in block
            for c in lane
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
