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

    def _prepare_initial_data(self, item: FeaturesCreate, ingestion_time: datetime) -> dict:
        """
        Maps the FeaturesCreate schema to the Features model fields.
        """
        return {
            "feature_date": item.feature_date,
            "subject": item.subject,
            "summary": item.summary,
            "created_dt": item.created_dt,
            "updated_dt": item.updated_dt,
            "html_file_path": item.file_path,
            "file_storage_path": "",  # Placeholder
            "ingestion_dt": ingestion_time
        }

features_service = FeaturesService()