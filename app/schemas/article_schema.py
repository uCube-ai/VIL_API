from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ArticleCreate(BaseModel):
    universal_id: UUID
    vil_id: int
    article_date: datetime | None = None
    summary: str | None = None
    author: str | None = None
    file_path: str
    created_dt: datetime | None = None
    updated_dt: datetime | None = None

# --- This schema is no longer used by the upload endpoint but can be kept for other potential uses ---
class ArticleResponse(BaseModel):
    pass