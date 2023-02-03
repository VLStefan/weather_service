import time
from typing import Any, Coroutine, Dict, List, Union

from fastapi import status
from fastapi.exceptions import HTTPException
from httpx import AsyncClient, HTTPError, HTTPStatusError
from config import WEATHERSTACK_TOKEN


class WeatherStackService:
    REQUEST_TIMEOUT = 20

    def __init__(self) -> None:
        self._request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json-patch+json",
        }

    async def _request(
        self,
        *,
        method: str,
        endpoint: str,
    ) -> Any:
        result = {}
        
        async with AsyncClient() as client:
            try:
                response = await client.request(
                    method,
                    endpoint,
                    headers=self._request_headers,
                    timeout=self.REQUEST_TIMEOUT,
                )
                response.raise_for_status()
            except (HTTPError, HTTPStatusError, Exception) as ex:
                if isinstance(ex, (HTTPError, HTTPStatusError)):
                    exc_text = ex.response.text
                    status_code = ex.response.status_code
                    if not exc_text:
                        exc_text = "".join(ex.args)
                else:
                    exc_text = "Something wrong"
                    status_code = 500

                raise HTTPException(
                    status_code=status_code,
                    detail={"message": exc_text},
                ) from None
            else:
                result = response.json()

        return result

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
