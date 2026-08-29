# Sweep Food Backend

Run the API from this directory:

```bash
uv sync
uv run python main.py
```

The API prefix is `/api`. The initial health module provides:

- `GET /api/health/liveness` — JSON process liveness response.
- `GET /api/health/error` — deterministic global-error response.
- `GET /api/health/text` — `Build with Cloudian Love Cloud` as plain text.

Each feature module follows the same four-file layout:

- `*_router.py`
- `*_service.py`
- `*_dependency.py`
- `*_dto.py`
