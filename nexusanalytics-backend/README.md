# NexusAnalytics Backend

## Structure

- `app/main.py` - FastAPI app factory and router registration.
- `app/api/v1/endpoints/` - Route modules (`summoner`, `matches`).
- `app/services/riot/client.py` - Riot API integration layer.
- `app/core/config.py` - Environment-backed settings.
- `app/core/errors.py` - Shared Riot error mapping.
- `app/models/` - Database models (future).
- `app/repositories/` - Data access layer (future).
- `app/cache/` - Caching helpers (future, e.g. Redis).
- `app/workers/` - Background jobs (future).
- `tests/` - Backend test package.

## Run

You can keep your existing command:

```bash
uvicorn main:app --reload
```

## Environment Variables

- `RIOT_API_KEY` (required)
- `REDIS_URL` (optional, example: `redis://localhost:6379/0`)
- `CACHE_TTL_SECONDS` (optional, default: `300`)
- `MATCH_DETAILS_CACHE_TTL_SECONDS` (optional, default: `300`)

## Routes

- Legacy routes remain available:
  - `GET /summoner/{summoner_name}/{tag}`
  - `GET /match-history/{puuid}`
- Versioned routes are also available:
  - `GET /api/v1/summoner/{summoner_name}/{tag}`
  - `GET /api/v1/match-history/{puuid}`
  - `GET /api/v1/match-details/{match_id}?force_refresh=false`
  - `GET /api/v1/match-cards/{puuid}?count=5&force_refresh=false`
