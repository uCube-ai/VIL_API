from dataclasses import dataclass
from typing import Type, Optional
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

    # Actual name of the table in the json dump (to facilitate cases like cs - st)
    vil_table_name: Optional[str] = None

    def __post_init__(self):
        """
        STEP 2: This method is automatically called by the dataclass decorator
        after the initial __init__ has run.
        
        We use it here to set our intelligent default for vil_table_name.
        """
        if self.vil_table_name is None:
            self.vil_table_name = self.table_name
