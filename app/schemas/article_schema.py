from pydantic import BaseModel
from datetime import datetime
from typing import List

class ArticleCreate(BaseModel):
    article_date: datetime
    summary: str
    author: str
    file_data: str
    file_path: str
    created_dt: datetime
    updated_dt: datetime

# --- This schema is no longer used by the upload endpoint but can be kept for other potential uses ---
class ArticleResponse(BaseModel):
    article_id: int
    article_date: datetime | None
    summary: str | None
    author: str | None
    html_file_path: str
    file_storage_path: str
    created_dt: datetime | None

    class Config:
        from_attributes = True

# This defines the structure of simplified success message.
class UploadSuccessResponse(BaseModel):
    message: str
    processed_articles: List[str]