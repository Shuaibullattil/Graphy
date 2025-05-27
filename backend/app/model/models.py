from pydantic import BaseModel,EmailStr
from typing import List, Dict, Any

class SheetData(BaseModel):
    fileName: str
    sheetName: str
    data: List[Dict[str, Any]]  # Rows as dictionaries

class ExcelUploadRequest(BaseModel):
    user_id: str
    username: str
    files: List[SheetData]

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    accountType: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str