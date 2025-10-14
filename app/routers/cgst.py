from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_upload_router
from app.services.cgst_service import cgst_service
from app.schemas import cgst_schema


cgst_config = RouterConfig(
    table_name="cgst",
    pydantic_schema=cgst_schema.CGSTCreate,
    service=cgst_service,
    pk_field_name="case_id",
    entity_name_singular="CGST Case",
    entity_name_plural="CGST Cases"
)

# 2. Create the router by calling the factory
router = create_upload_router(config=cgst_config)