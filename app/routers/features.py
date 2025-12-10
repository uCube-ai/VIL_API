from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_router
from app.services.features_service import features_service
from app.schemas.features_schema import FeaturesCreate


features_config = RouterConfig(
    table_name="features",
    pydantic_schema=FeaturesCreate,
    service=features_service,
    pk_field_name="feature_id",
    entity_name_singular="Feature",
    entity_name_plural="Features"
)

# 2. Create the router by calling the factory
router = create_router(config=features_config)