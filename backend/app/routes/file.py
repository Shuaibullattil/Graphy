from fastapi import APIRouter
from fastapi import FastAPI,HTTPException,status,Depends
from app.db.mongodb import sheet_data_collection,graph_collection
from app.model.models import ExcelUploadRequest,FileResponse
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
from typing import List, Optional
from app.auth.auth import oauth2_scheme,decode_token
import logging


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
    
@router.get("/about")
async def get_file_details(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Email not found in token")

        files = sheet_data_collection.find({"email": email})

        result = []
        async for file in files:
            file_id = str(file["_id"])
            file_name = file.get("file", {}).get("fileName", "Unnamed")
            data = file.get("file", {}).get("data", [])
            labels = list(data[0].keys()) if data else []

            result.append({
                "file_id": file_id,
                "fileName": file_name,
                "labels": labels
            })

        return {"files": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving files: {str(e)}")
    
@router.get("/all-file-names")
async def get_file_details(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Email not found in token")

        files = sheet_data_collection.find({"email": email})

        result = []
        async for file in files:
            file_id = str(file["_id"])
            file_name = file.get("file", {}).get("fileName", "Unnamed")

            result.append({
                "file_id": file_id,
                "fileName": file_name,
            })

        return {"count":len(result),"files": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving files: {str(e)}")

@router.delete("/drop")
async def delete_my_file(file_id: str, token: str = Depends(oauth2_scheme)):
    try:
        # Validate token
        token_data = decode_token(token)
        email = token_data.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

        # Validate ObjectId
        try:
            obj_id = ObjectId(file_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file ID format")

        # Check if file exists and belongs to the user
        existing_file = await sheet_data_collection.find_one({"_id": obj_id, "email": email})
        if not existing_file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found or unauthorized access")

        # Delete file
        await sheet_data_collection.delete_one({"_id": obj_id, "email": email})
        await graph_collection.delete_many({"file_id": obj_id})

        return {"message": "File and associated graphs deleted successfully"}

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        logging.exception("Unexpected error while deleting file")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
