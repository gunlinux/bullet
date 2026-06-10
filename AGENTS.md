# QWEN.md

## Project overview

**lmao-server** — a from-scratch Python ASGI micro-framework called **bullet**, built directly against the raw ASGI protocol contract. No Flask, Django, FastAPI, or any third-party web framework. The point is learning how ASGI works at the wire level.

The project is in active early development. The old learning code (raw WSGI/ASGI/RSGI implementations + schema comparison across pydantic/marshmallow/msgspec) has been removed; only `app/asgi.py` remains as a reference raw ASGI implementation.

## Environment

- Python **3.12+** (see `.python-version`)
- Package manager: [`uv`](https://docs.astral.sh/uv/) with `uv.lock` checked in
- Virtual env: `.venv/`

```bash
uv sync                    # install deps into .venv
uv sync --dev              # install with dev deps (linters, pytest, etc.)
```

## Key commands (from `Makefile`)

| Command | What it does |
|---------|-------------|
| `uv run uvicorn main:app_asgi` | Run the bullet app via uvicorn |
| `make dev` | `uv sync --dev && uv run uvicorn main:app_asgi` |
| `make check` | `make lint && make fix && make types && make test` |
| `make lint` | `uv run ruff check` |
| `make fix` | `uv run ruff check --fix && uv run ruff format` |
| `make types` | `uv run pyright` |
| `make test` | `uv run pytest` |

**Always run servers from the repo root.** Path-dependent imports assume the working directory is `/Users/loki/work/lmao_server`.

## Architecture

```
main.py              ← entry point: `from app import create_app_asgi`
app/
  __init__.py        ← `create_app_asgi()` — builds a BulletApp, registers routes
  asgi.py            ← standalone raw ASGI `application(scope, receive, send)` for reference
bullet/
  __init__.py        ← the bullet micro-framework: BulletApp, Handler, Request
debug.py             ← alternative uvicorn runner (async main)
temp.py              ← throwaway test client (requests)
```

### `main.py`
Imports `create_app_asgi` from `app` and assigns `app_asgi`. Served via `uvicorn main:app_asgi`.

### `app/__init__.py` — the bullet app
Creates a `BulletApp` instance with two routes:
- `GET /` → returns `{"name": "loki", "age": 37}` as JSON
- `GET /age/<age>` → returns `{"age": <age>}` as JSON (using parameter extraction from route pattern)

### `bullet/__init__.py` — the bullet framework

Core classes:

- **`BulletApp`** — callable ASGI application. Handles the `lifespan` protocol, drains request body, does route matching via `self.handlers` dict, dispatches to `Handler.execute()`, and sends JSON responses via `send_json`.

- **`Handler`** — wraps a route pattern and async handler callable. `execute(request)` calls the handler. Currently hardcoded to pass `age=16` (WIP — parameter extraction not yet wired).

- **`Request`** — parsed ASGI `scope` into typed attributes (method, path, query_string, headers, body, etc.).

- **`Addr`** — dataclass for server/client address (host, port).

- **`validate_handler(path, handler)`** — verifies that `<param>` placeholders in the route pattern correspond to annotated parameters on the handler. Raises `ValueError` if mismatched.

**Known issues / WIP in bullet:**
- Route matching in `BulletApp.__call__` has hardcoded debug strings (`path = '/age/<age>'`), not real pattern matching.
- `Handler.execute` hardcodes `age=16` instead of extracting the value from the actual request path.
- `BulletApp.send_json` passes `io.StringIO(body)` to `http.response.body` — likely a bug (should be `body` bytes directly).
- `app/asgi.py`'s `send_json` is imported into bullet but also has a local duplicate `BulletApp.send_json`.

### `app/asgi.py` — raw ASGI reference
A standalone raw ASGI `application(scope, receive, send)` with:
- Lifespan protocol handling
- Simple path-based routing: `/`, `/about`, `/contact`, `/api/*`
- `send_html` and `send_json` response helpers
- Partial `/api` routes for pydantic, marshmallow, msgspec (some commented out)
- The `home_page` handler is incomplete

This module is **not** wired into `main.py` — it exists as a learning reference. Its `send_json` helper is imported by `bullet/__init__.py`.

## Dependencies (`pyproject.toml`)

### Runtime
- `granian` — RSGI/ASGI/WSGI server
- `gunicorn` — WSGI server
- `uvicorn[standard]` — ASGI server (primary, used for development)
- `msgspec`, `pydantic`, `ujson` — serialization (legacy from the old schema comparison project, may not all be in use currently)

### Dev
- `pyright` — static type checking
- `pytest` — test runner
- `requests` — HTTP client (used in `temp.py`)
- `ruff` — linter + formatter

## Conventions

- No web framework — everything is built directly on the ASGI spec.
- Type annotations are expected for handler parameters (used by `validate_handler`).
- UTF-8 encoding for all string→bytes conversions.
- JSON responses use `application/json; charset=utf-8`.
- Route patterns use Flask-style `<param>` syntax.
- The project has **no tests yet** despite pytest being configured.
