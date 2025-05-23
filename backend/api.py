
from fastapi import FastAPI,HTTPException

import os
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb+srv://shuaibullattil7768:WtMhPfFKO9Dr5opo@sheetdata.tetsjo7.mongodb.net/"

# Create a new client and connect to the server
client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
db = client["Graphy_Base"]
sheet_data_collection = db["user_sheet_data"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.post("/add-user")
async def add_user(user: User):
    try:
        data = user.dict()
        result = await sheet_data_collection.insert_one(data)
        return {"message": "User added", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))