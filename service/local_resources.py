from typing import Dict, Any
from db import database, city
from sqlalchemy import select, func


class WeatherDataService:

    async def get_city_by_name(self, city_name: str) -> Dict[str, Any]:
        city_obj = await database.fetch_one(
            select(city).where(city.c.name == city_name)
        )

        return dict(city_obj)

    async def get_city_count(self) -> int:
        query = select([func.count()]).select_from(city)
        record_count = await database.fetch_val(query)

        return record_count
