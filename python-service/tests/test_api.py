from fastapi.testclient import TestClient

from search_flight.api import create_app
from search_flight.core import get_flight_search_urls


client = TestClient(create_app())


def test_search_urls_success_and_matches_core():
    payload = {
        "origin": "ctg",
        "destination": "bog",
        "date": "2026-04-20",
        "adults": 2,
    }

    response = client.post("/api/search-urls", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"aviasales", "skyscanner", "gflights"}

    expected = get_flight_search_urls("CTG", "BOG", "2026-04-20", adults=2)
    assert data == expected


def test_search_urls_rejects_invalid_iata_codes():
    payload = {
        "origin": "ct",
        "destination": "BOG",
        "date": "2026-04-20",
        "adults": 2,
    }

    response = client.post("/api/search-urls", json=payload)

    assert response.status_code == 422


def test_search_urls_rejects_invalid_date():
    payload = {
        "origin": "CTG",
        "destination": "BOG",
        "date": "20-04-2026",
        "adults": 2,
    }

    response = client.post("/api/search-urls", json=payload)

    assert response.status_code == 422


def test_search_urls_rejects_invalid_adults():
    payload = {
        "origin": "CTG",
        "destination": "BOG",
        "date": "2026-04-20",
        "adults": 0,
    }

    response = client.post("/api/search-urls", json=payload)

    assert response.status_code == 422


def test_search_urls_rejects_unknown_iata_codes():
    payload = {
        "origin": "ZZZ",
        "destination": "BOG",
        "date": "2026-04-20",
        "adults": 1,
    }

    response = client.post("/api/search-urls", json=payload)

    assert response.status_code == 422


def test_airports_autocomplete_returns_suggestions():
    response = client.get("/api/airports/autocomplete", params={"term": "LHR"})

    assert response.status_code == 200
    data = response.json()
    assert data
    assert any(item["code"] == "LHR" for item in data)
