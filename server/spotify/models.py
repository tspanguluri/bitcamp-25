from pydantic import BaseModel
from typing import List

class TrackArtistPair(BaseModel):
    track: str
    artist: str

class TrackArtistList(BaseModel):
    listings: List[TrackArtistPair]

