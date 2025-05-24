
from fastapi import FastAPI,HTTPException
from app.routes import auth,file,user

# uri = "mongodb+srv://shuaibullattil7768:WtMhPfFKO9Dr5opo@sheetdata.tetsjo7.mongodb.net/"

# # Create a new client and connect to the server
# client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
# db = client["Graphy_Base"]
# sheet_data_collection = db["user_sheet_data"]



app = FastAPI()
app.include_router(file.router)


