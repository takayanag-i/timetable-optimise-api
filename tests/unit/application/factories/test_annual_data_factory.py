import pytest
from application.models.dto import (
    CourseDto, CourseDetailDto,
    BlockDto, CurriculumDto, LaneDto,
    HomeroomDto, HomeroomDayDto,
    InstructorDto, AttendanceDayDto,
    SchoolDayDto
)
from application.factories.annual_data_factory import (
    _get_C,
    _get_H,
    _get_P,
    _get_credits,
    _get_curriculums,
    _get_periods,
    _get_D,
    _get_course_details,
    _get_I,
    _get_attendances,
    _get_school_days,
)
from domain.vo.annual_data import CourseDetailVo, SchoolDayVo


@pytest.fixture
def sample_courses():
    return [
        CourseDto(
            id="math",
            credits=1,
            courseDetails=[
                CourseDetailDto(instructor_id="instructor1", room_id="room1"),
                CourseDetailDto(instructor_id="instructor2", room_id="room2")
            ]
        ),
        CourseDto(
            id="science",
            credits=2,
            courseDetails=[
                CourseDetailDto(instructor_id="instructor3", room_id="room3"),
                CourseDetailDto(instructor_id="instructor4", room_id="room4")
            ]
        )
    ]


@pytest.fixture
def sample_curriculums():
    return [
        CurriculumDto(
            homeroom_id="2-4",
            blocks=[
                BlockDto(
                    id="block1",
                    lanes=[
                        LaneDto(course_ids=["math", "science"]),
                        LaneDto(course_ids=["history", "english"])
                    ]
                ),
                BlockDto(
                    id="block2",
                    lanes=[
                        LaneDto(course_ids=["math", "science"]),
                        LaneDto(course_ids=["history", "english"])
                    ]
                )
            ]
        ),
        CurriculumDto(
            homeroom_id="2-5",
            blocks=[
                BlockDto(
                    id="block1",
                    lanes=[
                        LaneDto(course_ids=["math", "science"]),
                        LaneDto(course_ids=["history", "english"])
                    ]
                ),
                BlockDto(
                    id="block2",
                    lanes=[
                        LaneDto(course_ids=["math", "science"]),
                        LaneDto(course_ids=["history", "english"])
                    ]
                )
            ]
        )
    ]


@pytest.fixture
def sample_homerooms():
    return [
        HomeroomDto(id="2-4",
                    days=[
                        HomeroomDayDto(day="mon", periods=6),
                        HomeroomDayDto(day="tue", periods=7)
                    ]),
        HomeroomDto(id="2-5", days=[HomeroomDayDto(day="wed", periods=5)])
    ]


@pytest.fixture
def sample_instructors():
    return [
        InstructorDto(
            id="instructor1",
            days=[
                AttendanceDayDto(day="mon", unavailable_periods=[1, 2]),
                AttendanceDayDto(day="wed", unavailable_periods=[3])
            ]
        ),
        InstructorDto(
            id="instructor2",
            days=[AttendanceDayDto(day="tue", unavailable_periods=[4])]
        ),
        InstructorDto(
            id="instructor3",
            days=[AttendanceDayDto(day="wed", unavailable_periods=[5])]
        ),
        InstructorDto(
            id="instructor4",
            days=[AttendanceDayDto(day="thu", unavailable_periods=[6])]
        )
    ]


@pytest.fixture
def sample_days():
    return [
        SchoolDayDto(day="mon", available=True, am_periods=4, pm_periods=3),
        SchoolDayDto(day="tue", available=True, am_periods=4, pm_periods=3),
        SchoolDayDto(day="wed", available=True, am_periods=4, pm_periods=3),
        SchoolDayDto(day="sat", available=False)
    ]


@pytest.fixture
def sample_school_days():
    """テスト用の学校曜日データ"""
    return [
        SchoolDayDto(
            day="mon",
            am_periods=3,
            pm_periods=2,
            available=True
        ),
        SchoolDayDto(
            day="tue",
            am_periods=2,
            pm_periods=1,
            available=True
        ),
        SchoolDayDto(
            day="wed",
            am_periods=1,
            pm_periods=2,
            available=False  # 利用不可の日
        ),
        SchoolDayDto(
            day="thu",
            am_periods=2,
            pm_periods=2,
            available=True
        )
    ]


def test_get_H(sample_homerooms):
    result = _get_H(sample_homerooms)
    assert result == ["2-4", "2-5"]


def test_get_D(sample_days):
    result = _get_D(sample_days)
    assert result == ["mon", "tue", "wed"]


def test_get_P(sample_days):
    result = _get_P(sample_days)
    assert result == [1, 2, 3, 4, 5, 6, 7]


def test_get_C(sample_courses):
    result = _get_C(sample_courses)
    assert result == ['math', 'science']


def test_get_I(sample_instructors):
    result = _get_I(sample_instructors)
    assert result == ["instructor1", "instructor2", "instructor3", "instructor4"]


def test_get_Phd(sample_homerooms):

    result = _get_periods(sample_homerooms)
    assert result == {
        "2-4": {
            "mon": [1, 2, 3, 4, 5, 6],
            "tue": [1, 2, 3, 4, 5, 6, 7]
        },
        "2-5": {
            "wed": [1, 2, 3, 4, 5]
        }
    }


def test_get_Bh(sample_curriculums):
    result = _get_curriculums(sample_curriculums)
    assert result == {
        "2-4": [
            [["math", "science"], ["history", "english"]],
            [["math", "science"], ["history", "english"]]
        ],
        "2-5": [
            [["math", "science"], ["history", "english"]],
            [["math", "science"], ["history", "english"]]
        ]
    }


def test_get_credits(sample_courses):
    result = _get_credits(sample_courses)
    assert result == {
        'math': 1,
        'science': 2
    }


def test_get_course_details(sample_courses):
    result = _get_course_details(sample_courses)
    assert result == {
        'math': [
            CourseDetailVo(instructor_id="instructor1", room_id="room1"),
            CourseDetailVo(instructor_id="instructor2", room_id="room2")
        ],
        'science': [
            CourseDetailVo(instructor_id="instructor3", room_id="room3"),
            CourseDetailVo(instructor_id="instructor4", room_id="room4")
        ]
    }


def test_get_attendances(sample_instructors):
    result = _get_attendances(sample_instructors)
    assert result == {
        "instructor1": {"mon": [1, 2], "wed": [3]},
        "instructor2": {"tue": [4]},
        "instructor3": {"wed": [5]},
        "instructor4": {"thu": [6]}
    }


def test_get_school_days(sample_school_days):
    """_get_school_days関数のテスト"""
    result = _get_school_days(sample_school_days)

    # available=Trueの曜日のみが含まれることを確認
    expected = {
        "mon": SchoolDayVo(am_periods=3, pm_periods=2),
        "tue": SchoolDayVo(am_periods=2, pm_periods=1),
        "thu": SchoolDayVo(am_periods=2, pm_periods=2)
        # "wed"は available=False なので含まれない
    }

    assert result == expected
    assert len(result) == 3  # available=Trueの曜日のみ3つ
    assert "wed" not in result  # available=Falseの曜日は含まれない

    # 各SchoolDayVoの値を個別に検証
    assert result["mon"].am_periods == 3
    assert result["mon"].pm_periods == 2
    assert result["tue"].am_periods == 2
    assert result["tue"].pm_periods == 1
    assert result["thu"].am_periods == 2
    assert result["thu"].pm_periods == 2
