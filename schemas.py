# -------------------------------------------------------
# Pydantic v2 모델을 정의하는 모듈입니다.
# 외부 API(Open-Meteo, Countries.dev, ip-api)에서
# 수집한 데이터 중 필요한 필드를 추출하여 타입과 값의 범위를 검증합니다.
#
# 검증 조건을 만족하지 않는 데이터가 입력되면
# Pydantic ValidationError를 발생시켜
# 잘못된 데이터가 저장되는 것을 방지하고 데이터의 무결성을 보장합니다.
# -------------------------------------------------------


from pydantic import BaseModel, Field, ValidationError


# Open-Meteo API의 날씨 데이터를 검증하는 모델
# temperature: 섭씨 온도이며 일반적인 기온 범위 (-100 ~ 100) 내의 실수인지 검증합니다.
# precipitation_probability: 강수확률이며 0~100 사이의 정수인지 검증합니다.
class WeatherSchema(BaseModel):
    temperature: float = Field(
        ge=-100,
        le=100,
        description="Temperature in Celsius"
    )

    precipitation_probability: int = Field(
        ge=0,
        le=100,
        description="Probability of precipitation (%)"
    )

# Countries.dev API의 국가 정보를 검증하는 모델
class CountrySchema(BaseModel):
    country_name: str = Field(
        min_length=1,
        description="Country_name"
    )

# ip-api의 IP 기반 위치 정보를 검증하는 모델
class IpSchema(BaseModel):
    country: str = Field(
        min_length=1,
        description="Country from IP address"
    )

    city: str = Field(
        min_length=1,
        description="City from IP address"
    )

# 날씨 데이터를 검증하고, 오류 발생 시 예외를 처리합니다.
def validate_weather(data):
    try:
        validated = WeatherSchema(
            temperature=data["temperature"],
            precipitation_probability=data["precipitation_probability"]
        )

        return validated
    
    except ValidationError as ve:
        print(f"날씨 데이터 검증 실패. Error : {ve}")

        return None