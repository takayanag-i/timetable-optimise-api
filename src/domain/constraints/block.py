from typing import List, override
from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel
import pulp


class BlockConstraint(ConstraintApplierBase):
    """ブロック制約の制約定義クラス。"""

    @override
    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        """LPモデルに制約を追加して返却する"""
        constraints: List[pulp.LpConstraint] = [
            lane_sums[0] == lane_sum
            for h in model.data.H
            for d in model.data.D
            for p in model.data.homeroom_day_dict[h][d]
            for block in model.data.curriculum_dict[h]
            if len(block) > 1
            and (
                lane_sums := [
                    pulp.lpSum([model.x[h, d, p, c] for c in lane])
                    for lane in block
                ]
            )
            for lane_sum in lane_sums[1:]
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
