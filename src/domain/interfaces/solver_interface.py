from abc import ABC, abstractmethod
from typing import Any


class SolverInterface(ABC):
    """ソルバーのインターフェース。"""

    @abstractmethod
    def get_solver(self) -> Any:
        """ソルバーインスタンスを取得する。

        Returns:
            Any: PuLPのソルバーインスタンス
        """
        pass
