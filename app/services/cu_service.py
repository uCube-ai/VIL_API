from datetime import datetime

from app.services.base import BaseDataProcessingService
from database.crud import cu_crud
from app.schemas.cu_schema import CUCreate


class CUService(BaseDataProcessingService):
    def __init__(self):
        super().__init__(
            crud_model=cu_crud.cu,
            storage_dir="cu",
            file_suffix="cu.json",
            pk_field_name="case_id"
        )

    def _prepare_initial_data(self, item: CUCreate, ingestion_time: datetime) -> dict:
        """
        Maps the CECreate schema to the CE model fields.
        """
        return {
            "vil_id": item.vil_id,
            "prod_id": item.prod_id,
            "prod_name": item.prod_name,
            "sub_prod_id": item.sub_prod_id,
            "sub_prod_name": item.sub_prod_name,
            "sub_subprod_id": item.sub_subprod_id,
            "circular_date": item.circular_date,
            "eq_citation": item.eq_citation,
            "circular_no": item.circular_no,
            "case_no": item.case_no,
            "order_no": item.order_no,
            "judge_name": item.judge_name,
            "cir_subject": item.cir_subject,
            "party_name": item.party_name,
            "html_file_path": item.file_path,
            "file_storage_path": "",
            "created_dt": item.created_dt,
            "updated_dt": item.updated_dt,
            "ingestion_dt": ingestion_time
        }

cu_service = CUService()