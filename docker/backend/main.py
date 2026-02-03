from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password123@localhost:27017")
client = MongoClient(MONGO_URI)
db = client["guestbook"]
names_collection = db["names"]


class NameEntry(BaseModel):
    name: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/names")
def add_name(entry: NameEntry):
    if not entry.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    names_collection.insert_one({"name": entry.name.strip()})
    return {"message": "Name added", "name": entry.name.strip()}


@app.get("/api/names")
def get_names():
    names = list(names_collection.find({}, {"_id": 0, "name": 1}))
    return {"names": [n["name"] for n in names]}
