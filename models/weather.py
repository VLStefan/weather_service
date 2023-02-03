from pydantic import BaseModel, Field


class WeatherModel(BaseModel):
    city: str
    