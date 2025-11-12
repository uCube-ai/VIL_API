from pydantic import BaseModel
from datetime import datetime

class ArticleCreate(BaseModel):
    vil_id: int
    article_date: datetime | None = None
    summary: str | None = None
    author: str | None = None
    file_data: str | None = None
    file_path: str
    created_dt: datetime | None = None
    updated_dt: datetime | None = None

# --- This schema is no longer used by the upload endpoint but can be kept for other potential uses ---
class ArticleResponse(BaseModel):
    vil_id: str | None = None
    article_id: int
    article_date: datetime | None
    summary: str | None
    author: str | None
    html_file_path: str
    file_storage_path: str
    created_dt: datetime | None

    class Config:
        from_attributes = True
