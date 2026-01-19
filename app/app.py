from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(title="Sift API")

@app.get("/")
def root():
    return { "message": "Sift API is online"}
   