import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    riot_api_key: str | None = os.getenv("RIOT_API_KEY")
    riot_account_base_url: str = "https://europe.api.riotgames.com"
    riot_match_base_url: str = "https://europe.api.riotgames.com"
    redis_url: str | None = os.getenv("REDIS_URL")
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))
    match_details_cache_ttl_seconds: int = int(os.getenv("MATCH_DETAILS_CACHE_TTL_SECONDS", "300"))


settings = Settings()
