from pydantic import BaseModel
from datetime import datetime

class SGSTCreate(BaseModel):

    prod_id: str | None = None
    prod_name: str | None = None
    sub_prod_id: str | None = None
    sub_prod_name: str | None = None
    sub_subprod_id: str | None = None
    state_id: str | None = None
    circular_date: datetime | None = None
    eq_citation: str | None = None
    section_no: str | None = None
    rule_no: str | None = None
    igst_section_no: str | None = None
    igst_rule_no: str | None = None
    circular_no: str
    case_no: str | None = None
    order_no: str | None = None
    judge_name: str | None = None
    cir_subject: str | None = None
    file_data: str | None = None
    file_path: str
    party_name: str | None = None
    created_dt: datetime | None = None
    updated_dt: datetime | None = None

# --- This schema is no longer used by the upload endpoint but can be kept for other potential uses ---
class SGSTResponse(BaseModel):
    pass
