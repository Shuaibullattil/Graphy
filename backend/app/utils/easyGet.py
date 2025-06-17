from bson import ObjectId
from fastapi import HTTPException, status
from typing import Dict
from app.db.mongodb import sheet_data_collection,graph_collection

def extract_fields(data: list[dict], fields: list[str]) -> list[dict]:
    """Dynamically extract specified fields from MongoDB-style data"""
    return [
        {
            field: int(value["$numberInt"]) if isinstance(value, dict) and "$numberInt" in value
                else int(value["$numberLong"]) if isinstance(value, dict) and "$numberLong" in value
                else value
            for field, value in entry.items()
            if field in fields
        }
        for entry in data
    ]



async def get_graph_details_by_id(graph_id: str) -> Dict:
    try:
        # Validate and convert graph_id to ObjectId
        if not ObjectId.is_valid(graph_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Graph ID format"
            )
        graph_obj_id = ObjectId(graph_id)

        # Step 1: Get the graph document
        graph = await graph_collection.find_one({"_id": graph_obj_id})
        if not graph:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Graph not found"
            )

        # Step 2: Get the file document using graph['file_id']
        file_id = graph.get("file_id")
        if not file_id or not ObjectId.is_valid(str(file_id)):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid file reference in graph"
            )
        file_data = await sheet_data_collection.find_one({"_id": ObjectId(str(file_id))})
        if not file_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File for graph data not found"
            )

        # Step 3: Extract relevant fields using the provided utility
        raw_data = file_data.get("file", {}).get("data", [])
        labels = graph.get("labels", [])
        extracted_data = extract_fields(raw_data, labels)

        # Step 4: Construct the response
        return {
            "graph_id": str(graph["_id"]),
            "name": graph.get("name"),
            "graph_type": graph.get("graph_id"),  # e.g., '001', '003'
            "labels": labels,
            "data": extracted_data,
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
