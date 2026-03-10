import json
from datetime import date
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from search_flight.core import FlightUrls, get_flight_search_urls

DEFAULT_ALLOWED_ORIGINS = [
    "http://localhost:4321",
    "http://127.0.0.1:4321",
]


class SearchUrlsRequest(BaseModel):
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    date: date
    adults: int = Field(default=2, ge=1)

    @field_validator("origin", "destination")
    @classmethod
    def validate_iata(cls, value: str) -> str:
        code = value.strip().upper()
        if len(code) != 3 or not code.isalpha():
            raise ValueError("must be a valid 3-letter IATA code")
        if code not in get_airports_data():
            raise ValueError("must be a known IATA airport code")
        return code


class SearchUrlsResponse(BaseModel):
    aviasales: str
    skyscanner: str
    gflights: str


class AirportSuggestion(BaseModel):
    code: str
    name: str
    city: str
    country: str


@lru_cache(maxsize=1)
def get_airports_data() -> dict[str, dict[str, str]]:
    data_path = Path(__file__).resolve().parent / "data" / "airports_iata.json"
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    return {item["code"]: item for item in payload["airports"]}


def build_airport_suggestions(term: str, limit: int = 8) -> list[AirportSuggestion]:
    normalized = term.strip().lower()
    if len(normalized) < 2:
        return []

    results: list[AirportSuggestion] = []
    for code, airport in get_airports_data().items():
        code_l = code.lower()
        name = airport.get("name", "")
        city = airport.get("city", "")
        country = airport.get("country", "")
        haystack = f"{name} {city} {country}".lower()

        if normalized in haystack or code_l.startswith(normalized):
            results.append(
                AirportSuggestion(code=code, name=name, city=city, country=country)
            )

    results.sort(
        key=lambda item: (
            not item.code.lower().startswith(normalized),
            item.city.lower(),
            item.name.lower(),
        )
    )
    return results[:limit]


def create_app() -> FastAPI:
    app = FastAPI(title="search-flight API", version="1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=DEFAULT_ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    @app.get("/api/airports/autocomplete", response_model=list[AirportSuggestion])
    def airports_autocomplete(term: str) -> list[AirportSuggestion]:
        return build_airport_suggestions(term)

    @app.post("/api/search-urls", response_model=SearchUrlsResponse)
    def search_urls(payload: SearchUrlsRequest) -> FlightUrls:
        return get_flight_search_urls(
            origin=payload.origin,
            destination=payload.destination,
            date=payload.date.isoformat(),
            adults=payload.adults,
        )

    return app


app = create_app()
