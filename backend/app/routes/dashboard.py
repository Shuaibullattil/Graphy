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
from app.utils.easyGet import get_graph_details_by_id
import asyncio


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
    
@router.get("/about", status_code=200)
async def get_my_dashboard_about(token: str = Depends(oauth2_scheme)):
    try:
        # Decode token to extract email
        token_data = decode_token(token)
        email = token_data.get("sub")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token."
            )

        # Query dashboards owned by this user
        cursor = dashboard_collection.find({"owner": email})

        dashboards = []
        async for dashboard in cursor:
            dashboards.append({
                "dashboard_id": str(dashboard.get("_id", "")),
                "name": dashboard.get("name", ""),
                "graphs": dashboard.get("graphs", [])
            })

        return {
            "message": "Dashboard data retrieved successfully.",
            "count": len(dashboards),
            "dashboard": dashboards
        }

    except HTTPException as http_err:
        # Re-raise FastAPI's own HTTP exceptions
        raise http_err

    except Exception as e:
        # Catch all other unhandled errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )
    
@router.get("/my/{dashboard_id}")
async def get_dashboard_by_id(dashboard_id: str, token: str = Depends(oauth2_scheme)):
    try:
        token_data = decode_token(token)
        email = token_data.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired or unauthorized")

        if not ObjectId.is_valid(dashboard_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid dashboard ID")

        dashboard_obj_id = ObjectId(dashboard_id)

        dashboard = await dashboard_collection.find_one({"_id": dashboard_obj_id, "owner": email})
        if not dashboard:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard not found or access denied")

        dashboard_name = dashboard.get("name", "")
        graph_ids = dashboard.get("graphs", [])
        if not isinstance(graph_ids, list):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid graph format in dashboard")

        # ✅ Use asyncio.gather to fetch all graph details in parallel
        tasks = [get_graph_details_by_id(graph_id) for graph_id in graph_ids]
        graph_details = await asyncio.gather(*tasks, return_exceptions=True)

        result = []
        for i, detail in enumerate(graph_details):
            if isinstance(detail, HTTPException):
                result.append({
                    "graph_id": graph_ids[i],
                    "error": detail.detail
                })
            else:
                result.append(detail)

        return {
            "dashboard_id": dashboard_id,
            "name": dashboard_name,
            "graph_count": len(result),
            "graphs": result
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    