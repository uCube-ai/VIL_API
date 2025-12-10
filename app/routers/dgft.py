from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_router
from app.services.dgft_service import dgft_service
from app.schemas.dgft_schema import DGFTCreate


dgft_config = RouterConfig(
    table_name="dgft",
    pydantic_schema=DGFTCreate,
    service=dgft_service,
    pk_field_name="case_id",
    entity_name_singular="DGFT Case",
    entity_name_plural="DGFT Cases"
)

# 2. Create the router by calling the factory
router = create_router(config=dgft_config)