from pydantic import BaseModel
from datetime import datetime

class BudgetsUnionCreate(BaseModel):
    vil_id: int
    circular_date: datetime | None = None
    circular_no: str
    cir_subject: str | None = None
    file_data: str | None = None
    file_path: str
    created_dt: datetime | None = None
    updated_dt: datetime | None = None

# --- This schema is no longer used by the upload endpoint but can be kept for other potential uses ---
class BudgetsUnionResponse(BaseModel):
    vil_id: str | None = None
    budgets_union_id: int
    circular_date: datetime | None
    circular_no: str | None
    cir_subject: str | None
    html_file_path: str
    file_storage_path: str
    created_dt: datetime | None
    updated_dt: datetime | None

    class Config:
        from_attributes = True
