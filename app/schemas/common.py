from pydantic import BaseModel
from typing import List, Dict


class UploadSuccessResponse(BaseModel):
    message: str
    processed_items: List[str]
    failed_items: List[Dict[str, str]] = []