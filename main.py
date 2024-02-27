from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import quote_plus
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

username = quote_plus('ajmalhanee')
password = quote_plus('@$$B!t3OOF')

MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.7v4hno5.mongodb.net/?ssl=true"
MONGO_DB = "vlncy"
COLLECTION_NAME = "users"


class User(BaseModel):
    user_id: str
    user_zip: str
    user_age: int
    gender: str
    pref_distance: List[int]
    pref_age: List[int]
    user_matches: dict

# MongoDB Connection
def connect_to_mongo():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[MONGO_DB]
        yield db
    except ServerSelectionTimeoutError as err:
        raise HTTPException(status_code=500, detail="Failed to connect to database")
    

# Routes
@app.get("/")
async def read_root():
    return {"message": "Welcome to your FastAPI MongoDB app!"}


@app.get("/users/", response_model=List[User])
async def get_users(db=Depends(connect_to_mongo)):
    users_data = db[COLLECTION_NAME].find({}, {"_id": 0}) 
    users = [User(**user) for user in users_data]
    return users


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
