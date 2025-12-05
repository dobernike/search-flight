from typing import TypedDict

from fast_flights import FlightData, Passengers, create_filter


class FlightUrls(TypedDict):
    aviasales: str
    skyscanner: str
    gflights: str


def generate_google_flights_url(
    origin: str,
    destination: str,
    depart_date: str,
    adults: int = 1,
    seat_type: str = "economy",
    max_stops: int | None = None,
    currency: str = "USD",
) -> str:
    # Create a new filter
    filter = create_filter(
        flight_data=[
            FlightData(
                date=depart_date,  # Date of departure for outbound flight
                from_airport=origin,
                to_airport=destination,
            ),
        ],
        trip="one-way",  # Trip (round-trip, one-way)
        seat=seat_type,  # Seat (economy, premium-economy, business or first)
        passengers=Passengers(
            adults=adults, children=0, infants_in_seat=0, infants_on_lap=0
        ),
        max_stops=max_stops,
    )

    # Encode the filter to base64
    b64 = filter.as_b64().decode("utf-8")

    # Construct the Google Flights URL
    url = f"https://www.google.com/travel/flights?tfs={b64}&curr={currency}"
    return url


# "CTG" "BOG" "2025-03-28"
def get_flight_search_urls(
    origin: str, destination: str, date: str, adults: int = 2
) -> FlightUrls:
    year, month, day = date.split("-")

    # https://www.aviasales.com/search/ctg2803bog2
    aviasales_url = (
        f"https://www.aviasales.com/search/{origin}{day}{month}{destination}{adults}"
    )

    # https://skyscanner.com/transport/flights/ctg/bog/250223/?adultsv2=2
    skyscanner_url = f"https://skyscanner.com/transport/flights/{origin}/{destination}/{year}{month}{day}/?adultsv2={adults}"

    # https://www.google.com/travel/flights?tfs=GhoSCjIwMjUtMDMtMjhqBRIDQ1RHcgUSA0JPR0ICAQFIAZgBAg==&curr=USD
    google_flights_url = generate_google_flights_url(origin, destination, date, adults)

    return {
        "aviasales": aviasales_url,
        "skyscanner": skyscanner_url,
        "gflights": google_flights_url,
    }
