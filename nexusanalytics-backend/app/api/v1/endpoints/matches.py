from typing import Any, Optional

from fastapi import APIRouter, HTTPException

from app.cache.redis_cache import cache_client
from app.core.config import settings
from app.services.riot.client import riot_client

router = APIRouter()


def _champion_icon_url(champion_id: int) -> str:
    return (
        "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/"
        f"global/default/v1/champion-icons/{champion_id}.png"
    )


def _safe_number(value: Any) -> int:
    if isinstance(value, (int, float)):
        return int(value)
    return 0


def _participant_csing(participant: dict[str, Any]) -> int:
    return _safe_number(participant.get("totalMinionsKilled")) + _safe_number(
        participant.get("neutralMinionsKilled")
    )


async def _resolve_riot_identity(puuid: str) -> tuple[str, str]:
    cache_key = f"account-by-puuid:{puuid}"
    cached_value = await cache_client.get_json(cache_key)
    if cached_value is not None:
        return cached_value.get("gameName") or "Unknown", cached_value.get("tagLine") or "--"

    account = await riot_client.get_account_by_puuid(puuid)
    await cache_client.set_json(cache_key, account, ttl_seconds=settings.cache_ttl_seconds)
    return account.get("gameName") or "Unknown", account.get("tagLine") or "--"


async def _participant_name_tag(participant: dict[str, Any]) -> tuple[str, str]:
    game_name = participant.get("riotIdGameName") or participant.get("gameName")
    tag_line = participant.get("riotIdTagline") or participant.get("tagLine")
    if game_name and tag_line:
        return str(game_name), str(tag_line)

    puuid = participant.get("puuid")
    if puuid:
        return await _resolve_riot_identity(str(puuid))

    return "Unknown", "--"


async def _build_match_card(match_data: dict[str, Any], player_puuid: str) -> dict[str, Any]:
    info = match_data.get("info", {})
    participants = info.get("participants", [])
    duration_seconds = _safe_number(info.get("gameDuration"))
    duration_minutes = max(duration_seconds / 60, 1)

    player = next((item for item in participants if item.get("puuid") == player_puuid), None)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found in this match")

    player_team_id = player.get("teamId")
    player_kills = _safe_number(player.get("kills"))
    player_deaths = _safe_number(player.get("deaths"))
    player_assists = _safe_number(player.get("assists"))
    player_cs = _participant_csing(player)

    enriched: list[dict[str, Any]] = []
    for participant in participants:
        game_name, tag_line = await _participant_name_tag(participant)
        kills = _safe_number(participant.get("kills"))
        deaths = _safe_number(participant.get("deaths"))
        assists = _safe_number(participant.get("assists"))
        cs_value = _participant_csing(participant)

        enriched.append(
            {
                "gameName": game_name,
                "tagLine": tag_line,
                "championName": participant.get("championName"),
                "championId": participant.get("championId"),
                "championIconUrl": _champion_icon_url(_safe_number(participant.get("championId"))),
                "kills": kills,
                "deaths": deaths,
                "assists": assists,
                "kda": f"{kills}/{deaths}/{assists}",
                "cs": cs_value,
                "teamId": participant.get("teamId"),
                "win": bool(participant.get("win")),
            }
        )

    ally_participants = [item for item in enriched if item.get("teamId") == player_team_id]
    enemy_participants = [item for item in enriched if item.get("teamId") != player_team_id]

    return {
        "matchId": match_data.get("metadata", {}).get("matchId"),
        "queueId": info.get("queueId"),
        "gameMode": info.get("gameMode"),
        "gameDurationSeconds": duration_seconds,
        "player": {
            "gameName": player.get("riotIdGameName") or player.get("gameName"),
            "tagLine": player.get("riotIdTagline") or player.get("tagLine"),
            "championName": player.get("championName"),
            "championId": player.get("championId"),
            "championIconUrl": _champion_icon_url(_safe_number(player.get("championId"))),
            "kills": player_kills,
            "deaths": player_deaths,
            "assists": player_assists,
            "kda": f"{player_kills}/{player_deaths}/{player_assists}",
            "cs": player_cs,
            "csPerMinute": round(player_cs / duration_minutes, 1),
            "win": bool(player.get("win")),
            "teamId": player_team_id,
        },
        "teams": {
            "ally": ally_participants,
            "enemy": enemy_participants,
        },
    }


@router.get("/match-history/{puuid}")
async def get_match_history(
    puuid: str,
    start: int = 0,
    count: int = 20,
    queue: Optional[int] = None,
    type: Optional[str] = None,
    startTime: Optional[int] = None,
    endTime: Optional[int] = None,
) -> dict[str, list[str]]:
    if count < 0 or count > 100:
        raise HTTPException(status_code=400, detail="count must be between 0 and 100")

    match_ids = await riot_client.get_match_history_ids(
        puuid=puuid,
        start=start,
        count=count,
        queue=queue,
        type_=type,
        start_time=startTime,
        end_time=endTime,
    )
    return {"matchIds": match_ids}


@router.get("/match-details/{match_id}")
async def get_match_details(match_id: str, force_refresh: bool = False) -> dict[str, Any]:
    cache_key = f"match-details:{match_id}"

    if not force_refresh:
        cached_value = await cache_client.get_json(cache_key)
        if cached_value is not None:
            return {"data": cached_value, "source": "cache"}

    match_details = await riot_client.get_match_details(match_id=match_id)
    await cache_client.set_json(
        key=cache_key,
        value=match_details,
        ttl_seconds=settings.match_details_cache_ttl_seconds,
    )

    return {"data": match_details, "source": "riot"}


@router.get("/match-cards/{puuid}")
async def get_match_cards(
    puuid: str,
    count: int = 5,
    force_refresh: bool = False,
) -> dict[str, Any]:
    if count < 1 or count > 20:
        raise HTTPException(status_code=400, detail="count must be between 1 and 20")

    match_ids = await riot_client.get_match_history_ids(
        puuid=puuid,
        start=0,
        count=count,
        queue=None,
        type_=None,
        start_time=None,
        end_time=None,
    )

    cards: list[dict[str, Any]] = []
    source_by_match: dict[str, str] = {}

    for match_id in match_ids:
        cache_key = f"match-details:{match_id}"

        match_data = None
        source = "riot"
        if not force_refresh:
            match_data = await cache_client.get_json(cache_key)
            if match_data is not None:
                source = "cache"

        if match_data is None:
            match_data = await riot_client.get_match_details(match_id=match_id)
            await cache_client.set_json(
                key=cache_key,
                value=match_data,
                ttl_seconds=settings.match_details_cache_ttl_seconds,
            )

        card = await _build_match_card(match_data=match_data, player_puuid=puuid)
        cards.append(card)
        source_by_match[match_id] = source

    return {
        "cards": cards,
        "sources": source_by_match,
    }
