# --------------------------------------------------------------
# Pydantic 스키마 검증 테스트를 수행하는 파일입니다.
# 정상 데이터는 올바르게 생성되는지 확인하고,
# 잘못된 데이터는 ValidationError가 발생하는지 pytest를 이용하여 테스트합니다.
# --------------------------------------------------------------


import pytest
from pydantic import ValidationError

from schemas import WeatherSchema


def test_weather_valid():
    data = WeatherSchema(
        temperature=25.5,
        precipitation_probability=40
    )

    assert data.temperature == 25.5

def test_weather_invalid():
    with pytest.raises(ValidationError):
        WeatherSchema(
            temperature=200,
            precipitation_probability=50
        )