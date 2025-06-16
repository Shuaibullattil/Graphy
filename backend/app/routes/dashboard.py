from fastapi import APIRouter
from fastapi import FastAPI,HTTPException,status,Depends
from app.db.mongodb import sheet_data_collection,graph_collection,dashboard_collection
from app.model.models import Dashboard
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
from typing import List, Optional
from app.auth.auth import oauth2_scheme,decode_token
import logging
from bson.errors import InvalidId


router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_new_dashboard(
    payload: Dashboard,
    token: str = Depends(oauth2_scheme)
):
    try:
        # Decode the JWT and extract user info
        token_data = decode_token(token)
        email = token_data.get("sub")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized: Invalid token or email not found"
            )

        # Validate dashboard data
        if not payload.name or not isinstance(payload.graphs, list):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payload: 'name' must be a string and 'graphs' must be a list of graph IDs"
            )

        dashboard_doc = {
            "name": payload.name,
            "graphs": payload.graphs,
            "owner": email,
        }

        result = await dashboard_collection.insert_one(dashboard_doc)

        return {
            "message": "Dashboard created successfully",
            "dashboard_id": str(result.inserted_id)
        }

    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )