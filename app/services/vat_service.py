from datetime import datetime

from app.services.base import BaseDataProcessingService
from database.crud import vat_crud
from app.schemas.vat_schema import VATCreate


class VATService(BaseDataProcessingService):
    def __init__(self):
        super().__init__(
            crud_model=vat_crud.vat,
            storage_dir="vat",
            file_suffix="vat.json",
            pk_field_name="case_id"
        )

    def _prepare_initial_data(self, item: VATCreate, ingestion_time: datetime, file_storage_path: str) -> dict:
        """
        Maps the VATCreate schema to the VAT model fields.
        """
        return {
            "vil_id": item.vil_id,
            "prod_id": item.prod_id,
            "prod_name": item.prod_name,
            "sub_prod_id": item.sub_prod_id,
            "sub_prod_name": item.sub_prod_name,
            "sub_subprod_id": item.sub_subprod_id,
            "state_id": item.state_id,
            "circular_date": item.circular_date,
            "eq_citation": item.eq_citation,
            "circular_no": item.circular_no,
            "case_no": item.case_no,
            "order_no": item.order_no,
            "judge_name": item.judge_name,
            "cir_subject": item.cir_subject,
            "html_file_path": item.file_path,
            "party_name": item.party_name,
            "created_dt": item.created_dt,
            "updated_dt": item.updated_dt,
            "ingestion_dt": ingestion_time,
            "file_storage_path": file_storage_path
        }

vat_service = VATService()