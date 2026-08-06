# ----------------------------------------------------------------------------
# 외부 API(Open-Meteo, Countries.dev, ip-api)에서 데이터를 비동기로 수집하는 모듈입니다.
# httpx의 AsyncClient와 asyncio.gather()를 사용하여 세 개의 API를 동시에 호출하고,
# 응답받은 JSON 데이터를 하나의 딕셔너리 형태로 반환합니다.
# ----------------------------------------------------------------------------


import asyncio

import httpx

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=37.5665"
    "&longitude=126.9780"
    "&hourly=temperature_2m,precipitation_probability"
    "&forecast_days=3"
    "&timezone=Asia/Seoul"
)

COUNTRY_URL = ( "https://countries.dev/alpha/KOR" )

IP_URL = ( "http://ip-api.com/json/8.8.8.8" )

# 공통 HTTP GET 함수
async def fetch(client, url):
    response = await client.get(url)
    response.raise_for_status()
    return response.json()

# asyncio.gather()을 이용한 API 병렬 수집
async def collect_data():
    async with httpx.AsyncClient() as client:
        weather, country, ip = await asyncio.gather(
            fetch(client, WEATHER_URL),
            fetch(client, COUNTRY_URL),
            fetch(client, IP_URL)
        )

    return {
        "weather": weather,
        "country": country,
        "ip": ip
    }

if __name__ == "__main__":
    result = asyncio.run(collect_data())
    print(result)