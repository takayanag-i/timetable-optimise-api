"""年次時間割編成MutationのAssembler"""

from interface.schemas.graphql_input import OptimiseAnnualTimetableInput
from application.models.dto import OptimiseAnnualTimetableDto


def to_dto(input: OptimiseAnnualTimetableInput) -> OptimiseAnnualTimetableDto:
    """
    年次時間割編成Mutation InputからDTOを生成する

    Args:
        input (OptimiseAnnualTimetableInput): Input

    Returns:
        OptimiseAnnualTimetableDto: DTO
    """
    return input.to_pydantic()
