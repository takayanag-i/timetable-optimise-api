import logging

from fastapi import APIRouter, Path, Body

from application.usecases.get_annual_data_usecase import AnnualDataService
from application.usecases.optimise_annual_timetable_usecase import OptimiseAnnualTimetableUsecase
from application.models.dto import OptimiseAnnualTimetableDto, AnnualTimetableResultDto

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/annual-data/{ttid}",
    tags=["annual-data"],
    summary="年次データ取得",
    description="指定されたTTIDに対応する年次データを取得します。",
    response_description="年次データ"
)
def get_annual_data(
    ttid: str = Path(..., description="時間割ID（TTID）", example="550e8400-e29b-41d4-a716-446655440000")
):
    """
    年次データを取得するエンドポイント
    
    - **ttid**: 時間割を一意に識別するID（UUID形式）
    
    取得されるデータ:
    - 学校曜日情報
    - 学級情報
    - 教員情報
    - 教室情報
    - 講座情報
    - カリキュラム情報
    """
    service = AnnualDataService(ttid)
    return service.get_annual_data()


@router.post(
    "/optimise-annual-timetable",
    response_model=AnnualTimetableResultDto,
    tags=["timetable"],
    summary="年次時間割最適化",
    description="年次データと制約定義を基に、最適な時間割を生成します。",
    response_description="最適化された時間割の結果"
)
def optimise_annual_timetable(
    input_data: OptimiseAnnualTimetableDto = Body(
        ...,
        description="年次時間割最適化リクエスト"
    )
) -> AnnualTimetableResultDto:
    """
    年次時間割編成エンドポイント
    
    ## 処理フロー
    1. 年次データと制約定義を受け取る
    2. 線形計画問題を構築
    3. Gurobi Optimizerで最適化を実行
    4. 最適な時間割エントリと制約違反を返却
    
    ## 入力データ
    - **ttid**: 時間割ID
    - **annualData**: 年次データ（学校曜日、学級、教員、教室、講座、カリキュラム）
    - **constraintDefinitions**: 制約定義リスト
    
    ## 出力データ
    - **entries**: 時間割エントリのリスト（学級ID、曜日、時限、講座ID）
    - **violations**: 制約違反のリスト
    
    ## 最適化について
    このエンドポイントは、与えられた制約の下で最適な時間割を生成します。
    すべてのハード制約は満たされ、ソフト制約は可能な限り満たされます。
    """
    # リクエストをログ出力
    logger.info(
        "POST /optimise-annual-timetable - Request received",
        extra={"request_body": input_data.model_dump()}
    )
    
    result = OptimiseAnnualTimetableUsecase(input_data).execute()
    return result
