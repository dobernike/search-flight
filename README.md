# search-flight monorepo

This repository contains:
- `python-service`: core flight URL generator, CLI (`sfly`), and API.
- `web`: Astro frontend (no React) that calls the Python API.

The web form enforces valid airport IATA codes by using backend-powered autocomplete.

## Local development

### 1) Python API

```bash
cd python-service
uv sync --dev
uv run uvicorn search_flight.api:app --reload --host 0.0.0.0 --port 8000
```

### 2) Astro web UI

```bash
cd web
npm install
PUBLIC_API_BASE_URL=http://localhost:8000 npm run dev
```

Open [http://localhost:4321](http://localhost:4321).

## API contract

`POST /api/search-urls`

Request:

```json
{
  "origin": "CTG",
  "destination": "BOG",
  "date": "2026-04-20",
  "adults": 2
}
```

Response:

```json
{
  "aviasales": "https://...",
  "skyscanner": "https://...",
  "gflights": "https://..."
}
```

Validation:
- `origin`, `destination`: uppercase 3-letter IATA codes.
- `origin`, `destination`: must exist in known airport IATA dataset.
- `date`: `YYYY-MM-DD`.
- `adults`: integer `>= 1`.

`GET /api/airports/autocomplete?term=<query>`
- Returns airport suggestions for autocomplete.
- Supports searching by IATA code, airport name, city, or country.
