from typing import List, override
from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel
import pulp


class CoursesPerDayInstructorConstraint(ConstraintApplierBase):
    """教員の1日あたりのコマ数制約

    教員の1日あたりの担当コマ数が、設定した上限値以下である。
    """

    def __init__(self, max_daily_lessons: int = 4):
        """
        Args:
            max_daily_lessons: 教員の1日あたりの最大担当コマ数
        """
        self.max_daily_lessons = max_daily_lessons

    @override
    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        """LPモデルに制約を追加して返却する"""

        def get_big_M() -> int:
            """Big-M値として、教員が1日に担当可能な最大コマ数を取得"""
            return max(len(periods) for h in model.data.H for d in model.data.D
                       for periods in [model.data.homeroom_day_dict[h][d]])

        big_M = get_big_M()

        constraints: List[pulp.LpConstraint] = [
            pulp.lpSum(model.y[d, p, i] for p in model.data.P)
            <= self.max_daily_lessons + big_M * model.v3[d, i]
            for d in model.data.D
            for i in model.data.I
        ]

        for constraint in constraints:
            model.problem += constraint

        # ペナルティをコストに追加
        model.problem += (
            1 * pulp.lpSum(model.v3[d, i] for d in model.data.D for i in model.data.I)
        ), "V3"

        return model

