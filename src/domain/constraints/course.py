from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel


class CourseConstraint(ConstraintApplierBase):
    """講座制約の制約定義クラス。"""

    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        constraints = [
            model.x[enrolled_homerooms[0], d, p, c] == model.x[enrolled_homeroom, d, p, c]
            for c in model.data.C
            for d in model.data.D
            for p in model.data.P
            if (
                #  cを受講しているhのリスト
                enrolled_homerooms := [
                    h for h in model.data.H
                    if (h, d, p, c) in model.x  # cがあるかと、d, pがあるかのチェック
                ]
            ) and len(enrolled_homerooms) > 1
            for enrolled_homeroom in enrolled_homerooms[1:]
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
