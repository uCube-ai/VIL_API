import os
import logging
from typing import Dict, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from database.db_session import get_db
from app.schemas.common import UploadSuccessResponse
from app.core.logging_config import transaction_logging
from app.routers.router_config import RouterConfig

transaction_logger = logging.getLogger("transaction_logger")

def create_router(config: RouterConfig) -> APIRouter:
    """
    A factory function that creates and configures an APIRouter for a specific data type.
    It now creates TWO endpoints: /upload (Upsert) and /update (Update-Only).
    """
    router = APIRouter()

    @router.post(
        "/upload",
        response_model=UploadSuccessResponse,
        status_code=status.HTTP_201_CREATED,
        summary=f"Endpoint to upload and upsert {config.entity_name_plural.title()}",
        description=f"Processes each {config.entity_name_singular} from a JSON export, saving data and returning a simple success message for each."
    )
    async def upload_from_export(
        payload: Dict[str, Any] = Body(...),
        db: Session = Depends(get_db)
    ):
        
        with transaction_logging(table_name=config.table_name, operation="upload") as log_file:
            start_time = datetime.now(timezone.utc)

            # 1. Validation Logic
            payload_table_name = payload.get("name")
            if payload_table_name != config.vil_table_name:
                detail = (f"Table mismatch. Endpoint expects '{config.vil_table_name}', "
                        f"but payload contains data for '{payload_table_name}'.")
                transaction_logger.error(f"FAILURE: {detail}")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

            items_to_process = payload.get("data", [])

            if not items_to_process:
                message = f"Payload received, but 'data' array is empty for {config.entity_name_plural}."
                transaction_logger.warning(message)
                return {"message": message, "processed_items": []}

            # 2. Processing Logic
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
            
            # 3. Log Summary
            end_time = datetime.now(timezone.utc)
            duration = end_time - start_time
            
            transaction_logger.info("PROCESSING SUMMARY")
            transaction_logger.info(f"Total items: {len(items_to_process)}")
            transaction_logger.info(f"Success: {success_count}")
            transaction_logger.info(f"Failed: {failure_count}")
            transaction_logger.info(f"Duration: {duration}")

            if not success_messages:
                detail = f"Data was provided, but no {config.entity_name_plural} could be successfully processed due to errors."
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

            return {
                "message": f"Successfully processed {len(success_messages)} {config.entity_name_singular}(s).",
                "processed_items": success_messages
            }

    @router.post(
        "/update",
        response_model=UploadSuccessResponse,
        status_code=status.HTTP_200_OK,
        summary=f"Endpoint to update existing {config.entity_name_plural.title()}",
        description=f"Processes each {config.entity_name_singular} from a JSON export. ONLY updates items found via vil_id. Skips unknown items."
    )
    async def update_from_export(
        payload: Dict[str, Any] = Body(...),
        db: Session = Depends(get_db)
    ):

        with transaction_logging(table_name=config.table_name, operation="update") as log_file:
            start_time = datetime.now(timezone.utc)

            # 1. Validation
            payload_table_name = payload.get("name")
            if payload_table_name != config.vil_table_name:
                 detail = f"Table mismatch: Expected '{config.vil_table_name}', got '{payload_table_name}'"
                 transaction_logger.error(detail)
                 raise HTTPException(status_code=400, detail=detail)
            
            items_to_process = payload.get("data", [])

            if not items_to_process:
                message = f"Payload received, but 'data' array is empty for {config.entity_name_plural}."
                transaction_logger.warning(message)
                return {"message": message, "processed_items": []}

            # 2. Processing
            success_messages = []
            success_count = 0
            failure_count = 0
            created_count = 0
            updated_count = 0

            for index, item_dict in enumerate(items_to_process):
                item_identifier = item_dict.get('vil_id', f'unknown_{config.entity_name_singular}_at_index_{index}')
                
                try:
                    request_timestamp = datetime.now(timezone.utc)
                    validated_data = config.pydantic_schema(**item_dict)

                    # A. TRY UPDATE FIRST
                    db_item = await config.service.process_update_item(
                        db=db,
                        item=validated_data,
                        ingestion_time=request_timestamp)
                    
                    if db_item:
                        action_type = "UPDATED"
                        updated_count += 1
                    else:
                        # --- CREATE PATH (Fallback if not found) ---
                        transaction_logger.info(f"Item '{item_identifier}' not found. Switching to CREATE.")
                        
                        db_item = await config.service.process_and_create_item(
                            db=db,
                            item=validated_data,
                            ingestion_time=request_timestamp)
                        action_type = "CREATED"
                        created_count += 1
                    
                    # --- SUCCESS HANDLING (Common for both) ---
                    message = f"{action_type}: vil_id {db_item.vil_id}"
                    success_messages.append(message)
                    
                    pk_value = getattr(db_item, config.pk_field_name, "N/A")
                    transaction_logger.info(f"SUCCESS ({action_type}): {config.entity_name_singular} '{item_identifier}'. DB ID: {pk_value}")
                    success_count += 1
                        
                except (ValidationError, Exception) as e:
                    failure_count += 1
                    transaction_logger.error(f"FAILURE (Update): Item '{item_identifier}'. Reason: {e}")
                    continue

            # 3. Log Summary
            end_time = datetime.now(timezone.utc)
            duration = end_time - start_time
            
            transaction_logger.info("PROCESSING SUMMARY")
            transaction_logger.info(f"Total items: {len(items_to_process)}")
            transaction_logger.info(f"Success: {success_count}")
            transaction_logger.info(f"Skipped/Failed: {failure_count}")
            transaction_logger.info(f"Duration: {duration}")

            return {
                "message": f"Successfully updated {success_count} item(s). {failure_count} failed or were skipped.",
                "processed_items": success_messages
            }

    return router
