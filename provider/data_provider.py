import datetime
from typing import Any, Optional
from collections import defaultdict

from sqlalchemy import insert

from db import city, database
from service.accuweather_service import AccuWeatherService
from service.local_resources import WeatherDataService
from service.weatherstack_service import WeatherStackService


async def check_and_update_cities() -> None:
    local_data_service = WeatherDataService()
    record_count = await local_data_service.get_city_count()

    if record_count <= 150:
        await update_cities()


async def update_cities() -> None:
    external_api = AccuWeatherService()

    cities_data = await external_api.fetch_top_cities()

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


async def get_current_weather_forecast_for_city(city_name: str) -> Any:
    external_api = WeatherStackService()
    forecast_data = {}
    forecast_response = await external_api.fetch_current_weather(city=city_name)

    forecast_data["weather"] = forecast_response.get("current", {})
    forecast_data["location"] = forecast_response.get("location", {})

    return forecast_data


async def get_history_weather_forecast_for_city(
    city_name: str,
    day: Optional[int],
    month: Optional[int],
    year: Optional[int],
    number_of_days: int,
) -> Any:
    external_api = WeatherStackService()
    forecast_data = {}
    today = datetime.date.today()
    date = datetime.date(
        day=day or today.day,
        month=month or today.month,
        year=year or today.year,
    )
    days = [str(date + datetime.timedelta(days=number)) for number in range(number_of_days)]

    forecast_response = await external_api.fetch_historical_forecast(city=city_name, dates=days)

    forecast_data["location"] = forecast_response.get("location", {})
    forecast_data["historical"] = forecast_response.get("historical", {})

    return forecast_data


async def get_weather_forecast_statistics_for_city(
    city_name: str,
    day: Optional[int],
    month: Optional[int],
    min_year: int,
    max_year: int,
    number_of_days: int,
) -> Any:
    external_api = WeatherStackService()
    forecast_data = {}
    average_values = defaultdict(dict)

    mintemp = defaultdict(list)
    maxtemp = defaultdict(list)
    avgtemp = defaultdict(list)
    totalsnow = defaultdict(list)
    sunhour = defaultdict(list)
    uv_index = defaultdict(list)


    days = []
    today = datetime.date.today()

    for year_value in range(min_year, max_year+1):
        base_date = datetime.date(
            day=day or today.day,
            month=month or today.month,
            year=year_value,
        )
        days += [str(base_date + datetime.timedelta(days=number)) for number in range(number_of_days)]

    forecast_response = await external_api.fetch_historical_forecast(city=city_name, dates=days)

    forecast_data["location"] = forecast_response.get("location", {})
    all_forecast_data = forecast_response.get("historical", {})

    for record_date, values in all_forecast_data.items():
        day_month = record_date[5:]
        average_values[day_month] = {}
        mintemp[day_month].append(values["mintemp"])
        maxtemp[day_month].append(values["maxtemp"])
        avgtemp[day_month].append(values["avgtemp"])
        totalsnow[day_month].append(values["totalsnow"])
        sunhour[day_month].append(values["sunhour"])
        uv_index[day_month].append(values["uv_index"])

    for record_date in average_values.keys():
        average_values[record_date] = {
            "mintemp": min(mintemp[record_date]),
            "maxtemp": max(maxtemp[record_date]),
            "avgtemp": round(sum(avgtemp[record_date])/len(avgtemp[record_date]), 2),
            "totalsnow": round(sum(totalsnow[record_date])/len(totalsnow[record_date]), 2),
            "sunhour": round(sum(sunhour[record_date])/len(sunhour[record_date]), 2),
            "uv_index": round(sum(uv_index[record_date])/len(uv_index[record_date]), 2),
        }

    forecast_data["statistics"] = average_values
    return forecast_data
