"""
年次時間割編成結果のファクトリ

ドメインデータ（年次LPモデル）-> Pydanticモデル（年次時間割編成結果）変換のための関数群
"""

from typing import List
from common.constants import BINARY_ONE
from application.models.dto import (
    ConstraintViolationDto,
    V1ConstraintViolationDto,
    V2ConstraintViolationDto,
    V3ConstraintViolationDto,
    V4ConstraintViolationDto,
    TimetableEntryDto
)
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
    violations: List[ConstraintViolationDto] = []

    # V1: 午前午後制約違反（講座IDのリスト）
    v1_keys = [
        c for c in model.data.C
        if hasattr(model, 'v1') and c in model.v1 and model.v1[c].value() == BINARY_ONE
    ]
    if v1_keys:
        violations.append(V1ConstraintViolationDto(violation_keys=v1_keys))

    # V2: 連続曜日制約違反（講座IDのリスト）
    v2_keys = [
        c for c in model.data.C
        if hasattr(model, 'v2') and c in model.v2 and model.v2[c].value() == BINARY_ONE
    ]
    if v2_keys:
        violations.append(V2ConstraintViolationDto(violation_keys=v2_keys))

    # V3: 教員コマ数（１日）制約違反（(曜日, 教員ID)のタプルのリスト）
    v3_keys = []
    if hasattr(model, 'v3'):
        v3_keys = [
            (d, i) for d in model.data.D
            for i in model.data.I
            if (d, i) in model.v3 and model.v3[d, i].value() == BINARY_ONE
        ]
    if v3_keys:
        violations.append(V3ConstraintViolationDto(violation_keys=v3_keys))

    # V4: 教員連続コマ数制約違反（(曜日, 時限, 教員ID)のタプルのリスト）
    v4_keys = []
    if hasattr(model, 'v4'):
        v4_keys = [
            (d, p, i) for d in model.data.D
            for p in model.data.P
            for i in model.data.I
            if (d, p, i) in model.v4 and model.v4[d, p, i].value() == BINARY_ONE
        ]
    if v4_keys:
        violations.append(V4ConstraintViolationDto(violation_keys=v4_keys))

    return violations
