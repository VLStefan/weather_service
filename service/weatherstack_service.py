import time
from typing import Any, Dict, List

from config import WEATHERSTACK_TOKEN
from service.external_resources import ExternalService


class WeatherStackService(ExternalService):
    REQUEST_TIMEOUT = 20

    async def fetch_forecast(
        self, city: str, dates: List[str],
    ) -> List[Dict[str, Any]]:
        historical_dates = ";".join(dates) if len(dates) > 1 else dates[0]
        endpoint = f"https://api.weatherstack.com/historical?access_key={WEATHERSTACK_TOKEN}&query={city}&historical_date={historical_dates}"
        response = await self._request(
            method="GET", endpoint=endpoint
        )
        return response


    async def fetch_current(
        self, city: str, period: int,
    ) -> List[Dict[str, Any]]:
        endpoint = f"https://api.weatherstack.com/current?access_key={WEATHERSTACK_TOKEN}&query={city}"
        response = await self._request(
            method="GET", endpoint=endpoint
        )
        return response
