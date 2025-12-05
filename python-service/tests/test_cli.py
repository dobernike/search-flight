import argparse

import pytest

from search_flight.cli import date_type


def test_date_type():
    data = "2025-12-20"

    assert date_type(data) == data

    with pytest.raises(argparse.ArgumentTypeError):
        date_type("2025/12/20")

    with pytest.raises(argparse.ArgumentTypeError):
        date_type("2025_12_20")

    with pytest.raises(argparse.ArgumentTypeError):
        date_type("2025-13-01")

    with pytest.raises(argparse.ArgumentTypeError):
        date_type("2025-12-32")

    assert date_type("2025-01-01") == "2025-01-01"
    assert date_type("2025-12-31") == "2025-12-31"


"""
More test cases for cli module

2. generate_google_flights_url() function:
   - Test basic URL generation with required parameters
   - Test URL contains correct base URL
   - Test URL contains base64 encoded filter
   - Test different seat types (economy, premium-economy, business, first)
   - Test different currencies
   - Test different number of adults
   - Test max_stops parameter

3. CliArgs model (Pydantic):
   - Test valid airport codes (3-letter format)
   - Test invalid airport codes (too short, too long)
   - Test uppercase conversion of airport codes
   - Test valid date parsing
   - Test invalid adults values (zero, negative)
   - Test default adults value

4. main() function integration:
   - Test argument parsing with valid inputs
   - Test browser opening is called (mock webbrowser)
   - Test URL generation for all three services (Aviasales, Skyscanner, Google Flights)
"""
