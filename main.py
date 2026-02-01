from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Gacha(BaseModel):
    game: str
    target_pulls: int
    

@app.get("/")
def read_root():
    return {"Hello": "World"}
