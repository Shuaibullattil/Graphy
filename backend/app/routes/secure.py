# routes/secure.py

from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/secure-data")
def secure_data(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user['sub']}! You have access."}
