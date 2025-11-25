from domain.constraints.afternoon import AfternoonConstraint
from domain.constraints.credit import CreditConstraint
from domain.constraints.homeroom import HomeroomConstraint
from domain.constraints.course import CourseConstraint
from domain.constraints.block import BlockConstraint
from domain.constraints.instructor import InstructorConstraint
from domain.constraints.consecutive_period import ConsecutivePeriodConstraint
from domain.constraints.courses_per_day import CoursesPerDayConstraint
from domain.constraints.specific_day_period import SpecificDayPeriodConstraint
from domain.constraints.w_of_x_definition import WofXDefinition
from domain.constraints.y_of_x_definition import YofXDefinition
# from domain.constraints.specific_day_period import SpecificDayPeriodConstraint
# from domain.constraints.moving_classroom import MovingClassroomConstraint
from domain.constraints.consecutive_day import ConsecutiveDayConstraint
from domain.constraints.courses_per_day_instructor import CoursesPerDayInstructorConstraint
from domain.constraints.consecutive_period_instructor import ConsecutivePeriodInstructorConstraint

###
# 状況：移動教室関係は実装できていない。ソフト制約をソフトにしない設定はできていない。同日開講許可は組み込んでいない。
###


# 変数定義
VARIABLE_DEFINITIONS = {
    "W_OF_X": WofXDefinition,
    "Y_OF_X": YofXDefinition,
    # "Z_OF_X": ZofXDefinition,
}

# 必須制約
CONSTRAINT_DEFINITIONS_MANDATORY = {
    "HOMEROOM": HomeroomConstraint,  # 学級制約
    "COURSE": CourseConstraint,  # 講座制約
    "CREDIT": CreditConstraint,  # 単位数制約
    "BLOCK": BlockConstraint,  # ブロック制約
    "INSTRUCTOR": InstructorConstraint,  # 教員制約
}

# 組み込み制約
CONSTRAINT_DEFINITIONS_BUILT_IN = {
    "CONSECUTIVE_PERIOD": ConsecutivePeriodConstraint,  # ２コマ連続開講
    "COURSES_PER_DAY": CoursesPerDayConstraint,  # 同日開講
    "AFTERNOON": AfternoonConstraint,  # 午前午後制約
    "CONSECUTIVE_DAY": ConsecutiveDayConstraint,  # 連続曜日制約
    "TEACHER_DAILY_LESSONS": CoursesPerDayInstructorConstraint,  # 教員の1日あたりのコマ数 → レビュー必要
    "TEACHER_CONSECUTIVE_LESSONS": ConsecutivePeriodInstructorConstraint,  # 教員の連続コマ数 → レビュー必要
    "SPECIFIC_DAY_PERIOD": SpecificDayPeriodConstraint,  # 曜日時限指定 → レビュー必要
}
