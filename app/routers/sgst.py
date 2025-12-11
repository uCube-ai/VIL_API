from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_router
from app.services.sgst_service import sgst_service
from app.schemas.sgst_schema import SGSTCreate


sgst_config = RouterConfig(
    table_name="casedata_sgst",
    pydantic_schema=SGSTCreate,
    service=sgst_service,
    pk_field_name="case_id",
    entity_name_singular="SGST Case",
    entity_name_plural="SGST Cases"
)

# 2. Create the router by calling the factory
router = create_router(config=sgst_config)