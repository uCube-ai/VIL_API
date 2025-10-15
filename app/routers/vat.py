from app.routers.router_config import RouterConfig
from app.routers.generic_router_factory import create_upload_router
from app.services.vat_service import vat_service
from app.schemas import vat_schema


vat_config = RouterConfig(
    table_name="vat",
    pydantic_schema=vat_schema.VATCreate,
    service=vat_service,
    pk_field_name="case_id",
    entity_name_singular="VAT Case",
    entity_name_plural="VAT Cases"
)

# 2. Create the router by calling the factory
router = create_upload_router(config=vat_config)