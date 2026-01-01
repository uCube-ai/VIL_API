from datetime import datetime

from app.services.base import BaseDataProcessingService
from database.crud import features_crud
from app.schemas.features_schema import FeaturesCreate


class FeaturesService(BaseDataProcessingService):
    def __init__(self):
        super().__init__(
            crud_model=features_crud.features,
            storage_dir="features",
            file_suffix="feature.json",
            pk_field_name="feature_id"
        )

    def _prepare_initial_data(self, item: FeaturesCreate, ingestion_time: datetime, file_storage_path: str) -> dict:
        """
        Maps the FeaturesCreate schema to the Features model fields.
        """
        return {
            "universal_id": item.universal_id,
            "vil_id": item.vil_id,
            "feature_date": item.feature_date,
            "subject": item.subject,
            "summary": item.summary,
            "html_file_path": item.file_path,
            "created_dt": item.created_dt,
            "updated_dt": item.updated_dt,
            "ingestion_dt": ingestion_time,
            "file_storage_path": file_storage_path
        }

features_service = FeaturesService()