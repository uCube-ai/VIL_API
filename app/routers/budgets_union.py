from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_upload_router
from app.services.budgets_union_service import budgets_union_service
from app.schemas import budgets_union_schema


article_config = RouterConfig(
    table_name="budgets_union",
    pydantic_schema=budgets_union_schema.BudgetsUnionCreate,
    service=budgets_union_service,
    pk_field_name="circular_id",
    entity_name_singular="Budget Union file",
    entity_name_plural="Budget Union files"
)

# 2. Create the router by calling the factory
router = create_upload_router(config=article_config)