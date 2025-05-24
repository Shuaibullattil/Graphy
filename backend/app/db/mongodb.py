from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os

# MongoDB connection settings
uri = "mongodb+srv://shuaibullattil7768:WtMhPfFKO9Dr5opo@sheetdata.tetsjo7.mongodb.net/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(uri)
db = client["Graphy_Base"]
sheet_data_collection = db["user_sheet_data"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



