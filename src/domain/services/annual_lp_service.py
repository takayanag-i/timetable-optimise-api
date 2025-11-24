from typing import List

import pulp
from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel
from domain.constraints._mapping import (
    CONSTRAINT_DEFINITIONS_BUILT_IN, CONSTRAINT_DEFINITIONS_MANDATORY, VARIABLE_DEFINITIONS
)
from domain.exceptions.exceptions import OptimizationError


class AnnualLpService:
    """modelオブジェクトに定義した最適化問題を解くサービスクラス"""

    @staticmethod
    def solve(model: AnnualLpModel) -> None:
        """最適化問題を解く。

        Args:
            model (AnnualLpModel): AnnualLpModelインスタンス
        """
        # modelオブジェクトに格納した制約を適用する
        appliers: List[ConstraintApplierBase] = [
            # 変数定義
            *(cls() for cls in VARIABLE_DEFINITIONS.values()),
            # 必須制約
            *(cls() for cls in CONSTRAINT_DEFINITIONS_MANDATORY.values()),
            # 組み込み制約
            *(CONSTRAINT_DEFINITIONS_BUILT_IN[c.code.upper()](**c.parameters)
              for c in model.constraint_definitions if not c.soft_flag),
        ]
        for applier in appliers:
            applier.apply(model)

        # 最適化問題を解く
        status = model.problem.solve()
        if status != pulp.LpStatusOptimal:
            raise OptimizationError(status)
