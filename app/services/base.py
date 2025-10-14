import os
import json
import aiofiles
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)

class BaseDataProcessingService(ABC):
    """
    An abstract base class for data processing services.
    It encapsulates the transactional logic for:
    1. Creating a database record.
    2. Saving an associated file.
    3. Updating the record with the file path.
    """
    def __init__(self, crud_model, storage_dir: str, file_suffix: str, pk_field_name: str):
        self.crud = crud_model
        self.storage_dir = storage_dir
        self.file_suffix = file_suffix
        self.pk_field_name = pk_field_name

    @abstractmethod
    def _prepare_initial_data(self, item: BaseModel, ingestion_time: datetime) -> dict:
        """
        Abstract method to be implemented by child classes.
        This method is responsible for mapping the Pydantic schema fields
        to the SQLAlchemy model's fields.
        """
        pass

    async def process_and_create_item(self, db: Session, item: BaseModel, ingestion_time: datetime):
        """
        Handles the generic business logic of processing an item.
        """
        try:
            # 1. Prepare data using the child-specific implementation
            initial_data = self._prepare_initial_data(item=item, ingestion_time=ingestion_time)
            
            # 2. Call the generic CRUD create method
            db_obj = self.crud.create(db=db, obj_in=initial_data)

            # 3. File Saving Logic 
            pk_value = getattr(db_obj, self.pk_field_name, None)
            if not pk_value:
                raise Exception(f"Failed to retrieve PK '{self.pk_field_name}' after flushing the session.")
            
            new_filename = f"{pk_value}_{self.file_suffix}"
            target_dir = os.path.join(settings.STORAGE_PATH, self.storage_dir)
            os.makedirs(target_dir, exist_ok=True)
            file_storage_path = os.path.join(target_dir, new_filename)

            json_content_to_save = item.model_dump(mode='json')
            async with aiofiles.open(file_storage_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(json_content_to_save, indent=4))

            # 4. Update DB record with file path
            self.crud.update_path(db=db, db_obj=db_obj, path=file_storage_path)

            # 5. Finalize Transaction
            db.commit()
            db.refresh(db_obj)
            
            return db_obj

        except (SQLAlchemyError, IOError, Exception) as e:
            logger.error(f"Error processing item. Rolling back transaction. Error: {e}")
            db.rollback()
            raise