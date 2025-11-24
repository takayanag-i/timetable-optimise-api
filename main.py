from interface.routers.rest import router as rest_router
import uvicorn
import logging
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
