# -------------------------------------------------------
# API에서 수집한 JSON 데이터를 분석하기 쉬운 형태로 가공하는 모듈입니다.
# 필요한 데이터만 추출하여 Pandas DataFrame으로 변환하고,
# CSV와 Parquet 형식으로 저장하는 기능을 제공합니다.
# -------------------------------------------------------


import pandas as pd

from schemas import validate_weather


# API JSON -> DataFrame 변환
def mak_dataframe(data):
    weather = data["weather"]
    ip = data["ip"]

    rows = []

    temperatures = weather["hourly"]["temperature_2m"]
    rain_probability = weather["hourly"]["precipitation_probability"]

    # 시간별 데이터 생성
    for temp, rain in zip(
        temperatures,
        rain_probability
    ):
        weather_data = {
            "temperature": temp,
            "precipitation_probability": rain
        }

        validated_weather = validate_weather(
            weather_data
        )

        if validated_weather is None:
            continue

        rows.append({
            "city": "Seoul",
            "temperature": validated_weather.temperature,
            "rain_probability": validated_weather.precipitation_probability,
            "country": "Korea",
            "ip_city": ip.get(
                "city",
                "unknown"
            )
        })

    return pd.DataFrame(rows)

# CSV / Parquet 저장
def save_files(df):
    df.to_csv("data/weather.csv", index=False)
    df.to_parquet("data/weather.parquet", index=False)