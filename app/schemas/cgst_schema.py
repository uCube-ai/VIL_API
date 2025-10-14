from pydantic import BaseModel
from datetime import datetime

class CGSTCreate(BaseModel):

    prod_id: str
    prod_name: str
    sub_prod_id: str
    sub_prod_name: str
    sub_subprod_id: str
    circular_date: datetime
    circular_no: str
    cir_subject: str
    file_data: str
    file_path: str
    created_dt: datetime
    updated_dt: datetime

# --- This schema is no longer used by the upload endpoint but can be kept for other potential uses ---
class CGSTResponse(BaseModel):
    pass
