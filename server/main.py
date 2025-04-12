# pip install fastapi "uvicorn[standard]"
# uvicorn main:app --reload

from fastapi import FastAPI
from chatgpt import router as chatgpt
from fastapi.middleware.cors import CORSMiddleware

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
    chatgpt.router,
    prefix="/chatgpt",
    tags=["Chatgpt"]
)
@app.get("/")
def read_root():
    return {"message": "Hello suckas!"}