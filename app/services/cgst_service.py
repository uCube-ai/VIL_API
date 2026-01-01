from datetime import datetime

from app.services.base import BaseDataProcessingService
from database.crud import cgst_crud
from app.schemas.cgst_schema import CGSTCreate


class CGSTService(BaseDataProcessingService):
    def __init__(self):
        super().__init__(
            crud_model=cgst_crud.cgst,
            storage_dir="cgst",
            file_suffix="cgst.json",
            pk_field_name="case_id"
        )

    def _prepare_initial_data(self, item: CGSTCreate, ingestion_time: datetime, file_storage_path: str) -> dict:
        """
        Maps the CGSTCreate schema to the CGST model fields.
        """
        return {
            "universal_id": item.universal_id,
            "vil_id": item.vil_id,
            "prod_id": item.prod_id,
            "prod_name": item.prod_name,
            "sub_prod_id": item.sub_prod_id,
            "sub_prod_name": item.sub_prod_name,
            "sub_subprod_id": item.sub_subprod_id,
            "circular_date": item.circular_date,
            "circular_no": item.circular_no,
            "cir_subject": item.cir_subject,
            "html_file_path": item.file_path,
            "created_dt": item.created_dt,
            "updated_dt": item.updated_dt,
            "ingestion_dt": ingestion_time,
            "file_storage_path": file_storage_path
        }

cgst_service = CGSTService()