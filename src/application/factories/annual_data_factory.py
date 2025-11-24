from typing import Dict, List
from application.models.dto import (
    CourseDto, CurriculumDto, HomeroomDto,
    InstructorDto, SchoolDayDto, AnnualDataDto
)
from domain.vo.annual_data import (
    AnnualDataVo, CourseDetailVo, SchoolDayVo,
    HomeroomId, DayOfWeek, Period, CourseId, InstructorId,
    HomeroomDay, AttendanceDay, Curriculum
)


def create_annual_data(dto: AnnualDataDto) -> AnnualDataVo:
    """
    年次データDTOからドメイン用の年次データを生成する。

    Args:
        dto (AnnualDataDTO): 年次データDTO

    Returns:
        AnnualData: 年次データ
    """
    return AnnualDataVo(
        H=_get_H(dto.homerooms),
        D=_get_D(dto.school_days),
        P=_get_P(dto.school_days),
        C=_get_C(dto.courses),
        I=_get_I(dto.instructors),
        homeroom_day_dict=_get_periods(dto.homerooms),
        curriculum_dict=_get_curriculums(dto.curriculums),
        credit_dict=_get_credits(dto.courses),
        course_details_dict=_get_course_details(dto.courses),
        school_day_dict=_get_school_days(dto.school_days),
        attendance_day_dict=_get_attendances(dto.instructors)
    )


def _get_D(school_days: List[SchoolDayDto]) -> List[DayOfWeek]:
    """学校曜日時限リストから曜日リストを取得する。"""
    return list(
        dict.fromkeys(
            school_day.day for school_day in school_days
            if school_day.available
        )
    )


def _get_P(school_days: List[SchoolDayDto]) -> List[Period]:
    """学校曜日時限リストから時限リストを取得する。"""
    return list(range(
        1,
        max(
            (school_day.am_periods + school_day.pm_periods)
            for school_day in school_days
            if school_day.available
        ) + 1
    ))


def _get_I(instructors: List[InstructorDto]) -> List[InstructorId]:
    """教員リストから教員IDリストを取得する。"""
    return list(
        dict.fromkeys(
            instructor.id for instructor in instructors
        )
    )


def _get_C(courses: List[CourseDto]) -> List[CourseId]:
    """講座リストから講座IDリストを取得する。"""
    return list(
        dict.fromkeys(
            course.id for course in courses
        )
    )


def _get_H(homerooms: List[HomeroomDto]) -> List[HomeroomId]:
    """学級リストから学級IDリストを取得する。"""
    return list(
        dict.fromkeys(
            homeroom.id for homeroom in homerooms
        )
    )


def _get_periods(homerooms: List[HomeroomDto]) -> Dict[HomeroomId, HomeroomDay]:
    """学級リストから{学級ID:時限リスト}辞書を取得する。"""
    return {
        homeroom.id: {
            day.day: list(range(1, day.periods + 1))
            for day in homeroom.days
        }
        for homeroom in homerooms
    }


def _get_curriculums(curriculums: List[CurriculumDto]) -> Dict[HomeroomId, Curriculum]:
    """カリキュラムリストからカリキュラム辞書を取得する。"""
    return {
        curriculum.homeroom_id: [
            [lane.course_ids for lane in block.lanes]
            for block in curriculum.blocks
        ]
        for curriculum in curriculums
    }


def _get_credits(courses: List[CourseDto]) -> Dict[CourseId, int]:
    """講座リストから{講座ID: 単位数}辞書を取得する。"""
    return {
        course.id: course.credits
        for course in courses
    }


def _get_course_details(courses: List[CourseDto]) -> Dict[CourseId, List[CourseDetailVo]]:
    """講座リストから{講座ID: 講座詳細}辞書を取得する。"""
    return {
        course.id: [CourseDetailVo(
            instructor_id=detail.instructor_id,
            room_id=detail.room_id) for detail in course.courseDetails]
        for course in courses
    }


def _get_school_days(school_days: List[SchoolDayDto]) -> Dict[DayOfWeek, SchoolDayVo]:
    """学校曜日DTOリストから{曜日: 学校曜日VO}辞書を取得する。"""
    return {
        school_day.day: SchoolDayVo(
            am_periods=school_day.am_periods,
            pm_periods=school_day.pm_periods
        )
        for school_day in school_days
        if school_day.available
    }


def _get_attendances(instructors: List[InstructorDto]) -> Dict[InstructorId, AttendanceDay]:
    """教員リストから{教員ID: 勤怠曜日}辞書を取得する。"""
    return {
        instructor.id: {
            day.day: day.unavailable_periods
            for day in instructor.days
        } for instructor in instructors
    }
