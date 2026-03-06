from fastapi import HTTPException
import httpx


RIOT_ERROR_MAPPING = {
    400: "Bad request to Riot API",
    401: "Unauthorized – check Riot API key",
    403: "Forbidden – invalid or expired API key",
    404: "Data not found",
    405: "Method not allowed",
    415: "Unsupported media type",
    429: "Rate limit exceeded",
    500: "Internal server error",
    502: "Bad gateway",
    503: "Service unavailable",
    504: "Gateway timeout",
}


def raise_for_riot_response(response: httpx.Response) -> None:
    if response.status_code < 400:
        return

    raise HTTPException(
        status_code=response.status_code,
        detail=RIOT_ERROR_MAPPING.get(response.status_code, response.text),
    )
