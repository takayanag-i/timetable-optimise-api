from typing import List
from application.factories.annual_data_factory import create_annual_data
from application.factories.annual_timetable_result_factory import create_timetable_entries, create_constraint_violations
from application.factories.constraint_definitions_factory import create_constraint_definitions
from application.models.dto import (
    AnnualTimetableResultDto, TimetableEntryDto,
    OptimiseAnnualTimetableDto, V1ConstraintViolationDto
)
from domain.services.annual_lp_service import AnnualLpService
from domain.vo.annual_data import AnnualDataVo
from domain.models.annual_lp_model import AnnualLpModel
from domain.vo.constraint_definition import ConstraintDefinitionVo
from infrastructure.solvers.gurobi_solver import GurobiSolver


class OptimiseAnnualTimetableUsecase:
    """年次時間割編成ユースケース"""

    def __init__(self, dto: OptimiseAnnualTimetableDto):
        """イニシャライザ。

        Args:
            dto (OptimiseAnnualTimetableDTO): 年次時間割編成DTO
        """
        self.dto = dto

    def execute(self) -> AnnualTimetableResultDto:
        """年次時間割編成を実行する。

        Returns:
            AnnualTimetableResult: 年次時間割編成結果
        """
        annual_data: AnnualDataVo = create_annual_data(self.dto.annual_data)
        constraint_definitions: List[ConstraintDefinitionVo] = create_constraint_definitions(
            self.dto.constraint_definitions
        )
        solver = GurobiSolver()  # todo ここで注入しますか？
        model = AnnualLpModel(annual_data, constraint_definitions, solver)

        AnnualLpService.solve(model)

        entries: List[TimetableEntryDto] = create_timetable_entries(model)
        violations: List[V1ConstraintViolationDto] = create_constraint_violations(model)

        return AnnualTimetableResultDto(
            entries=entries,
            violations=violations
        )
