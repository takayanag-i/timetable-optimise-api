import pandas as pd

from domain.vo.annual_data import AnnualDataVo
from domain.models.annual_lp_model import AnnualLpModel
from collections import defaultdict


def display_result_by_homeroom(model: AnnualLpModel, h: str) -> pd.DataFrame:
    result_df = pd.DataFrame(columns=[i for i in range(1, 8)], index=model.data.D)

    for d in model.data.D:
        for p in model.data.homeroom_day_dict[h][d]:
            # 複数の講座を一時的に保持するリスト
            courses_in_period = []
            for block in model.data.curriculum_dict[h]:
                for lane in block:
                    for c in lane:
                        if model.x[h, d, p, c].value() == 1:
                            courses_in_period.append(c)
            # 複数の講座がある場合、カンマ区切りで結合してDataFrameに格納
            if courses_in_period:
                result_df.at[d, p] = '/'.join(courses_in_period)

    return result_df


def display_result_all_homerooms(response_json: dict) -> pd.DataFrame:
    # entries を取り出す
    entries = response_json["data"]["optimiseAnnualTimetable"]["entries"]

    # ユニークな学級・曜日・時限を抽出して並び順を定義
    homerooms = sorted({e["homeroom"] for e in entries})
    days = ["mon", "tue", "wed", "thu", "fri"]
    periods = list(range(1, 8))

    # カラムを 'mon 1', 'mon 2', ..., 'fri 7' という形式で作成
    columns = [f"{day} {period}" for day in days for period in periods]

    # 空の DataFrame を作成
    timetable_df = pd.DataFrame(index=homerooms, columns=columns)

    # データを格納
    for entry in entries:
        h = entry["homeroom"]
        d = entry["day"]
        p = entry["period"]
        c = entry["course"]
        key = f"{d} {p}"
        if pd.isna(timetable_df.at[h, key]):
            timetable_df.at[h, key] = c
        else:
            timetable_df.at[h, key] += f"/{c}"

    return timetable_df


def display_result_all_teachers(
        annual_data: AnnualDataVo,
        response_json
) -> pd.DataFrame:

    entries = response_json["data"]["optimiseAnnualTimetable"]["entries"]

    periods = [f'{d} {p}' for d in annual_data.D for p in annual_data.P]
    instrutors = list(annual_data.I)

    timetable_df = pd.DataFrame(index=instrutors, columns=periods)
    for entry in entries:
        for detail in annual_data.course_details_dict[entry["course"]]:
            timetable_df.at[detail.instructor_id, f'{entry["day"]} {entry["period"]}'] = entry["course"]

    return timetable_df


def summarise_course_periods(response_json: dict) -> pd.DataFrame:
    entries = response_json["data"]["optimiseAnnualTimetable"]["entries"]

    # courseごとに開講情報を集める
    course_map = defaultdict(list)
    for e in entries:
        course = e["course"]
        info = f'{e["day"]} {e["period"]} ({e["homeroom"]})'
        course_map[course].append(info)

    # データフレームに整形
    df = pd.DataFrame([
        {"course": course, "periods": ", ".join(sorted(times))}
        for course, times in course_map.items()
    ])

    return df.sort_values("course").reset_index(drop=True)
