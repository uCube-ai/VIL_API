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
        # 1. Calculate File Path (Using vil_id instead of DB PK)
        new_filename = f"{item.vil_id}_{self.file_suffix}"
        target_dir = os.path.join(settings.STORAGE_PATH, self.storage_dir)
        os.makedirs(target_dir, exist_ok=True)
        file_storage_path = os.path.join(target_dir, new_filename)

        file_created = False

        try:
            # 2. File Saving Logic (Happens FIRST now)
            json_content_to_save = item.model_dump(mode='json')
            async with aiofiles.open(file_storage_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(json_content_to_save, indent=4))
            file_created = True

            # 3. Prepare data and Insert into DB
            initial_data = self._prepare_initial_data(
                item=item, 
                ingestion_time=ingestion_time, 
                file_storage_path=file_storage_path
            )
            
            db_obj = self.crud.create(db=db, obj_in=initial_data)

            # 4. Finalize Transaction
            db.commit()
            db.refresh(db_obj)
            
            return db_obj

        except (SQLAlchemyError, IOError, Exception) as e:
            logger.error(f"Error processing item vil_id {item.vil_id}. Rolling back transaction. Error: {e}")
            db.rollback()

            if file_created and os.path.exists(file_storage_path):
                try:
                    os.remove(file_storage_path)
                    logger.info(f"Cleaned up orphaned file: {file_storage_path}")
                except OSError as cleanup_error:
                    logger.critical(f"Failed to clean up file after DB error: {cleanup_error}")

            raise

    async def process_update_item(self, db: Session, item: BaseModel, ingestion_time: datetime):
        """
        It assumes the item exists and will skip (return None) if it doesn't.
        """
        try:
            # 1. Get the vil_id (which Pydantic has validated)
            item_vil_id = item.vil_id
            
            # 2. Find the existing database object
            db_obj = self.crud.get_by_vil_id(db=db, vil_id=item_vil_id)
            
            if not db_obj:
                # --- SKIP PATH ---
                logger.warning(f"Update skipped: Record with vil_id {item_vil_id} not found.")
                return None

            # --- UPDATE PATH ---
            logger.info(f"Found existing record (vil_id: {item_vil_id}). Updating...")
            
            # 3. Prepare the data dictionary for the update
            data_dict = self._prepare_initial_data(item=item, ingestion_time=ingestion_time)
            data_dict.pop('file_storage_path', None)

            # 4. Update the object in the database session
            db_obj = self.crud.update(db=db, db_obj=db_obj, obj_in=data_dict)
            
            # 5. Overwrite the associated JSON file with the new data
            json_content_to_save = item.model_dump(mode='json')
            async with aiofiles.open(db_obj.file_storage_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(json_content_to_save, indent=4))
            
            db.commit()
            db.refresh(db_obj)
            
            return db_obj

        except (SQLAlchemyError, IOError, Exception) as e:
            logger.error(f"Error processing update for vil_id {item.vil_id}. Rolling back transaction. Error: {e}")
            db.rollback()
            raise
