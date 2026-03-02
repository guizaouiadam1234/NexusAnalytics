from fastapi import FastAPI, HTTPException
import httpx
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()
app = FastAPI()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

RIOT_ACCOUNT_BASE_URL = "https://europe.api.riotgames.com"

@app.get("/")
async def root():
    return {"message": "Welcome to Nexus Analytics!"}

@app.get("/summoner/{summoner_name}/{tag}")
async def get_summoner_info(summoner_name: str, tag: str):
    # Placeholder for summoner information retrieval logic
    encoded_summoner_name = quote(summoner_name)
    encoded_tag = quote(tag)
    url = f"{RIOT_ACCOUNT_BASE_URL}/riot/account/v1/accounts/by-riot-id/{encoded_summoner_name}/{encoded_tag}"
    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Request error: {str(exc)}")
    if response.status_code == 200:
        data = response.json()

        return {
            "puuid": data.get("puuid"),
            "gameName": data.get("gameName"),
            "tagLine": data.get("tagLine")
        }
    elif response.status_code == 400:
        raise HTTPException(status_code=400, detail="Bad request to Riot API")

    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized – check Riot API key")

    elif response.status_code == 403:
        raise HTTPException(status_code=403, detail="Forbidden – invalid or expired API key")

    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Account not found")

    elif response.status_code == 429:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )