from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_upload_router
from app.services.article_service import article_service
from app.schemas import article_schema


article_config = RouterConfig(
    table_name="articles",
    pydantic_schema=article_schema.ArticleCreate,
    service=article_service,
    pk_field_name="article_id",
    entity_name_singular="Article",
    entity_name_plural="articles"
)

# 2. Create the router by calling the factory
router = create_upload_router(config=article_config)