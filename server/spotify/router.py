from fastapi import APIRouter, Query, HTTPException
import os
import httpx
import base64
from spotify.models import TrackArtistList

router = APIRouter()

@router.get("/info")
async def info():
    return {"message": os.getenv("SPOTIFY_CLIENT")}



async def get_access_token():
    SPOTIFY_CLIENT = os.getenv("SPOTIFY_CLIENT")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    auth_str = f"{SPOTIFY_CLIENT}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    async with httpx.AsyncClient() as client:
        resp = await client.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
        resp.raise_for_status()
        return resp.json()["access_token"]

@router.post("/search-track")
async def search_track(trackArtistList: TrackArtistList):
    print("track:", trackArtistList)
    print("entering get access token")
    token = await get_access_token()
    print("exiting get access token")

    headers = {"Authorization": f"Bearer {token}"}


    json_lst = []
    for listing in trackArtistList.listings:
        query = f"track:{listing.track} artist:{listing.artist}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.spotify.com/v1/search",
                params={"q": query, "type": "track", "limit": 1},
                headers=headers,
            )
            resp.raise_for_status()
            items = resp.json()["tracks"]["items"]
            if not items:
                raise HTTPException(status_code=404, detail="Track not found")
            track_info = items[0]
            json_lst.append( {
                "track": track_info["name"],
                "artist": ", ".join(artist["name"] for artist in track_info["artists"]),
                "spotify_id": track_info["id"],
                "spotify_url": track_info["external_urls"]["spotify"],
                "images": track_info["album"]["images"],
                "duration_ms": track_info["duration_ms"]
            })
    return json_lst