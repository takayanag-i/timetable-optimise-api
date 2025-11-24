from typing import List
from application.models.dto import ConstraintDefinitionDto
from domain.vo.constraint_definition import ConstraintDefinitionVo


def create_constraint_definitions(dtos: List[ConstraintDefinitionDto]) -> List[ConstraintDefinitionVo]:
    """
    制約定義DTOリストからドメイン用の制約定義リストを生成する。
    """
    return [
        ConstraintDefinitionVo(
            code=dto.constraint_definition_code,
            soft_flag=dto.soft_flag,
            penalty_weight=dto.penalty_weight,
            parameters={item.key: item.value for item in dto.parameters}
        ) for dto in dtos
    ]
