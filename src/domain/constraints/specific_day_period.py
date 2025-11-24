from typing import Dict, List
from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel


class SpecificDayPeriodConstraint(ConstraintApplierBase):
    """曜日時限指定制約

    開講曜日時限を指定する（先入れ）。

    システム表現: 指定された学級・講座・曜日・時限の`解バイナリ`を1に固定する。
    """

    def __init__(self, fixed_assignments: List[Dict[str, str]]):
        """
        Args:
            fixed_assignments: 固定する割り当てのリスト
                各辞書は {"homeroom": "H1", "course": "C1", "day": "mon", "period": 1} の形式
        """
        self.fixed_assignments = fixed_assignments

    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        """LPモデルに制約を追加して返却する"""
        constraints = []

        for assignment in self.fixed_assignments:
            h = assignment.get("homeroom")
            c = assignment.get("course")
            d = assignment.get("day")
            p = assignment.get("period")

            # 必要なキーが全て存在し、変数も存在する場合のみ制約を追加
            if all(key in assignment for key in ["homeroom", "course", "day", "period"]):
                if isinstance(p, str):
                    try:
                        p = int(p)  # 文字列の場合は整数に変換
                    except ValueError:
                        continue  # 変換できない場合はスキップ

                if (h, d, p, c) in model.x:
                    # 指定された割り当てを固定（x[h, d, p, c] = 1）
                    constraint = model.x[h, d, p, c] == 1
                    constraints.append(constraint)

        for constraint in constraints:
            model.problem += constraint

        return model
