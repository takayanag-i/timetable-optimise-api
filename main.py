from interface.routers.rest import router as rest_router
import uvicorn
import logging
from fastapi import FastAPI
from pythonjsonlogger import jsonlogger


def setup_logging():
    """JSON形式の構造化ログを設定"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 既存のハンドラーをクリア
    logger.handlers.clear()

    # JSON形式のフォーマッター
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        rename_fields={"asctime": "timestamp", "levelname": "level"},
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


setup_logging()

app = FastAPI(
    title="時間割最適化API",
    description="""
    ## 概要
    時間割編成を最適化するためのREST APIです。
    
    ## 機能
    - 年次データの取得
    - 年次時間割の最適化実行
    
    ## データモデル
    すべてのエンティティはIDベースで管理されています。
    
    - **学級 (Homeroom)**: 学級ID + 名称
    - **教員 (Instructor)**: 教員ID + 名称
    - **教室 (Room)**: 教室ID + 名称
    - **講座 (Course)**: 講座ID + 名称
    - **ブロック (Block)**: ブロックID + 名称
    
    ## 最適化エンジン
    Gurobi Optimizerを使用して線形計画問題を解きます。
    """,
    version="1.0.0",
    contact={
        "name": "Timetable API Support",
    },
    license_info={
        "name": "MIT",
    },
)

app.include_router(rest_router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run(app)
