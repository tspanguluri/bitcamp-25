from fastapi import APIRouter, Query, HTTPException
import os
import httpx
import base64

router = APIRouter()

@router.get("/info")
async def info():
    return {"message": os.getenv("SPOTIFY_CLIENT")}



async def get_access_token():
    SPOTIFY_CLIENT = os.getenv("SPOTIFY_CLIENT")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    print(SPOTIFY_CLIENT, SPOTIFY_CLIENT_SECRET)
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

@router.get("/search-track")
async def search_track(track: str = Query(...), artist: str = Query(...)):
    token = await get_access_token()

    headers = {"Authorization": f"Bearer {token}"}
    query = f"track:{track} artist:{artist}"

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
        return {"spotify_id": track_info["id"]}



#takes the name and artist, and retrives the spotifyID

#takes the spotifyID and retrieves all the info we want about the song