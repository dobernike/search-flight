# search-flight
A simple CLI tool that opens popular flight aggregator websites with pre-filled search parameters, including departure and destination locations, travel dates, and the number of passengers. Ideal for quickly comparing flight options without manual input

## Installation
required python3.8+ and pipx

```
pipx install .
```

## Usage
```
sfly CTG BOG 2025-03-28 --adults 1
```

```
sfly CTG BOG 2025-03-28
```

will open the flight aggregator websites in your default browser with the pre-filled search parameters: departure city, destination city, travel date, and number of adults (default: 2).

## Next Feature
- Search by name of city instead of IATA code
