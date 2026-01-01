from datetime import datetime

from app.services.base import BaseDataProcessingService
from database.crud import budgets_union_crud
from app.schemas.budgets_union_schema import BudgetsUnionCreate


class BudgetsUnionService(BaseDataProcessingService):
    def __init__(self):
        super().__init__(
            crud_model=budgets_union_crud.budget_union,
            storage_dir="budgets_union",
            file_suffix="budgetsunion.json",
            pk_field_name="circular_id"
        )

    def _prepare_initial_data(self, item: BudgetsUnionCreate, ingestion_time: datetime, file_storage_path: str) -> dict:
        """
        Maps the BudgetsUnionCreate schema to the BudgetsUnion model fields.
        """
        return {
            "universal_id": item.universal_id,
            "vil_id": item.vil_id,
            "circular_date": item.circular_date,
            "circular_no": item.circular_no,
            "cir_subject": item.cir_subject,
            "html_file_path": item.file_path,
            "created_dt": item.created_dt,
            "updated_dt": item.updated_dt,
            "file_storage_path": file_storage_path,
            "ingestion_dt": ingestion_time
        }

budgets_union_service = BudgetsUnionService()