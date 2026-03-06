from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="Nexus Analytics API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root() -> dict[str, str]:
        return {"message": "Welcome to Nexus Analytics!"}

    app.include_router(api_router, prefix="/api/v1")
    app.include_router(api_router)
    return app


app = create_app()
