# pip install fastapi "uvicorn[standard]"
# uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello suckas!"}