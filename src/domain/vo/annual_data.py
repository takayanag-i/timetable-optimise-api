from typing import List, Dict, Optional, TypeAlias
from pydantic import BaseModel, ConfigDict

# 型エイリアス
HomeroomId: TypeAlias = str
DayOfWeek: TypeAlias = str
Period: TypeAlias = int
CourseId: TypeAlias = str
InstructorId: TypeAlias = str
HomeroomDay: TypeAlias = Dict[DayOfWeek, List[Period]]
AttendanceDay: TypeAlias = Dict[DayOfWeek, List[Period]]
Lane: TypeAlias = List[CourseId]
Block: TypeAlias = List[Lane]
Curriculum: TypeAlias = List[Block]


class SchoolDayVo(BaseModel):
    """学校曜日"""
    am_periods: int
    pm_periods: int


class CourseDetailVo(BaseModel):
    """講座詳細"""
    instructor_id: InstructorId
    room_id: Optional[str] = None

    model_config = ConfigDict(frozen=True)


class AnnualDataVo(BaseModel):
    """年次データ。

    ドメイン層で、年次データをリスト・辞書として保持する。

    Attributes:
        H: 学級IDリスト
        D: 曜日リスト
        P: 時限リスト
        C: 講座IDリスト
        I: 教員IDリスト
        homeroom_day_dict: 学級ID -> 学級曜日
        curriculum_dict: 学級ID -> カリキュラム
        credit_dict: 講座ID -> 単位数
        course_details_dict: 講座ID -> 講座詳細リスト
        school_day_dict: 曜日 -> 学校曜日
        attendance_day_dict: 教員ID -> 勤怠曜日
    """
    H: List[HomeroomId]
    D: List[DayOfWeek]
    P: List[Period]
    C: List[CourseId]
    I: List[InstructorId]
    homeroom_day_dict: Dict[HomeroomId, HomeroomDay]
    curriculum_dict: Dict[HomeroomId, Curriculum]
    credit_dict: Dict[CourseId, int]
    course_details_dict: Dict[CourseId, List[CourseDetailVo]]
    school_day_dict: Dict[DayOfWeek, SchoolDayVo]
    attendance_day_dict: Dict[InstructorId, AttendanceDay]

    model_config = ConfigDict(frozen=True)
