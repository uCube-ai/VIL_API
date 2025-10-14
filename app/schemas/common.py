from pydantic import BaseModel
from typing import List


class UploadSuccessResponse(BaseModel):
    message: str
    processed_items: List[str]