
from datetime import datetime

from app.services.base import BaseDataProcessingService
from database.crud import sgst_crud
from app.schemas.sgst_schema import SGSTCreate


class SGSTService(BaseDataProcessingService):
    def __init__(self):
        super().__init__(
            crud_model=sgst_crud.sgst,
            storage_dir="sgst",
            file_suffix="sgst.json",
            pk_field_name="case_id"
        )

    def _prepare_initial_data(self, item: SGSTCreate, ingestion_time: datetime) -> dict:
        """
        Maps the SGSTCreate schema to the SGST model fields.
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
            "section_no": item.section_no,
            "rule_no": item.rule_no,
            "igst_section_no": item.igst_section_no,
            "igst_rule_no": item.igst_rule_no,
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

sgst_service = SGSTService()