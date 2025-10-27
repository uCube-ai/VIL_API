import os
import logging
from typing import List, Dict, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from database.db_session import get_db
from app.schemas.common import UploadSuccessResponse
from app.core.config import settings
from app.routers.router_config import RouterConfig

transaction_logger = logging.getLogger("transaction_logger")

def create_upload_router(config: RouterConfig) -> APIRouter:
    """
    A factory function that creates and configures an APIRouter for a specific data type.
    """
    router = APIRouter()

    @router.post(
        "/upload",
        response_model=UploadSuccessResponse,
        status_code=status.HTTP_201_CREATED,
        summary=f"Endpoint to upload VIL {config.entity_name_plural.title()}",
        description=f"Processes each {config.entity_name_singular} from a JSON export, saving data and returning a simple success message for each."
    )
    async def upload_from_export(
        payload: List[Dict[str, Any]] = Body(...),
        db: Session = Depends(get_db)
    ):
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        log_filename = f"upload_{config.table_name}_{timestamp}.txt"
        log_filepath = os.path.join(settings.LOGS_DIR, log_filename)

        file_handler = logging.FileHandler(log_filepath)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        transaction_logger.addHandler(file_handler)

        start_time = datetime.now(timezone.utc)
        
        try:
            transaction_logger.info("=" * 50)
            transaction_logger.info(f"STARTING NEW '{config.table_name}' DATA DUMP PROCESSING")
            transaction_logger.info(f"Log file: {log_filename}")
            transaction_logger.info("=" * 50)

            table_info = None
            for item in payload:
                if item.get("type") == "table" and item.get("name") == config.vil_table_name:
                    table_info = item
                    break

            if not table_info:
                detail = f"The JSON payload is missing the required '{config.table_name}' table data block."
                transaction_logger.error(f"FAILURE: {detail}")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

            items_to_process = table_info.get("data", [])
            if not items_to_process:
                message = f"Payload processed, but no {config.entity_name_plural} were found in the data array."
                transaction_logger.warning(message)
                return {"message": message, "processed_items": []}

            success_messages = []
            success_count = 0
            failure_count = 0

            for index, item_dict in enumerate(items_to_process):
                item_identifier = item_dict.get('vil_id', f'unknown_{config.entity_name_singular}_at_index_{index}')
                
                try:
                    request_timestamp = datetime.now(timezone.utc)
                    validated_data = config.pydantic_schema(**item_dict)
                    new_db_item = await config.service.process_and_create_item(
                        db=db,
                        item=validated_data,
                        ingestion_time=request_timestamp
                    )
                    
                    message = f"File with vil_id: {new_db_item.vil_id} has been successfully added to the LKS X VIL data dump"
                    success_messages.append(message)
                    
                    pk_value = getattr(new_db_item, config.pk_field_name, "N/A")
                    transaction_logger.info(f"SUCCESS: {config.entity_name_singular.title()} with vil_id:'{item_identifier}' ingested. DB ID: {pk_value}")
                    success_count += 1

                except ValidationError as e:
                    failure_count += 1
                    transaction_logger.error(f"FAILURE: {config.entity_name_singular.title()} with vil_id:'{item_identifier}' failed validation. Reason: {e.errors()}")
                    continue
                except Exception as e:
                    failure_count += 1
                    transaction_logger.error(f"FAILURE: {config.entity_name_singular.title()} with vil_id:'{item_identifier}' failed processing. Reason: {type(e).__name__} - {e}")
                    continue

            if not success_messages:
                detail = f"Data was provided, but no {config.entity_name_plural} could be successfully processed due to errors."
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

            return {
                "message": f"Successfully processed {len(success_messages)} {config.entity_name_singular}(s).",
                "processed_items": success_messages
            }

        finally:
            end_time = datetime.now(timezone.utc)
            duration = end_time - start_time
            
            transaction_logger.info("=" * 50)
            transaction_logger.info("PROCESSING SUMMARY")
            transaction_logger.info(f"Total {config.entity_name_plural} in payload: {len(items_to_process)}")
            transaction_logger.info(f"Successfully ingested: {success_count}")
            transaction_logger.info(f"Failed to ingest: {failure_count}")
            transaction_logger.info(f"Total processing time: {duration}")
            transaction_logger.info("END OF TRANSACTION")
            transaction_logger.info("=" * 50)

            transaction_logger.removeHandler(file_handler)
            file_handler.close()

    return router