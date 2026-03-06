from fastapi import APIRouter

from app.api.v1.endpoints import matches, summoner

api_router = APIRouter()
api_router.include_router(summoner.router, tags=["summoner"])
api_router.include_router(matches.router, tags=["matches"])
