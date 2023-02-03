import time
from typing import Any, Dict, List

from service.external_resources import ExternalService
from config import ACCUWEATHER_TOKEN

class AccuWeatherService(ExternalService):
    REQUEST_TIMEOUT = 20

    async def city_search(
        self, city: str
    ) -> Dict[str, Any]:
        endpoint = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={ACCUWEATHER_TOKEN}&q=city{city}"
        response = await self._request(
            method="GET", endpoint=endpoint
        )
        return response
    
    
    async def fetch_top_cities(
        self
    ) -> List[Dict[str, Any]]:
        endpoint = f"http://dataservice.accuweather.com/locations/v1/topcities/150?apikey={ACCUWEATHER_TOKEN}"
        response = await self._request(
            method="GET", endpoint=endpoint
        )
        return response

    async def fetch_5_days_forecast(
        self, city_id: str
    ) -> Dict[str, Any]:
        endpoint = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{city_id}?apikey={ACCUWEATHER_TOKEN}"
        response = await self._request(
            method="GET", endpoint=endpoint
        )
        return response
