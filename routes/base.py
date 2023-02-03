import asyncio
from typing import List, Optional

from fastapi import APIRouter

from provider.data_provider import (
    check_and_update_cities,
    get_current_weather_forecast_for_city,
    get_history_weather_forecast_for_city,
    get_weather_forecast_for_city,
)
from response_models import accuweather, weatherstack

base_router: APIRouter = APIRouter(tags=["weather_forecast"], prefix="/forecast")


@base_router.get("/")
def root():
    coroutine = check_and_update_cities()
    asyncio.run(coroutine)
    return {"Hello": "World"}


@base_router.get(
    "/current/{city_name}",
    summary="Get  current weather forecast by city",
    response_model=weatherstack.CurrentWeatherResponse,
)
async def current_weather(city_name: str):
    response = await get_current_weather_forecast_for_city(city_name=city_name)

    return response


@base_router.get(
    "/{city_name}",
    summary="Get weather forecast by city for a 5 days",
    response_model=List[accuweather.AccuWeather],
)
async def weather_forecast(city_name: str):
    response = await get_weather_forecast_for_city(city_name=city_name)

    return response


@base_router.get(
    "/history/{city_name}",
    summary="Get history of weather for selected date range.",
)
async def weather_history(
    city_name: str,
    day: Optional[int] = None,
    month: Optional[int] = None,
    year: int = 2022,
    number_of_days: int = 5,
):
    response = await get_history_weather_forecast_for_city(
        city_name=city_name,
        day=day,
        month=month,
        year=year,
        number_of_days=number_of_days,
    )

    return response
