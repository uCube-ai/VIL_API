from dataclasses import dataclass
from typing import Type
from pydantic import BaseModel

from app.services.base import BaseDataProcessingService

@dataclass
class RouterConfig:
    """
    A configuration class to hold the specific details for a generic upload router.
    """
    table_name: str
    
    # The Pydantic schema used to validate incoming data items
    pydantic_schema: Type[BaseModel]
    
    # The specific service instance that will process the data
    service: BaseDataProcessingService
    
    # The name of the primary key field on the SQLAlchemy model
    pk_field_name: str
    
    # A human-friendly name for the entity (singular, e.g., "Article")
    entity_name_singular: str
    
    # A human-friendly name for the entity (plural, e.g., "articles")
    entity_name_plural: str