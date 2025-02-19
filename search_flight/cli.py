import argparse
import datetime
import webbrowser

from fast_flights import FlightData, Passengers, create_filter


def date_type(value: str) -> str:
    try:
        date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        return str(date)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"format isn't correct: {value}. Use format YYYY-MM-DD, ex. 2025-03-28"
        )


def generate_google_flights_url(
    origin,
    destination,
    depart_date,
    adults=1,
    seat_type="economy",
    max_stops=None,
    currency="USD",
):
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Open a browser with pre-filled flight search information."
    )
    parser.add_argument("origin", type=str, help="Origin airport code")
    parser.add_argument("destination", type=str, help="Destination airport code")
    parser.add_argument("date", type=date_type, help="Flight date in YYYY-MM-DD format")
    parser.add_argument(
        "--adults",
        default=2,
        type=int,
        required=False,
        help="Number of adults (default: 2)",
    )
    args = parser.parse_args()

    fly_from = args.origin  # "CTG"
    fly_to = args.destination  # "BOG"
    fly_date = args.date  # 2025-03-28
    splitted_date = fly_date.split("-")  # [2025, 03, 28]
    fly_year = splitted_date[0]
    fly_month = splitted_date[1]
    fly_day = splitted_date[2]
    adults = args.adults

    # https://www.aviasales.com/search/ctg2803bog2
    aviasales_url = f"https://www.aviasales.com/search/{fly_from}{fly_day}{fly_month}{fly_to}{adults}"
    webbrowser.open(aviasales_url)

    # https://skyscanner.com/transport/flights/ctg/bog/250223/?adultsv2=2
    skyscanner_url = f"https://skyscanner.com/transport/flights/{fly_from}/{fly_to}/{fly_year}{fly_month}{fly_day}/?adultsv2={adults}"
    webbrowser.open(skyscanner_url)

    # https://www.google.com/travel/flights?tfs=GhoSCjIwMjUtMDMtMjhqBRIDQ1RHcgUSA0JPR0ICAQFIAZgBAg==&curr=USD
    google_flights_url = generate_google_flights_url(fly_from, fly_to, fly_date, adults)
    webbrowser.open(google_flights_url)


if __name__ == "__main__":
    main()
