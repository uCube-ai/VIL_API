from pydantic import BaseModel
from datetime import datetime

class CECreate(BaseModel):

    prod_id: str
    prod_name: str
    sub_prod_id: str
    sub_prod_name: str
    sub_subprod_id: str
    circular_date: datetime
    eq_citation: str
    circular_no: str
    case_no: str
    order_no: str
    judge_name: str
    cir_subject: str
    file_data: str
    file_path: str
    party_name: str
    created_dt: datetime
    updated_dt: datetime

# --- This schema is no longer used by the upload endpoint but can be kept for other potential uses ---
class CEResponse(BaseModel):
    pass
