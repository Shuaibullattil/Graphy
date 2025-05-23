from pydantic import BaseModel
from typing import List, Dict, Any

class SheetData(BaseModel):
    fileName: str
    sheetName: str
    data: List[Dict[str, Any]]  # Rows as dictionaries

class ExcelUploadRequest(BaseModel):
    user_id: str
    username: str
    files: List[SheetData]
