# pip install fastapi "uvicorn[standard]"
# uvicorn main:app --reload OR fastapi dev main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from spotify import router as spotify

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http://localhost:[0-9]{4,5}",
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    ],
    allow_headers=["*"]
)

app.include_router(
    spotify.router,
    prefix="/spotify",
    tags="Spotify"
)

@app.get("/")
def read_root():
    return {"message": "Hello suckas!"}