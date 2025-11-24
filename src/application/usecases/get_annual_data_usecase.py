import json

from application.models.dto import AnnualDataDto
from application.factories.annual_data_factory import create_annual_data


class AnnualDataService:
    def __init__(self, ttid: str):
        self.str = str

    def get_annual_data(self):
        """年次データを取得する

        STUB

        Returns:
            AnnualDataDTO: 年次データ
        """

        with open("/workspaces/timetable/fastapi/tests/resources/sample04/all.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)["annualData"]
        dto = AnnualDataDto(
            courses=json_data["courses"],
            curriculums=json_data["curriculums"],
            homerooms=json_data["homerooms"],
            instructors=json_data["instructors"],
            rooms=json_data["rooms"],
            school_days=json_data["schoolDays"]
        )
        return create_annual_data(dto)
