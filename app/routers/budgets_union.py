from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_router
from app.services.budgets_union_service import budgets_union_service
from app.schemas.budgets_union_schema import BudgetsUnionCreate


article_config = RouterConfig(
    table_name="budgets_union",
    pydantic_schema=BudgetsUnionCreate,
    service=budgets_union_service,
    pk_field_name="circular_id",
    entity_name_singular="Budget Union file",
    entity_name_plural="Budget Union files"
)

# 2. Create the router by calling the factory
router = create_router(config=article_config)