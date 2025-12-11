from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_router
from app.services.cu_service import cu_service
from app.schemas.cu_schema import CUCreate


cu_config = RouterConfig(
    table_name="casedata_cu",
    pydantic_schema=CUCreate,
    service=cu_service,
    pk_field_name="case_id",
    entity_name_singular="CU Case",
    entity_name_plural="CU Cases"
)

# 2. Create the router by calling the factory
router = create_router(config=cu_config)