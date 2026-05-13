# Agent Guidance

## Run the server

```bash
uvicorn main:app --reload
# or with Docker (ensure network "app" exists first: docker network create app)
docker-compose up -d --build
```

## Port

- Local (`uvicorn`): `127.0.0.1:8000`
- Docker: `127.0.0.1:8888` (Dockerfile/ compose expose 8888, not 8000)

## Docker network

`docker-compose.yaml` references an `external: true` network called `app`. If starting fresh, create it first:
```bash
docker network create app
```

## Ticker suffix for Brazilian assets

Tickers on B3 must append `.SA` (e.g., `PETR4.SA`, `MXRF11.SA`).

## Ticker input validation

- Symbols are normalized with `strip().upper()`.
- Valid format: up to 16 chars, only `[A-Z0-9.-]`.
- Invalid format returns `400` with code `INVALID_INPUT`.

## Architecture

- `main.py` — FastAPI app, includes `controllers/ticker_controller.py` router
- `controllers/` — FastAPI route handlers
- `services/` — Business logic + `ServiceException` hierarchy (`NotFoundException`, `InvalidInputException`, `ServiceUnavailableException`)
- `services/rate_limit.py` — Rate limiter using slowapi (30 requests/minute per IP)

## Error behavior

- Unknown ticker / empty upstream payload: `404` with code `NOT_FOUND`
- Invalid ticker format: `400` with code `INVALID_INPUT`
- Upstream provider/network failure: `503` with code `SERVICE_UNAVAILABLE`

## Testing

Tests use `pytest` with `httpx` for FastAPI's `TestClient`. Keep tests deterministic and offline by mocking `yfinance` calls (no external network dependency).

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_ticker_service.py -v
```

Fixtures are defined in `tests/conftest.py`. Test modules: `test_service_exception.py`, `test_ticker_service.py`, `test_ticker_controller.py`, `test_main.py`, `test_rate_limit.py`.

`yfinance-test.py` is a scratch script, not a test suite.

## Lint and Typecheck

`pyproject.toml` has ruff config (lint + format). `mypy.ini` has type checking config.

```bash
# Lint and format check
ruff check . && ruff format --check .

# Type check (run on specific files to avoid .venv issues)
mypy main.py controllers/ticker_controller.py services/ticker_service.py services/service_exception.py services/rate_limit.py

# Full verification: lint -> typecheck -> test
ruff check . && ruff format --check . && mypy main.py controllers/ticker_controller.py services/ticker_service.py services/service_exception.py services/rate_limit.py && pytest tests/
```

## Package structure

`controllers/` and `services/` require `__init__.py` for proper package resolution.
