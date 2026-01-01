import logging
from typing import Dict, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
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
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "message": message, 
                        "processed_items": [], 
                        "failed_items": []})

            # 2. Processing Logic
            success_messages = []
            failed_items_list = []
            success_count = 0
            failure_count = 0

            for index, item_dict in enumerate(items_to_process):
                item_identifier = item_dict.get('universal_id', f'index_{index}')
                
                try:
                    request_timestamp = datetime.now(timezone.utc)
                    
                    # A. Validation
                    validated_data = config.pydantic_schema(**item_dict)
                    
                    # B. Creation (Insert + File Write)
                    new_db_item = await config.service.process_and_create_item(
                        db=db,
                        item=validated_data,
                        ingestion_time=request_timestamp
                    )
                    
                    # C. Success Handling
                    message = f"CREATED: universal_id={new_db_item.universal_id}"
                    success_messages.append(message)
                    
                    pk_value = getattr(new_db_item, config.pk_field_name, "N/A")
                    transaction_logger.info(f"SUCCESS: {config.entity_name_singular} '{item_identifier}' ingested. DB ID: {pk_value}")
                    success_count += 1

                except ValidationError as e:
                    error_msgs = [f"Field '{err['loc'][-1]}': {err['msg']}" for err in e.errors()]
                    clean_msg = f"Schema Validation Error: {'; '.join(error_msgs)}"
                    
                    failure_count += 1
                    transaction_logger.error(f"Item {item_identifier}: {clean_msg}")
                    failed_items_list.append({"universal_id": str(item_identifier), "reason": clean_msg})

                except IntegrityError as e:
                    clean_msg = "Duplicate Error: This record already exists (universal_id or unique constraint violation)."
                    
                    failure_count += 1
                    transaction_logger.error(f"Item {item_identifier}: {clean_msg}")
                    failed_items_list.append({"universal_id": str(item_identifier), "reason": clean_msg})

                except (IOError, OSError) as e:
                    clean_msg = f"File System Error: Unable to write JSON file. {e.strerror}"
                    
                    failure_count += 1
                    transaction_logger.critical(f"Item {item_identifier}: {clean_msg}")
                    failed_items_list.append({"universal_id": str(item_identifier), "reason": clean_msg})

                except SQLAlchemyError as e:
                    clean_msg = f"Database Error: {str(e.__cause__) or str(e)}"
                    
                    failure_count += 1
                    transaction_logger.error(f"Item {item_identifier}: {clean_msg}")
                    failed_items_list.append({"universal_id": str(item_identifier), "reason": clean_msg})

                except Exception as e:
                    clean_msg = f"Unexpected Server Error: {str(e)}"
                    
                    failure_count += 1
                    transaction_logger.error(f"Item {item_identifier}: {clean_msg}")
                    failed_items_list.append({"universal_id": str(item_identifier), "reason": clean_msg})

            # 3. Log Summary
            end_time = datetime.now(timezone.utc)
            duration = end_time - start_time
            
            transaction_logger.info("PROCESSING SUMMARY")
            transaction_logger.info(f"Total items: {len(items_to_process)}")
            transaction_logger.info(f"Success: {success_count}")
            transaction_logger.info(f"Failed: {failure_count}")
            transaction_logger.info(f"Duration: {duration}")

            response_payload = {
                "message": f"Upload processed. Success: {success_count}, Failed: {failure_count}",
                "processed_items": success_messages,
                "failed_items": failed_items_list
            }

            content = jsonable_encoder(response_payload)

            if success_count > 0 and failure_count == 0:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
            
            elif success_count > 0 and failure_count > 0:
                return JSONResponse(status_code=status.HTTP_207_MULTI_STATUS, content=content)
            
            else:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)


    @router.post(
        "/update",
        response_model=UploadSuccessResponse,
        summary=f"Endpoint to update existing {config.entity_name_plural.title()}",
        description=f"Processes each {config.entity_name_singular} from a JSON export. ONLY updates items found via vil_id or universal_id. Skips unknown items."
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
                detail = (f"Table Mismatch: Endpoint expects data for '{config.vil_table_name}', "
                           f"but received payload for '{payload_table_name}'.")
                transaction_logger.error(detail)
                raise HTTPException(status_code=400, detail=detail)
            
            items_to_process = payload.get("data", [])

            if not items_to_process:
                message = f"Payload received, but 'data' array is empty for {config.entity_name_plural}."
                transaction_logger.warning(message)
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "message": message, 
                        "processed_items": [], 
                        "failed_items": []})

            # 2. Processing
            success_messages = []
            failed_items_list = []
            success_count = 0
            failure_count = 0

            for index, item_dict in enumerate(items_to_process):
                item_identifier = item_dict.get('universal_id', f'unknown_{config.entity_name_singular}_at_index_{index}')
                
                try:
                    request_timestamp = datetime.now(timezone.utc)
                    validated_data = config.pydantic_schema(**item_dict)

                    db_item = await config.service.process_update_item(db=db, 
                                                                       item=validated_data, 
                                                                       ingestion_time=request_timestamp) 
                    action_type = "UPDATED"
                    if not db_item:
                         db_item = await config.service.process_and_create_item(db=db, 
                                                                                item=validated_data, 
                                                                                ingestion_time=request_timestamp)
                         action_type = "CREATED"
                    
                    # --- SUCCESS HANDLING (Common for both) ---
                    success_messages.append(f"{action_type}: universal_id={db_item.universal_id}")
                    success_count += 1
                        
                except ValidationError as e:
                    error_msgs = [f"Field '{err['loc'][-1]}': {err['msg']}" for err in e.errors()]
                    clean_msg = f"Schema Validation Error: {'; '.join(error_msgs)}"
                    
                    failure_count += 1
                    transaction_logger.error(f"Item {item_identifier}: {clean_msg}")
                    failed_items_list.append({"universal_id": str(item_identifier), "reason": clean_msg})

                except IntegrityError as e:
                    clean_msg = "Database Constraint Error: This record likely already exists or violates a unique constraint."
                    
                    failure_count += 1
                    transaction_logger.error(f"Item {item_identifier}: {clean_msg}")
                    failed_items_list.append({"universal_id": str(item_identifier), "reason": clean_msg})

                except (IOError, OSError) as e:
                    clean_msg = f"File System Error: Unable to write JSON file to storage. {e.strerror}"
                    
                    failure_count += 1
                    transaction_logger.critical(f"Item {item_identifier}: {clean_msg}")
                    failed_items_list.append({"universal_id": str(item_identifier), "reason": clean_msg})

                except SQLAlchemyError as e:
                    clean_msg = f"Database Error: {str(e.__cause__) or str(e)}"
                    
                    failure_count += 1
                    transaction_logger.error(f"Item {item_identifier}: {clean_msg}")
                    failed_items_list.append({"universal_id": str(item_identifier), "reason": clean_msg})

                except Exception as e:
                    clean_msg = f"Unexpected Server Error: {str(e)}"
                    
                    failure_count += 1
                    transaction_logger.error(f"Item {item_identifier}: {clean_msg}")
                    failed_items_list.append({"universal_id": str(item_identifier), "reason": clean_msg})

            # 3. Log Summary
            end_time = datetime.now(timezone.utc)
            duration = end_time - start_time
            transaction_logger.info(f"Summary - Success: {success_count}, Failed: {failure_count}, Time: {duration}")

            response_payload = {
                "message": f"Upsert processed. Success: {success_count}, Failed: {failure_count}",
                "processed_items": success_messages,
                "failed_items": failed_items_list 
            }

            content = jsonable_encoder(response_payload)

            if success_count > 0 and failure_count == 0:
                return JSONResponse(status_code=status.HTTP_200_OK, content=content)
            
            elif success_count > 0 and failure_count > 0:
                return JSONResponse(status_code=status.HTTP_207_MULTI_STATUS, content=content)
            
            else:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)


    @router.post(
        "/delete",
        response_model=UploadSuccessResponse,
        summary=f"Endpoint to delete {config.entity_name_plural.title()}",
        description="Deletes records based on a list of universal_ids. Does NOT remove files from storage."
    )
    async def delete_items(
        payload: Dict[str, Any] = Body(...),
        db: Session = Depends(get_db)
    ):
        with transaction_logging(table_name=config.table_name, operation="delete") as log_file:
            start_time = datetime.now(timezone.utc)

            # 1. Validation
            payload_table_name = payload.get("name")
            if payload_table_name != config.vil_table_name:
                detail = (f"Table Mismatch: Endpoint expects '{config.vil_table_name}', "
                          f"but received '{payload_table_name}'.")
                transaction_logger.error(detail)
                raise HTTPException(status_code=400, detail=detail)

            ids_to_delete = payload.get("universal_id", [])

            if not ids_to_delete:
                message = "Payload received, but 'universal_id' list is empty."
                transaction_logger.warning(message)
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "message": message, 
                        "processed_items": [], 
                        "failed_items": []})
            
            # 2. Processing
            success_messages = []
            failed_items_list = []
            success_count = 0
            failure_count = 0

            for uid in ids_to_delete:
                try:
                    deleted_item = await config.service.process_delete_item(db=db, universal_id=uid)
                    
                    if deleted_item:
                        success_count += 1
                        msg = f"DELETED: {uid}"
                        success_messages.append(msg)
                        transaction_logger.info(f"SUCCESS: {msg}")
                    else:
                        failure_count += 1
                        clean_msg = "Record not found in database."
                        transaction_logger.warning(f"SKIPPED: {uid} - {clean_msg}")
                        failed_items_list.append({"universal_id": str(uid), "reason": clean_msg})

                except Exception as e:
                    failure_count += 1
                    clean_msg = f"Database/Server Error: {str(e)}"
                    transaction_logger.error(f"FAILURE: {uid} - {clean_msg}")
                    failed_items_list.append({"universal_id": str(uid), "reason": clean_msg})

            # 3. Log Summary & Response
            end_time = datetime.now(timezone.utc)
            duration = end_time - start_time
            
            transaction_logger.info("PROCESSING SUMMARY")
            transaction_logger.info(f"Total requested: {len(ids_to_delete)}")
            transaction_logger.info(f"Deleted: {success_count}")
            transaction_logger.info(f"Failed/Skipped: {failure_count}")
            transaction_logger.info(f"Duration: {duration}")

            response_payload = {
                "message": f"Delete processed. Success: {success_count}, Failed: {failure_count}",
                "processed_items": success_messages,
                "failed_items": failed_items_list
            }
            
            content = jsonable_encoder(response_payload)

            if success_count > 0 and failure_count == 0:
                return JSONResponse(status_code=status.HTTP_200_OK, content=content)
            
            elif success_count > 0 and failure_count > 0:
                return JSONResponse(status_code=status.HTTP_207_MULTI_STATUS, content=content)

            else:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)

    return router
