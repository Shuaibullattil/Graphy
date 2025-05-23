from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection settings
uri = "mongodb+srv://shuaibullattil7768:WtMhPfFKO9Dr5opo@sheetdata.tetsjo7.mongodb.net/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(uri)
db = client["Graphy_Base"]
sheet_data_collection = db["user_sheet_data"]



