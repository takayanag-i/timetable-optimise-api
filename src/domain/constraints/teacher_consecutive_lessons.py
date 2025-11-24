from typing import List, override
from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel
import pulp


class TeacherConsecutiveLessonsConstraint(ConstraintApplierBase):
    """教員の連続コマ数制約

    教員が連続して授業を担当するコマ数が、設定した上限値以下である。
    """

    def __init__(self, max_consecutive_lessons: int = 3):
        """
        Args:
            max_consecutive_lessons: 教員の連続担当コマ数の上限
        """
        self.max_consecutive_lessons = max_consecutive_lessons

    @override
    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        """LPモデルに制約を追加して返却する"""

        def get_big_M() -> int:
            """Big-M値として、1日の最大時限数を取得"""
            return max(len(periods) for h in model.data.H for d in model.data.D
                       for periods in [model.data.homeroom_day_dict[h][d]])

        big_M = get_big_M()

        constraints: List[pulp.LpConstraint] = []

        # 各教員、各曜日、各時限から始まる連続コマ数をチェック
        for d in model.data.D:
            for i in model.data.I:
                for start_p in model.data.P:
                    # start_p から始まる連続コマ数を計算
                    consecutive_periods = []
                    for offset in range(self.max_consecutive_lessons + 1):
                        check_p = start_p + offset
                        if check_p in model.data.P:
                            consecutive_periods.append(check_p)
                        else:
                            break

                    # max_consecutive_lessons + 1 個の連続する時限がある場合のみ制約を追加
                    if len(consecutive_periods) >= self.max_consecutive_lessons + 1:
                        constraint = (
                            pulp.lpSum(model.y[d, p, i] for p in consecutive_periods)
                            <= self.max_consecutive_lessons + big_M * model.v4[d, start_p, i]
                        )
                        constraints.append(constraint)

        for constraint in constraints:
            model.problem += constraint

        # ペナルティをコストに追加
        model.problem += (
            1 * pulp.lpSum(model.v4[d, p, i] for d in model.data.D for p in model.data.P for i in model.data.I)
        ), "V4"

        return model
