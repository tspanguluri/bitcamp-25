from fastapi import APIRouter, Query, HTTPException, Request
from fastapi.responses import RedirectResponse
import os
import httpx
import base64
from spotify.models import TrackArtistList, SongSpotifyURIs
from urllib.parse import urlencode

router = APIRouter()

SPOTIFY_CLIENT = os.getenv("SPOTIFY_CLIENT")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

@router.get("/info")
async def info():
    return {"message": os.getenv("SPOTIFY_CLIENT")}



async def get_access_token():
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
                "spotify_uri": track_info["uri"],
                "images": track_info["album"]["images"],
                "duration_ms": track_info["duration_ms"]

            })
            # json_lst.append(track_info)
    return json_lst

@router.get("/login")
def login():
    SCOPES = "user-read-private user-read-email playlist-modify-private playlist-modify-public"

    params = {
        "client_id": SPOTIFY_CLIENT,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES
    }
    url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()
        token_data = response.json()

    return {
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"],
        "expires_in": token_data["expires_in"],
        "token_type": token_data["token_type"]
    }


@router.post("/export-playlist")
async def export_playlist(songSpotifyURIs: SongSpotifyURIs):
    name = "Bitcamp Playlist"
    public = True
    collaborative = False
    description = "placeholder"

    token = await get_access_token()
    # print("token: ", token)

    authorization_token = os.getenv("AUTHORIZATION_TOKEN")

    headers = {"Authorization": f"Bearer {authorization_token}"}
    #required: user_id
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.spotify.com/v1/me",
            headers=headers
        )
        resp.raise_for_status()
        items = resp.json()

        id = items["id"]

    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {authorization_token}",
        "Content-Type": "application/json"
    }
    data = {
        "name": name,
        "description": description,
        "public": public
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=data, headers=headers)
        res.raise_for_status()
        response = res.json()
        playlist_id = response["id"]

    
    headers = {
        "Authorization": f"Bearer {authorization_token}",
        "Content-Type": "application/json"
    }

    data = {
        # "uris": [
        #     "spotify:track:2TjnCxxQRYn56Ye8gkUKiW",
        # ],
        "uris": songSpotifyURIs.uris
    }

    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=data, headers=headers)
        res.raise_for_status()
        response = res.json()
        return response






        # response = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
        # response.raise_for_status()
        # token_data = response.json()