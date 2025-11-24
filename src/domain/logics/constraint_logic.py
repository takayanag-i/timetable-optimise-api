from domain.vo.annual_data import AnnualDataVo


def is_enrolled(data: AnnualDataVo, h: str, c: str) -> bool:
    """学級 h が講座 c を履修しているか"""
    return any(c in lane for block in data.curriculum_dict[h] for lane in block)


def get_enrolled_homeroom(data: AnnualDataVo, c: str) -> str:
    """講座 h を履修している学級を1つ取得する"""
    return min(
        (h for h in data.H
         if is_enrolled(data, h, c))
    )


def is_instructor_of_course(data: AnnualDataVo, i: str, c: str) -> bool:
    """教員 i が講座 c を担当しているか"""
    return any(i == detail.instructor_id for detail in data.course_details_dict[c])
