from urllib.parse import quote
from typing import Any

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.core.errors import raise_for_riot_response


class RiotClient:
    async def get_account_by_riot_id(self, summoner_name: str, tag: str) -> dict[str, Any]:
        if not settings.riot_api_key:
            raise HTTPException(status_code=500, detail="RIOT_API_KEY is not set")

        encoded_summoner_name = quote(summoner_name)
        encoded_tag = quote(tag)
        url = (
            f"{settings.riot_account_base_url}"
            f"/riot/account/v1/accounts/by-riot-id/{encoded_summoner_name}/{encoded_tag}"
        )
        headers = {"X-Riot-Token": settings.riot_api_key}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, headers=headers)
            except httpx.RequestError as exc:
                raise HTTPException(status_code=500, detail=f"Request error: {str(exc)}")

        raise_for_riot_response(response)
        return response.json()

    async def get_account_by_puuid(self, puuid: str) -> dict[str, Any]:
        if not settings.riot_api_key:
            raise HTTPException(status_code=500, detail="RIOT_API_KEY is not set")

        encoded_puuid = quote(puuid)
        url = f"{settings.riot_account_base_url}/riot/account/v1/accounts/by-puuid/{encoded_puuid}"
        headers = {"X-Riot-Token": settings.riot_api_key}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, headers=headers)
            except httpx.RequestError as exc:
                raise HTTPException(status_code=500, detail=f"Request error: {str(exc)}")

        raise_for_riot_response(response)
        return response.json()

    async def get_match_history_ids(
        self,
        puuid: str,
        start: int,
        count: int,
        queue: int | None,
        type_: str | None,
        start_time: int | None,
        end_time: int | None,
    ) -> list[str]:
        if not settings.riot_api_key:
            raise HTTPException(status_code=500, detail="RIOT_API_KEY is not set")

        encoded_puuid = quote(puuid)
        url = f"{settings.riot_match_base_url}/lol/match/v5/matches/by-puuid/{encoded_puuid}/ids"
        headers = {"X-Riot-Token": settings.riot_api_key}
        params = {
            "start": start,
            "count": count,
            "queue": queue,
            "type": type_,
            "startTime": start_time,
            "endTime": end_time,
        }
        params = {key: value for key, value in params.items() if value is not None}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, headers=headers, params=params)
            except httpx.RequestError as exc:
                raise HTTPException(status_code=500, detail=f"Request error: {str(exc)}")

        raise_for_riot_response(response)
        return response.json()

    async def get_match_details(self, match_id: str) -> dict[str, Any]:
        if not settings.riot_api_key:
            raise HTTPException(status_code=500, detail="RIOT_API_KEY is not set")

        encoded_match_id = quote(match_id, safe="")
        url = f"{settings.riot_match_base_url}/lol/match/v5/matches/{encoded_match_id}"
        headers = {"X-Riot-Token": settings.riot_api_key}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, headers=headers)
            except httpx.RequestError as exc:
                raise HTTPException(status_code=500, detail=f"Request error: {str(exc)}")

        raise_for_riot_response(response)
        return response.json()


riot_client = RiotClient()
