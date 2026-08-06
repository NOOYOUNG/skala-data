# ----------------------------------------
#               asyncio + httpx
#                     |
#                     ↓
#           ┌────────────────────┐
#           │  API 3개 동시 호출    │
#           └────────────────────┘
#           ↓          ↓          ↓
#      Open-Meteo  Countries   ip-api
#           ↓          ↓          ↓
#               JSON 응답
#                     |
#                     ↓
#           Pydantic v2 검증
#                     |
#                     ↓
#         ┌─────────────────┐
#         │ 정상 데이터만 저장   │
#         └─────────────────┘
#              ↓       ↓
#            CSV    Parquet
#              ↓       ↓
#             속도 비교 측정
#                     |
#                     ↓
#         pytest + ruff + git commit
# ----------------------------------------


import asyncio

from benchmark import measure
from collector import collect_data
from processor import mak_dataframe, save_files


async def main():
    print("API 수집 시작")
    data = await collect_data()
    print("수집 완료")

    df = mak_dataframe(data)
    print(df.head())

    save_files(df)
    print("파일 저장 완료")

    measure()

if __name__ == "__main__":
    asyncio.run(main())