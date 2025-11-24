import os
from typing import Any
import pulp
from dotenv import load_dotenv

from domain.interfaces.solver_interface import SolverInterface

load_dotenv()


class CbcSolver(SolverInterface):
    """CBCソルバーの実装。

    infrastructure層でCBCの具体的な設定と初期化を行う。
    """

    def __init__(self, time_limit: int = 1200):
        """イニシャライザ。

        Args:
            time_limit (int): ソルバーのタイムリミット（秒）
        """
        self.cbc_path = os.getenv("CBC_PATH")
        self.time_limit = time_limit

    def get_solver(self) -> Any:
        """CBCソルバーインスタンスを取得する。

        Returns:
            pulp.COIN_CMD: CBCソルバーインスタンス
        """
        return pulp.COIN_CMD(timeLimit=self.time_limit, path=self.cbc_path)
