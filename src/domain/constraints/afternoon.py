from typing import List, override
from domain.logics.constraint_logic import is_enrolled
from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel
import pulp


class AfternoonConstraint(ConstraintApplierBase):
    """午前午後制約の制約定義クラス。"""

    @override
    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        """LPモデルに制約を追加して返却する。"""

        def get_capability_in_afternoon(c: str) -> int:
            """講座cの、午後に配置可能なコマ数を取得する。"""
            return max(model.data.credit_dict[c] - 1, 1)

        def get_big_M(c: str) -> int:
            """Big-Mとして、講座cがすべて午後に配置される場合の、午後の開講コマ数（単位数に一致）を取得する。"""

            return model.data.credit_dict[c]

        def get_h0(c: str) -> str:  # todo: ドメインロジック切り出し→マッピング
            """講座cを履修する学級を1つ取得する。"""
            return next(
                (h for h in model.data.H if is_enrolled(model.data, h, c)), None
            )

        def get_first_pm_period(d: str) -> int:
            """午後の先頭時限を取得する。"""
            return model.data.school_day_dict[d].am_periods + 1

        constraints: List[pulp.LpConstraint] = [
            pulp.lpSum(terms) <= get_capability_in_afternoon(c) + get_big_M(c) * model.v1[c]
            for c in model.data.C
            if (h0 := get_h0(c)) is not None
            if (terms := [
                model.x[h0, d, p, c]
                for d in model.data.D
                for p in model.data.homeroom_day_dict[h0][d]
                if p >= get_first_pm_period(d)
            ])
        ]

        for constraint in constraints:
            model.problem += constraint

        model.problem += (
            1 * pulp.lpSum(model.v1[c] for c in model.data.C)
        ), "V1"

        return model
