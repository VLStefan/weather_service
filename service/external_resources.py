import time
from typing import Any, Coroutine, Dict, List, Union

from fastapi import status
from fastapi.exceptions import HTTPException
from httpx import AsyncClient, HTTPError, HTTPStatusError
from config import ACCUWEATHER_TOKEN


class ExternalService:
    REQUEST_TIMEOUT = 60

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
