from fastapi import APIRouter
from fastapi import FastAPI,HTTPException,status,Depends
from app.db.mongodb import sheet_data_collection
from app.model.models import ExcelUploadRequest,FileResponse
from datetime import datetime
from bson import objectid
from typing import List, Optional
from app.auth.auth import oauth2_scheme,decode_token


router = APIRouter(prefix="/file", tags=["file"])

@router.post("/upload")
async def upload_excel(payload: ExcelUploadRequest,token: str = Depends(oauth2_scheme)):
    toke_data = decode_token(token)
    email = toke_data.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token payload") 
    try:
        files_data = payload.files

        uploaded_at = datetime.utcnow()

        documents = []
        for file in files_data:
            doc = {
                "email": email,
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
    
@router.get("/my", response_model=List[FileResponse])
async def get_user_files(
    token: str = Depends(oauth2_scheme)
    
):
    payload = decode_token(token)  # Will raise HTTPException if invalid or expired
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    try:
        # Find all documents matching the user's email
        cursor = sheet_data_collection.find({"email": email})
        
        # Convert MongoDB documents to response model
        files = []
        async for document in cursor:
            files.append({
                "fileName": document["file"]["fileName"],
                "sheetName": document["file"]["sheetName"],
                "uploaded_at": document["uploaded_at"],
                "data": document["file"]["data"]
            })
        
        return files

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving files: {str(e)}"
        )