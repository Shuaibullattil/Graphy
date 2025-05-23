
from fastapi import FastAPI,HTTPException
from db import sheet_data_collection
from datetime import datetime
from models import ExcelUploadRequest

# uri = "mongodb+srv://shuaibullattil7768:WtMhPfFKO9Dr5opo@sheetdata.tetsjo7.mongodb.net/"

# # Create a new client and connect to the server
# client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
# db = client["Graphy_Base"]
# sheet_data_collection = db["user_sheet_data"]



app = FastAPI()

#all apis here
# main.py

@app.post("/hello")
async def say_hello():
    message = {"message": "shuaib Hello!"}

    # Save to MongoDB
    result = await sheet_data_collection.insert_one(message)

    return {
        "message": message["message"],
        "inserted_id": str(result.inserted_id)
    }

@app.post("/upload-excel")
async def upload_excel(payload: ExcelUploadRequest):
    try:
        user_id = payload.user_id
        username = payload.username
        files_data = payload.files

        uploaded_at = datetime.utcnow()

        documents = []
        for file in files_data:
            doc = {
                "user_id": user_id,
                "username": username,
                "uploaded_at": uploaded_at,
                "file": {
                    "fileName": file.fileName,
                    "sheetName": file.sheetName,
                    "data": file.data
                }
            }
            documents.append(doc)

        await sheet_data_collection.insert_many(documents)

        return {
            "message": "Files uploaded and saved successfully",
            "files_saved": len(documents)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while uploading files: {str(e)}"
        )

#get all upload files
@app.get("/get-all-uploads")
async def get_all_uploads():
    try:
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "user_id": "$user_id",
                        "username": "$username"
                    },
                    "files_uploaded": {"$sum": 1},
                    "files": {"$push": "$file"}
                }
            }
        ]

        results = await sheet_data_collection.aggregate(pipeline).to_list(length=None)

        # Format results nicely
        users_uploads = []
        for r in results:
            users_uploads.append({
                "user_id": r["_id"]["user_id"],
                "username": r["_id"]["username"],
                "files_uploaded": r["files_uploaded"],
                "files": r["files"]
            })

        return users_uploads

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch uploads: {str(e)}")