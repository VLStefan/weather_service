from typing import Any
from sqlalchemy import insert
from service.accuweather_service import AccuWeatherService
from service.local_resources import WeatherDataService
from db import database, city



async def check_and_update_cities() -> None:
    local_data_service = WeatherDataService()
    record_count = await local_data_service.get_city_count()

    if record_count <= 150:
        await update_cities()


async def update_cities() -> None:
    external_api = AccuWeatherService()

    cities_data = (await external_api.fetch_top_cities())

    await database.connect()

    async with database.transaction():
        for city_data in cities_data:
            city_id = city_data.get("Key")
            city_name = city_data.get("EnglishName")
            geo_position = city_data.get("GeoPosition", {})

            city_latitude = geo_position.get("Latitude")
            city_longitude = geo_position.get("Longitude")

            insert_city_query = insert(city).values(
                name=city_name,
                city_id=city_id,
                latitude=city_latitude,
                longitude=city_longitude,
            )
            await database.execute(insert_city_query)

    await database.disconnect()


async def get_weather_forecast_for_city(city_name: str) -> Any:
    local_data_service = WeatherDataService()
    external_api = AccuWeatherService()

    city_obj = await local_data_service.get_city_by_name(city_name=city_name)

    city_id = city_obj.get("city_id", "")

    forecast_response = await external_api.fetch_5_days_forecast(city_id=city_id)

    forecast_data = forecast_response.get("DailyForecasts", [])

    return forecast_data
