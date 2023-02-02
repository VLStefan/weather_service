from typing import Union

import asyncio
from fastapi import APIRouter

from service.utils import check_and_update_cities, get_weather_forecast_for_city

base_router: APIRouter = APIRouter(
    tags=["weather_forecast"],
)

@base_router.get("/")
def root():
    # coroutine = check_and_update_cities()
    # asyncio.run(coroutine)
    return {"Hello": "World"}


@base_router.get(
    "/forecast/{city_name}",
    summary="Get weather forecast by city for a 5 days"
)
async def forecast(city: str):
    response = await get_weather_forecast_for_city(city_name=city)

    return {"query": city}

@base_router.get("/weather_history/{city_name}")
def forecast_history(city: Union[str, None] = None):
    return {"query": city}
