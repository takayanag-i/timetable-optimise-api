from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel
import pulp


class HomeroomConstraint(ConstraintApplierBase):
    """学級制約の制約定義クラス。"""

    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        """LPモデルに制約を追加して返却する"""
        constraints = [
            pulp.lpSum(
                [
                    model.x[h, d, p, c]
                    for block in model.data.curriculum_dict[h]
                    for lane in block
                    for c in lane
                ]
            ) >= 1
            for h in model.data.H
            for d in model.data.D
            for p in model.data.homeroom_day_dict[h][d]
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
