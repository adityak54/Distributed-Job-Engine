# Job Engine

A distributed job execution engine built in Python. Jobs are submitted via API, queued, and processed by background workers with retry logic, state tracking, and observability.

## Tech Stack

- **Python** (FastAPI, SQLAlchemy, Alembic)
- **PostgreSQL** (production) / **SQLite** (testing)
- **Redis** (job queue broker)
- **Prometheus + Grafana** (metrics & dashboards)
- **Docker Compose** (containerized infrastructure)
- **GitHub Actions** (CI/CD)

## Phases

### Phase 1: Core Engine

Local-first development — models, worker, handlers, and tests.

**1. Project setup**
- Created `pyproject.toml` with dependencies (`sqlalchemy`, `alembic`, `pydantic-settings`, `redis`, `psycopg2-binary`)
- Centralized configuration via `pydantic-settings` in `src/config.py`, loaded from `.env`
- `.env.example` committed as a template, `.env` is git-ignored

**2. Database**
- Defined `Job` model with 7 statuses: `PENDING → QUEUED → RUNNING → COMPLETED / FAILED → RETRYING → DEAD`
- Initialized Alembic for versioned schema migrations
- First migration auto-generated from models, applied to a Dockerized PostgreSQL instance

**3. Handler layer (Command pattern)**
- Abstract `JobHandler` base class with `execute()` and `validate()` methods
- `HandlerRegistry` for name-based handler lookup — adding a new job type = adding one file
- Three example handlers: `generate_report`, `send_email`, `process_csv`

**4. Queue abstraction**
- `BaseQueue` interface with `enqueue()` / `dequeue()`
- `MemoryQueue` — in-process queue for dev/testing
- `RedisQueue` — production queue using `RPUSH` / `BLPOP`

**5. Worker**
- `executor.py` — runs a job through the state machine, handles success, failure, validation errors, and retry/dead transitions
- `retry.py` — exponential backoff (`base * 2^retry_count`, capped at 60s)
- `main.py` — poll loop with graceful `SIGINT`/`SIGTERM` shutdown, auto-selects queue backend from config

**6. Tests (12 passing)**
- All tests run against in-memory SQLite — no Docker required
- Handler tests: registry operations, payload validation per handler
- Worker tests: `COMPLETED`, `FAILED`, `RETRYING`, `DEAD` state transitions
- Retry tests: backoff calculation and cap

```
python -m pytest tests/ -v
```

