from fastapi import FastAPI

app = FastAPI()

@app.get("/greeting")
def hello_world():
    return {"message": "Hello World!"}