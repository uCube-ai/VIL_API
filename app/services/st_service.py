from datetime import datetime

from app.services.base import BaseDataProcessingService
from database.crud import st_crud
from app.schemas.st_schema import STCreate


class STService(BaseDataProcessingService):
    def __init__(self):
        super().__init__(
            crud_model=st_crud.st,
            storage_dir="st",
            file_suffix="st.json",
            pk_field_name="case_id"
        )

    def _prepare_initial_data(self, item: STCreate, ingestion_time: datetime) -> dict:
        """
        Maps the STCreate schema to the ST model fields.
        """
        return {
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

st_service = STService()