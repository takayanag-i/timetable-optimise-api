from typing import Set

from domain.logics.constraint_logic import get_enrolled_homeroom
from domain.constraints._base import ConstraintApplierBase
from domain.models.annual_lp_model import AnnualLpModel
import pulp


class CoursesPerDayConstraint(ConstraintApplierBase):
    """同日開講制約の制約定義クラス。

    各講座について、1日あたりの開講数を制限する。
    連続時限（講座）制約が設定されている講座は、同日2コマ開講を許可する。
    """

    def __init__(self, **kwargs):
        # パラメータは使用しない（後方互換性のためkwargsを受け取る）
        pass

    def apply(self, model: AnnualLpModel) -> AnnualLpModel:
        # 連続時限制約が設定されている講座IDを抽出
        twice_course_set = self._extract_consecutive_period_courses(model)

        constraints = [
            pulp.lpSum(
                model.x[h, d, p, c] for p in model.data.homeroom_day_dict[h][d]
            ) <= self._get_max(c, twice_course_set)
            for c in model.data.C
            if (h := get_enrolled_homeroom(model.data, c)) is not None
            for d in model.data.homeroom_day_dict[h]
        ]

        for constraint in constraints:
            model.problem += constraint

        return model

    def _extract_consecutive_period_courses(self, model: AnnualLpModel) -> Set[str]:
        """連続時限（講座）制約から講座IDを抽出する。

        Args:
            model: AnnualLpModelインスタンス

        Returns:
            連続時限制約が適用されている講座IDのセット
        """
        course_ids: Set[str] = set()
        for cd in model.constraint_definitions:
            if cd.code.upper() == "CONSECUTIVE_PERIOD" and cd.parameters:
                course_id = cd.parameters.get("courseId") or cd.parameters.get("course")
                if course_id:
                    course_ids.add(course_id)
        return course_ids

    def _get_max(self, course: str, twice_course_set: Set[str]) -> int:
        """講座の1日あたりの最大開講数を返す。

        Args:
            course: 講座ID
            twice_course_set: 2コマ開講を許可する講座IDのセット

        Returns:
            最大開講数（1 or 2）
        """
        return 2 if course in twice_course_set else 1
