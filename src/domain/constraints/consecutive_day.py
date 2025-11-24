import logging
import pulp
from typing import List, override
from domain.logics.constraint_logic import get_enrolled_homeroom
from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel


class ConsecutiveDayConstraint(ConstraintApplierBase):
    """連続曜日制約の制約定義クラス。"""

    @override
    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        """LPモデルに制約を追加して返却する。"""
        logging.info("連続曜日制約の適用を開始します")

        def get_big_M() -> int:
            """Big-Mとして、1週あたりの授業日（月〜金）の数を取得する。"""
            return 5

        def get_patterns(c: str) -> List[List[str]]:
            """講座cの単位数に応じた連続曜日パターンを取得する。"""
            available_days = model.data.D
            patterns = []

            # 2単位の場合: 連続する2日のパターン
            for i in range(len(available_days) - 1):
                patterns.append([available_days[i], available_days[i + 1]])

            # 3単位の場合: 連続する3日のパターンも追加
            if model.data.credit_dict[c] >= 3:
                for i in range(len(available_days) - 2):
                    patterns.append([available_days[i], available_days[i + 1], available_days[i + 2]])

            return patterns

        constraints: List[pulp.LpConstraint] = [
            pulp.lpSum(
                model.x[h0, d, p, c]
                for d in pattern
                for p in model.data.homeroom_day_dict[h0][d]
            ) <= (len(pattern) - 1) + get_big_M() * model.v2[c]  # ペナルティ変数を追加
            for c in model.data.C
            if model.data.credit_dict[c] >= 2
            if (h0 := get_enrolled_homeroom(model.data, c)) is not None
            for pattern in get_patterns(c)
        ]

        for constraint in constraints:
            model.problem += constraint

        model.problem += (
            1 * pulp.lpSum(model.v2[c] for c in model.data.C)
        ), "V2"

        logging.info(f"連続曜日制約の適用を完了しました（制約数: {len(constraints)}）")
        return model
