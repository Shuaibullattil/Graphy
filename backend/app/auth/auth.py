from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError,ExpiredSignatureError
from datetime import datetime, timedelta
from app.db.mongodb import users_collection, hash_password, verify_password
from app.model.models import UserCreate, UserLogin
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register")
async def register(user: UserCreate):
    print("Incoming email:", user.email)
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(user.password)
    
    # Insert user
    await users_collection.insert_one({
        "name": user.name,
        "email": user.email, 
        "password": hashed,
        "accountType": user.accountType
    })
    
    # Create token with correct syntax
    token = create_token({"sub": user.email})
    
    # Return user data along with token
    return {
        "msg": "User registered successfully",
        "token": token,
        "user": {
            "name": user.name,
            "email": user.email,
            "accountType": user.accountType
        }
    }


@router.post("/login")
async def login(data: UserLogin):
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user["email"]})
    return {"token": token, "token_type": "bearer"}

@router.get("/me")
async def read_me(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)  # Will raise HTTPException if invalid or expired
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = await users_collection.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"email": user["email"], "name": user.get("name")}