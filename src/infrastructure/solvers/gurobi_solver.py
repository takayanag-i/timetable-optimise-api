import os
from typing import Any
import pulp
from dotenv import load_dotenv

from domain.interfaces.solver_interface import SolverInterface

load_dotenv()


class GurobiSolver(SolverInterface):
    """Gurobiソルバーの実装。

    infrastructure層でGurobiの具体的な設定と初期化を行う。
    """

    def __init__(self):
        """イニシャライザ。

        環境変数からGurobiのライセンス情報を読み込む。
        """
        self.options = {
            "WLSACCESSID": os.getenv("WLSACCESSID"),
            "WLSSECRET": os.getenv("WLSSECRET"),
            "LICENSEID": int(os.getenv("LICENSEID")) if os.getenv("LICENSEID") else None,
        }

        # Noneの値は除外
        self.options = {k: v for k, v in self.options.items() if v is not None}

    def get_solver(self) -> Any:
        """Gurobiソルバーインスタンスを取得する。

        Returns:
            pulp.GUROBI: Gurobiソルバーインスタンス
        """
        return pulp.GUROBI(manageEnv=True, envOptions=self.options)
