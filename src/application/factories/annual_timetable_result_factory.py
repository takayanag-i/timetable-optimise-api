"""
年次時間割編成結果のファクトリ

ドメインデータ（年次LPモデル）-> Pydanticモデル（年次時間割編成結果）変換のための関数群
"""

from typing import List
from common.constants import BINARY_ONE
from application.models.dto import ConstraintViolationDto, V1ConstraintViolationDto, TimetableEntryDto
from domain.models.annual_lp_model import AnnualLpModel


def create_timetable_entries(model: AnnualLpModel) -> List[TimetableEntryDto]:
    """
    時間割エントリのリストを生成する

    Args:
        model (AnnualLpModel): 年次LPモデル

    Returns:
        List[TimetableEntry]: 時間割エントリのリスト
    """
    return [
        TimetableEntryDto(
            homeroom=h,
            day=d,
            period=p,
            course=c
        )
        for h in model.data.H
        for d in model.data.D
        for p in model.data.homeroom_day_dict[h][d]
        for b in model.data.curriculum_dict[h]
        for l in b
        for c in l
        if model.x[h, d, p, c].value() == 1
    ]


def create_constraint_violations(model: AnnualLpModel) -> List[ConstraintViolationDto]:
    """
    制約違反のリストを生成する

    Args:
        model (AnnualLpModel): 年次LPモデル

    Returns:
        List[ConstraintViolation]: 制約違反
    """
    return [
        V1ConstraintViolationDto(
            violation_code="v1",
            violation_keys=[
                c for c in model.data.C
                if model.v1[c].value() == BINARY_ONE
            ]
        ),
    ]
