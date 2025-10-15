from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_upload_router
from app.services.st_service import st_service
from app.schemas import st_schema


st_config = RouterConfig(
    table_name="st",
    vil_table_name="cs",
    pydantic_schema=st_schema.STCreate,
    service=st_service,
    pk_field_name="case_id",
    entity_name_singular="ST Case",
    entity_name_plural="ST Cases"
)

# 2. Create the router by calling the factory
router = create_upload_router(config=st_config)