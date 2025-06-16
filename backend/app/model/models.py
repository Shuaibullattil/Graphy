from pydantic import BaseModel,EmailStr
from typing import List, Dict, Any
from datetime import datetime

class SheetData(BaseModel):
    fileName: str
    sheetName: str
    data: List[Dict[str, Any]]  # Rows as dictionaries

class FileResponse(BaseModel):
    fileName: str
    sheetName: str
    uploaded_at: datetime
    data: List[dict]  # or your specific data structure

class ExcelUploadRequest(BaseModel):
    files: List[SheetData]

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    accountType: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FileToGraph(BaseModel):
    name: str
    file_id: str
    sheetName: str
    labels: List[str]


class Dashboard(BaseModel):
    name: str
    graphs : List[str]