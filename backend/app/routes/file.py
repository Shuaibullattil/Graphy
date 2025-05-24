from fastapi import APIRouter
from fastapi import FastAPI,HTTPException
from app.db.mongodb import sheet_data_collection
from app.model.models import ExcelUploadRequest
from datetime import datetime
from bson import objectid


router = APIRouter(prefix="/file", tags=["file"])

@router.post("/upload")
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

@router.get("/all")
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
                    "files": {
                        "$push": {
                            "_id": "$_id",       # keep ObjectId
                            "file": "$file"      # file info
                        }
                    }
                }
            }
        ]

        results = await sheet_data_collection.aggregate(pipeline).to_list(length=None)

        # Convert ObjectId to string before returning
        users_uploads = []
        for r in results:
            files = [
                {
                    "_id": str(f["_id"]),    # Convert ObjectId to string
                    "file": f["file"]
                }
                for f in r["files"]
            ]

            users_uploads.append({
                "user_id": r["_id"]["user_id"],
                "username": r["_id"]["username"],
                "files_uploaded": r["files_uploaded"],
                "files": files
            })

        return users_uploads

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch uploads: {str(e)}")