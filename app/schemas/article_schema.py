from pydantic import BaseModel
from datetime import datetime

class ArticleCreate(BaseModel):
    article_date: datetime
    summary: str
    author: str
    file_data: str
    file_path: str  # This will map to our 'html_file_path' model field
    created_dt: datetime
    updated_dt: datetime

# This schema defines the data we will return in the API response.
# We don't want to send the massive 'file_data' back.
class ArticleResponse(BaseModel):
    article_id: int
    article_date: datetime | None
    summary: str | None
    author: str | None
    html_file_path: str
    file_storage_path: str # We include the new path we created
    created_dt: datetime | None

    class Config:
        # This allows Pydantic to read data from ORM models (like our SQLAlchemy Article model)
        from_attributes = True