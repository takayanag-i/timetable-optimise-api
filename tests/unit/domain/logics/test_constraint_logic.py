import pytest

from domain.logics.constraint_logic import is_enrolled, get_enrolled_homeroom, is_instructor_of_course


@pytest.mark.usefixtures("mock_annual_data")
def test_is_enrolled_true(mock_annual_data):
    # H1はC1を履修している
    assert is_enrolled(mock_annual_data, "H1", "C1") is True


def test_is_enrolled_other_class(mock_annual_data):
    # H2はC2を履修している
    assert is_enrolled(mock_annual_data, "H2", "C2") is True


def test_is_enrolled_false(mock_annual_data):
    # H1は存在しない講座C3を履修していない
    assert is_enrolled(mock_annual_data, "H1", "C3") is False


def test_is_enrolled_not_enrolled(mock_annual_data):
    # H3はC2を履修していない
    assert is_enrolled(mock_annual_data, "H3", "C2") is False


def test_get_enrolled_homeroom_single(mock_annual_data):
    # C1を履修している学級のうち最小値（H1）が返る
    assert get_enrolled_homeroom(mock_annual_data, "C1") == "H1"


def test_get_enrolled_homeroom_multiple_classes(mock_annual_data):
    # C3を履修している学級のうち最小値（H2）が返る
    assert get_enrolled_homeroom(mock_annual_data, "C3") == "H2"


def test_is_instructor_of_course_true(mock_annual_data):
    # I1はC1の担当教員
    assert is_instructor_of_course(mock_annual_data, "I1", "C1") is True


def test_is_instructor_of_course_multiple_instructors(mock_annual_data):
    # I2はC2の担当教員の一人
    assert is_instructor_of_course(mock_annual_data, "I2", "C2") is True


def test_is_instructor_of_course_false(mock_annual_data):
    # I1はC3の担当教員ではない
    assert is_instructor_of_course(mock_annual_data, "I1", "C3") is False
