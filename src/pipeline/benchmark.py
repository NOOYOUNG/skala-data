# ---------------------------------------------------
# CSV와 Parquet 파일의 읽기 성능을 비교하는 모듈입니다.
# 각 파일의 읽기 시간을 측정하여 출력하며,
# 파일 형식에 따른 성능 차이를 확인하기 위해 사용합니다.
# ---------------------------------------------------


import time

import pandas as pd


def measure():
    result = {}
    start = time.time()

    pd.read_csv("data/weather.csv")

    result["csv_read"] = (
        time.time() - start
    )

    start = time.time()

    pd.read_parquet("data/weather.parquet")

    result["parquet_read"] = (
        time.time() - start
    )

    print("CSV 읽기 : ", result["csv_read"])
    print("Parquet 읽기 : ", result["parquet_read"])

    return result

if __name__ == "__main__":
    measure()
