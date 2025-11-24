from typing import List
from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel
import pulp


class WofXDefinition(ConstraintApplierBase):
    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        constraints = [
            constraint
            for (h, d, p1, p2, c) in model.w.keys()
            for constraint in self._generate_double_consecutive_constraints(model, h, d, p1, p2, c)
        ]

        for constraint in constraints:
            model.problem += constraint
        return model

    def _generate_double_consecutive_constraints(
        self,
        model: AnnualLpModel,
        h: str,
        d: str,
        p1: int,
        p2: int,
        c: str
    ) -> List[pulp.LpConstraint]:
        """consecutive := min(x_{h,d,p1,c}, x_{h,d,p2,c})に相当する制約を生成する"""
        return [
            model.w[h, d, p1, p2, c] <= model.x[h, d, p1, c],
            model.w[h, d, p1, p2, c] <= model.x[h, d, p2, c],
            model.x[h, d, p1, c] + model.x[h, d, p2, c] - 1 <= model.w[h, d, p1, p2, c]
        ]
