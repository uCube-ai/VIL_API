from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_router
from app.services.ce_service import ce_service
from app.schemas.ce_schema import CECreate


ce_config = RouterConfig(
    table_name="casedata_ce",
    pydantic_schema=CECreate,
    service=ce_service,
    pk_field_name="case_id",
    entity_name_singular="CE Case",
    entity_name_plural="CE Cases"
)

# 2. Create the router by calling the factory
router = create_router(config=ce_config)