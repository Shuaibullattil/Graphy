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
from app.utils.extractLabelData import extract_fields


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


@router.get("/mygraphs")
async def get_all_my_graph(token: str = Depends(oauth2_scheme)):
    try:
        # Decode token to extract user email
        token_data = decode_token(token)
        email = token_data.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token: email not found")

        # Find all graphs owned by this user
        cursor = graph_collection.find({"owner": email})
        results = []

        async for graph in cursor:
            try:
                owner = graph.get("owner")
                labels = graph.get("labels", [])
                file_id = graph.get("file_id")
                graph_name = graph.get("graph_id")

                if not file_id:
                    continue  # skip if no file_id

                # Find the related file document
                file_doc = await sheet_data_collection.find_one({"_id": ObjectId(file_id)})
                if not file_doc:
                    continue  # skip if file not found

                file_data = file_doc.get("file", {}).get("data", [])
                graph_data = extract_fields(file_data, labels)

                result = {
                    "owner": owner,
                    "labels": labels,
                    "graph_name": graph_name,
                    "graph_data": graph_data
                }
                results.append(result)

            except Exception as inner_error:
                # Log or skip individual failed graph
                continue

        return {
            "message": "Your graph data is here",
            "data": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving graphs: {str(e)}")
