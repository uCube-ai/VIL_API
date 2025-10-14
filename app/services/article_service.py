from datetime import datetime

from app.services.base import BaseDataProcessingService
from database.crud import article_crud
from app.schemas.article_schema import ArticleCreate


class ArticleService(BaseDataProcessingService):
    def __init__(self):
        super().__init__(
            crud_model=article_crud.article,
            storage_dir="articles",
            file_suffix="article.json",
            pk_field_name="article_id"
        )

    def _prepare_initial_data(self, item: ArticleCreate, ingestion_time: datetime) -> dict:
        """
        Maps the ArticleCreate schema to the Article model fields.
        """
        return {
            "article_date": item.article_date,
            "summary": item.summary,
            "author": item.author,
            "created_dt": item.created_dt,
            "updated_dt": item.updated_dt,
            "html_file_path": item.file_path,
            "file_storage_path": "",  # Placeholder
            "ingestion_dt": ingestion_time
        }

article_service = ArticleService()