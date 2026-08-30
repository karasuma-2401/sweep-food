# ADR-001: Use Neon PostgreSQL as the Primary Database

## Status

Accepted

## Date

2026-08-29

## Context

Sweep Food needs a relational system of record for user accounts, sessions, ingredient catalog data, inventory batches, immutable stock ledger entries, recipes, meal plans, cooking transactions, shopping lists, and notifications. The backend requires PostgreSQL transactions, constraints, indexes, UUIDs, and `jsonb` metadata.

The project environment already supplies a Neon connection through `DATABASE_URL`. The team wants a managed database rather than operating a local PostgreSQL container as the application database. Local development still needs deterministic provider mocks and Redis, while schema migration and test data must never risk a shared staging or production database.

## Decision

Use Neon PostgreSQL as the authoritative persistent database for Sweep Food.

- The application connects through `DATABASE_URL` supplied by environment configuration.
- Alembic migrations remain the executable schema history; `docs/DATABASE.txt` remains the approved logical schema.
- Local development uses Neon development/test branches or an isolated test database, not a Docker PostgreSQL service.
- Automated tests, migration experiments, seed validation, and destructive operations run only against disposable database branches/databases.
- Redis remains a separate dependency for ephemeral OTP state, rate limiting, locks, cache, and background-job coordination.
- If pooled application connections are unsuitable for Alembic, a separate secret `DATABASE_URL_DIRECT` is used only for migration operations.

## Alternatives Considered

### Local PostgreSQL in Docker

- Pros: fully local development and simple database resets.
- Cons: diverges from the managed Neon environment and increases local infrastructure to operate.
- Rejected: Neon is already the chosen managed database. Docker remains useful for Redis and WireMock, while isolated Neon branches provide safe migration/test targets.

### SQLite

- Pros: no separate database service for local development.
- Cons: does not faithfully exercise PostgreSQL `jsonb`, transaction, locking, constraint, and migration behavior required by batch-level inventory and FEFO cooking.
- Rejected: it would create a misleading development/test environment for core data integrity logic.

### Persisting ephemeral state in Neon

- Pros: one infrastructure dependency.
- Cons: inefficient TTL/rate-limit/lock behavior and unnecessary persistence for OTP challenges and worker coordination.
- Rejected: Redis better matches the ephemeral and coordination use cases.

## Consequences

- Engineers need access to a safe Neon development/test branch before running migrations or integration tests.
- Connection strings are secrets and must never be committed, logged, or included in fixtures.
- Docker Compose does not create a PostgreSQL container; its local dependencies are Redis and WireMock.
- Migrations must be reviewed as carefully as application code and run first on a disposable Neon branch.
- Production-safe schema changes follow expand → backfill → switch → contract rather than destructive in-place changes.

## Related Documentation

- [`../prd.md`](../prd.md)
- [`../DATABASE.txt`](../DATABASE.txt)
- [`../../COOKBOOK.md`](../../COOKBOOK.md)
- [`../../../../tasks/plan.md`](../../../../tasks/plan.md)
