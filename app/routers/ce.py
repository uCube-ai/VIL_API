from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_upload_router
from app.services.ce_service import ce_service
from app.schemas import ce_schema


ce_config = RouterConfig(
    table_name="ce",
    pydantic_schema=ce_schema.CECreate,
    service=ce_service,
    pk_field_name="case_id",
    entity_name_singular="CE Case",
    entity_name_plural="CE Cases"
)

# 2. Create the router by calling the factory
router = create_upload_router(config=ce_config)