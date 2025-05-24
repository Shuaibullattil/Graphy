from fastapi import APIRouter, Form, HTTPException, status
from auth.auth import create_access_token

router = APIRouter()

# Dummy credentials - Replace with real DB check
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username != VALID_USERNAME or password != VALID_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}