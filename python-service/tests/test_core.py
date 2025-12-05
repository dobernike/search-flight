import re

from search_flight.core import generate_google_flights_url, get_flight_search_urls


def test_get_flight_search_urls_basic():
    urls = get_flight_search_urls("CTG", "BOG", "2025-03-28", adults=2)

    assert urls["aviasales"].startswith("https://www.aviasales.com/search/")
    assert "CTG" in urls["aviasales"]
    assert "BOG" in urls["aviasales"]
    assert "2" in urls["aviasales"]

    assert urls["skyscanner"].startswith("https://skyscanner.com/transport/flights/")
    assert "CTG" in urls["skyscanner"]
    assert "BOG" in urls["skyscanner"]
    assert "adultsv2=2" in urls["skyscanner"]

    assert urls["gflights"].startswith("https://www.google.com/travel/flights?")


def test_get_flight_search_urls_date_format_used():
    date = "2025-12-31"
    year, month, day = date.split("-")

    urls = get_flight_search_urls("CTG", "BOG", date, adults=1)

    assert f"{day}{month}" in urls["aviasales"]
    assert f"{year}{month}{day}" in urls["skyscanner"]


def test_generate_google_flights_url_base_parts():
    url = generate_google_flights_url(
        origin="CTG",
        destination="BOG",
        depart_date="2025-03-28",
        adults=3,
        seat_type="economy",
        currency="USD",
    )

    assert url.startswith("https://www.google.com/travel/flights?")
    assert "curr=USD" in url

    assert "tfs=" in url
    assert re.search(r"tfs=[A-Za-z0-9_\-%]+", url)
