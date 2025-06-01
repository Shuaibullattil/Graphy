from fastapi import APIRouter
from fastapi import FastAPI,HTTPException,status,Depends
from app.db.mongodb import sheet_data_collection,graph_collection
from app.model.models import ExcelUploadRequest,FileResponse,FileToGraph
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId,errors as bson_errors
from typing import List, Optional
from app.auth.auth import oauth2_scheme,decode_token
from pymongo.errors import PyMongoError


router = APIRouter(prefix="/graph", tags=["graph"])

@router.post("/filetograph")
async def file_to_graph(payload: FileToGraph, token: str = Depends(oauth2_scheme)):
    try:
        token_data = decode_token(token)
        email = token_data.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token or missing email.")

        try:
            file_obj_id = ObjectId(payload.file_id)
        except bson_errors.InvalidId:
            raise HTTPException(status_code=400, detail="Invalid file_id format.")

        result_data = {
            "name": payload.name,
            "file_id": file_obj_id,
            "graph_id": payload.graph_id,
            "sheetName": payload.sheetName,
            "labels": payload.labels,
            "owner": email
        }

        insert_result = await graph_collection.insert_one(result_data)

        return {
            "message": "Graph data saved successfully",
            "graph_id": str(insert_result.inserted_id)
        }

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


