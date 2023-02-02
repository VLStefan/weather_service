from typing import Union

import asyncio
from fastapi import APIRouter

from service.utils import check_and_update_cities, get_weather_forecast_for_city

base_router: APIRouter = APIRouter()

@base_router.get("/")
def root():
    coroutine = check_and_update_cities()
    asyncio.run(coroutine)
    return {"Hello": "World"}


@base_router.get("/forecast/{city_name}")
async def forecast(city: Union[str, None] = None):
    response = await get_weather_forecast_for_city(city_name=city)

    return {"query": city}

@base_router.get("/weather_history/{city_name}")
def forecast_history(city: Union[str, None] = None):
    return {"query": city}
