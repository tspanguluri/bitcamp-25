from fastapi import APIRouter, status, Query
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import re
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

router = APIRouter()
# dotenv_path = Path(__file__).resolve().parents[2] / ".env"
# loaded = load_dotenv(dotenv_path=dotenv_path)
load_dotenv()
api_keyv = os.getenv("OPENAI_API_KEY")
# spotify_client_id = os.getenv("SPOTIFY_CLIENT")
# spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# auth_manager = SpotifyClientCredentials(
#     client_id=spotify_client_id,
#     client_secret=spotify_client_secret
# )
# sp = spotipy.Spotify(auth_manager=auth_manager)

# def get_recommendations(genre: str, artist_name: str = None, min_year: int = None, max_year: int = None):
#     try:
#         kwargs = {"limit": 100}

#         if genre:
#             kwargs["seed_genres"] = [genre]

#         if artist_name:
#             search = sp.search(q=artist_name, type="artist", limit=1)
#             if search["artists"]["items"]:
#                 artist_id = search["artists"]["items"][0]["id"]
#                 kwargs["seed_artists"] = [artist_id]

#         # Spotify doesn't support min_year/max_year directly
#         # We'll simulate year filtering later, so don't pass them here

#         recommendations = sp.recommendations(**kwargs)
#         filtered_tracks = []

#         for track in recommendations["tracks"]:
#             release_year = int(track["album"].get("release_date", "1900")[:4])
#             if (min_year and release_year < min_year) or (max_year and release_year > max_year):
#                 continue
#             filtered_tracks.append({
#                 "track": track["name"],
#                 "artist": track["artists"][0]["name"]
#             })

#         return filtered_tracks
#     except Exception as e:
#         return [{"track": "error", "artist": str(e)}]

@router.get(
    "/chatgpt",
    status_code=200,
    # response_model=#Create Response Model
)
def generate_chatgpt_stuff(mood: str=Query(...), song_num: int=Query(...), genres: str=Query(...),
    artist: str = Query(None),
    min_year: int = Query(None),
    max_year: int = Query(None)):
   client = OpenAI(api_key=api_keyv)
   #mood = "happy"

   genre = genres.split(",")[0].strip().lower()  
#    spotify_songs = get_recommendations(genre, artist, min_year, max_year)
#    seed_song_list = ", ".join([f"{s['track']} by {s['artist']}" for s in spotify_songs])
#    print(seed_song_list)
   this_input = (
    # f"Here are 15 real Spotify songs from the genre '{genre}': {seed_song_list}. "
    # f"Now recommend {song_num} songs that align with the mood '{mood}' and genre '{genre}'. And use a few songs from the list above from Spotify.  "
    f"Recommend {song_num} songs that align with the mood \'{mood}\' and genre \'{genre}\'. And generate three colors which align with the mood, and give me the colors' hex values."
    f"Return ONLY a valid JSON object in the following schema:\n\n"
    f"{{\n"
    f"  \"songs\": [\n"
    f"    {{\"track\": string, \"artist\": string}},\n"
    f"    ...\n"
    f"  ],\n"
    f"  \"colors\": [\n"
    f"    string (hex value),\n"
    f"    string (hex value),\n"
    f"    string (hex value)\n"
    f"  ]\n"
    f"}}\n\n"
    f"Do not include any markdown formatting like ```json or explanations. "
    f"Only return the JSON object exactly as specified."
)
   response = client.responses.create(
      model = "gpt-4o",
      input = this_input
    )
   raw_output = response.output_text
   cleaned = re.sub(r"```json|```", "", raw_output).strip()
   try:
        parsed_json = json.loads(cleaned)
   except json.JSONDecodeError as e:
        return {"error": "Failed to parse JSON", "details": str(e), "raw": raw_output}
   return parsed_json

   
   





