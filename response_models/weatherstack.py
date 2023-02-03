from typing import List

from pydantic import BaseModel


class CurrentWeather(BaseModel):
    temperature: int
    weather_descriptions: List[str]
    wind_speed: int
    wind_degree: int
    wind_dir: str
    pressure: int
    precip: int
    humidity: int
    cloudcover: int
    feelslike: int
    uv_index: int
    visibility: int


class Location(BaseModel):
    name: str
    country: str
    lat: str
    lon: str
    timezone_id: str
    localtime: str


class CurrentWeatherResponse(BaseModel):
    location: Location
    weather: CurrentWeather
