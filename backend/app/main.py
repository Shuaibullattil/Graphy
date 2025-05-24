
from fastapi import FastAPI,HTTPException
from app.routes import file,user,secure,login
from app.auth import auth
import uvicorn

# uri = "mongodb+srv://shuaibullattil7768:WtMhPfFKO9Dr5opo@sheetdata.tetsjo7.mongodb.net/"

# # Create a new client and connect to the server
# client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
# db = client["Graphy_Base"]
# sheet_data_collection = db["user_sheet_data"]



app = FastAPI()
app.include_router(file.router)
app.include_router(secure.router)
app.include_router(login.router)
app.include_router(auth.router,prefix="/auth")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

