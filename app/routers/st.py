from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_router
from app.services.st_service import st_service
from app.schemas.st_schema import STCreate


st_config = RouterConfig(
    table_name="casedata_st",
    vil_table_name="cs",
    pydantic_schema=STCreate,
    service=st_service,
    pk_field_name="case_id",
    entity_name_singular="ST Case",
    entity_name_plural="ST Cases"
)

# 2. Create the router by calling the factory
router = create_router(config=st_config)