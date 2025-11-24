from typing import List
import pulp

from domain.vo.annual_data import AnnualDataVo
from domain.vo.constraint_definition import ConstraintDefinitionVo
from domain.interfaces.solver_interface import SolverInterface


class AnnualLpModel:
    """年次時間割のLPモデルクラス。

    ドメイン層でLPモデルとして必要な構造を保持する。
    """

    def __init__(
        self,
        annual_data: AnnualDataVo,
        constraint_definitions: List[ConstraintDefinitionVo],
        solver: SolverInterface
    ) -> None:
        """イニシャライザ。

        - 解変数、補助変数、ペナルティ変数を定義する。
        - 外部から注入されたソルバを指定する。

        Args:
            annual_data (AnnualData):
                年次データ。
            constraint_definitions (List[ConstraintDefinition]):
                制約定義リスト。
            solver (SolverInterface):
                ソルバーの実装。
        """

        self.data = annual_data
        self.constraint_definitions = constraint_definitions
        self.problem = pulp.LpProblem("sample", pulp.LpMinimize)

        self.problem.setSolver(solver.get_solver())
        self.define_variables()

    def define_variables(self) -> None:
        """変数を定義する。"""
        self.x = {
            (h, d, p, c): pulp.LpVariable(name=f"x_{h}_{d}_{p}_{c}", cat=pulp.LpBinary)
            for h in self.data.H
            for d in self.data.D
            for p in self.data.homeroom_day_dict[h][d]
            for b in self.data.curriculum_dict[h]
            for l in b
            for c in l
        }

        self.y = {
            (d, p, i): pulp.LpVariable(name=f"y_{d}_{p}_{i}", cat=pulp.LpBinary)
            for d in self.data.D
            for p in self.data.P
            for i in self.data.I
        }

        self.w = {
            (h, d, p1, p2, c): pulp.LpVariable(name=f"w_{h}_{d}_{p1}_{p2}_{c}", cat=pulp.LpBinary)
            for h in self.data.H
            for d in self.data.D
            for b in self.data.curriculum_dict[h]
            for l in b
            for c in l
            for p1, p2 in zip(self.data.homeroom_day_dict[h][d], self.data.homeroom_day_dict[h][d][1:])
            if all((h, d, p, c) in self.x for p in (p1, p2))
        }

        self.v1 = {
            c: pulp.LpVariable(name=f"v^1_{c}", cat=pulp.LpBinary)
            for c in self.data.C
        }

        self.v2 = {
            c: pulp.LpVariable(name=f"v^2_{c}", cat=pulp.LpBinary)
            for c in self.data.C
        }

        # self.v3 = {
        #     (d, i): pulp.LpVariable(name=f"v^3_{d}_{i}", cat=pulp.LpBinary)
        #     for d in self.data.D
        #     for i in self.data.I
        # }

        # self.v4 = {
        #     (d, p, i): pulp.LpVariable(name=f"v^4_{d}_{p}_{i}", cat=pulp.LpBinary)
        #     for d in self.data.D
        #     for p in self.data.P
        #     for i in self.data.I
        # }
