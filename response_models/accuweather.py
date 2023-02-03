from typing import Any, Dict

from pydantic import BaseModel


class AccuWeather(BaseModel):
    Date: str
    Temperature: Dict[str, Any]
    Day: Dict[str, Any]
    Night: Dict[str, Any]
