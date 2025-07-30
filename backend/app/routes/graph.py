from fastapi import APIRouter
from fastapi import FastAPI,HTTPException,status,Depends
from app.db.mongodb import sheet_data_collection,graph_collection,dashboard_collection
from app.model.models import ExcelUploadRequest,FileResponse,FileToGraph
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId,errors as bson_errors
from typing import List, Optional
from app.auth.auth import oauth2_scheme,decode_token
from pymongo.errors import PyMongoError
from app.utils.easyGet import extract_fields
import logging


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
                graph_id = str(graph.get("_id"))
                name = graph.get("name")
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
                    "graph_id": graph_id,
                    "name": name,
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


@router.get("/my-graph-preview")
async def get_my_graph_preview(
    name: str,
    file_id: str,
    sheetName: str,
    labels: str,  # comma-separated string
    graph_id: str,
    token: str = Depends(oauth2_scheme)
):
    try:
        # Decode and validate token
        token_data = decode_token(token)
        email = token_data.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired or invalid")

        # Parse labels from comma-separated string
        labels_list = [label.strip() for label in labels.split(',') if label.strip()]
        
        if not labels_list:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Labels cannot be empty")

        # Fetch file data
        document = await sheet_data_collection.find_one({"_id": ObjectId(file_id)})
        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        file_data = document.get("file", {}).get("data", [])
        if not file_data:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="File data is empty")

        # Extract graph data
        try:
            graph_data = extract_fields(file_data, labels_list)
        except Exception as e:
            logging.error(f"Error extracting fields: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to extract graph data")

        return {
            "name": name,
            "file_id": file_id,
            "sheetName": sheetName,
            "labels": labels_list,
            "graph_id": graph_id,
            "graph_data": graph_data,
        }

    except HTTPException as http_ex:
        raise http_ex  # Re-raise for FastAPI to handle cleanly

    except Exception as e:
        logging.exception("Unexpected error in get_my_graph_preview")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    

@router.delete("/drop")
async def delete_my_graph(graph_id: str, token: str = Depends(oauth2_scheme)):
    try:
        # Decode JWT and get user email
        token_data = decode_token(token)
        email = token_data.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

        # Validate ObjectId format
        try:
            obj_id = ObjectId(graph_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid graph ID format")

        # Check if the graph exists and belongs to the user
        existing_graph = await graph_collection.find_one({"_id": obj_id, "owner": email})
        if not existing_graph:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Graph not found or unauthorized access")

        # Delete the graph
        result = await graph_collection.delete_one({"_id": obj_id, "owner": email})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete graph")

        # Remove graph ID from all dashboards that include it
        await dashboard_collection.update_many(
            {"owner": email},
            {"$pull": {"graphs": graph_id}}  # Pull string ID, not ObjectId
        )

        return {"message": "Graph deleted successfully and dashboard references updated"}

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        logging.exception("Unexpected error while deleting graph")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
