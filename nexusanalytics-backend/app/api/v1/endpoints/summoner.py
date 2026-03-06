from fastapi import APIRouter

from app.services.riot.client import riot_client

router = APIRouter()


@router.get("/summoner/{summoner_name}/{tag}")
async def get_summoner_info(summoner_name: str, tag: str) -> dict[str, str | None]:
    data = await riot_client.get_account_by_riot_id(summoner_name=summoner_name, tag=tag)
    return {
        "puuid": data.get("puuid"),
        "gameName": data.get("gameName"),
        "tagLine": data.get("tagLine"),
    }
