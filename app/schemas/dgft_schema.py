from pydantic import BaseModel
from datetime import datetime

class DGFTCreate(BaseModel):
    vil_id: str | None = None
    prod_id: str | None = None
    prod_name: str | None = None
    sub_prod_id: str | None = None
    sub_prod_name: str | None = None
    sub_subprod_id: str | None = None
    state_id: str | None = None
    circular_date: datetime | None = None
    circular_no: str
    cir_subject: str | None = None
    file_path: str
    created_dt: datetime | None = None
    updated_dt: datetime | None = None

# --- This schema is no longer used by the upload endpoint but can be kept for other potential uses ---
class DGFTResponse(BaseModel):
    pass
