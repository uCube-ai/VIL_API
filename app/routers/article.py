import os
import logging
from typing import List, Dict, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from database.db_session import get_db
from app.services import article_service
from app.schemas import article_schema # This import now gives us access to all schemas

from app.core.config import settings


router = APIRouter()
transaction_logger = logging.getLogger("transaction_logger")


@router.post(
    "/upload",
    response_model=article_schema.UploadSuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Endpoint to upload VIL Articles",
    description="Processes each article from a JSON export, saving data and returning a simple success message for each."
)
async def upload_articles_from_export(
    payload: List[Dict[str, Any]] = Body(...),
    db: Session = Depends(get_db)
):
    # --- DYNAMIC LOG FILE SETUP (UPDATED) ---
    # Generate a high-precision timestamp including microseconds to ensure unique filenames.
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    log_filename = f"upload_{timestamp}.txt"
    log_filepath = os.path.join(settings.LOGS_DIR, log_filename)    

    file_handler = logging.FileHandler(log_filepath)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    transaction_logger.addHandler(file_handler)

    start_time = datetime.now(timezone.utc)
    
    try:
        transaction_logger.info("="*50)
        transaction_logger.info(f"STARTING NEW DATA DUMP PROCESSING")
        transaction_logger.info(f"Log file: {log_filename}")
        transaction_logger.info("="*50)

        table_info = None
        for item in payload:
            if item.get("type") == "table" and item.get("name") == "articles":
                table_info = item
                break

        if not table_info:
            transaction_logger.error("FAILURE: The JSON payload is missing the required 'articles' table data block.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The JSON payload is missing the required 'articles' table data block."
            )

        articles_to_process = table_info.get("data", [])
        if not articles_to_process:
            transaction_logger.warning("Payload processed, but no articles were found in the data array.")
            return {
                "message": "Payload processed, but no articles were found in the data array.",
                "processed_articles": []
            }

        success_messages = []
        success_count = 0
        failure_count = 0

        for index, article_dict in enumerate(articles_to_process):
            article_identifier = article_dict.get('file_path', f'unknown_article_at_index_{index}')
            
            try:
                request_timestamp = datetime.now(timezone.utc)
                validated_article_data = article_schema.ArticleCreate(**article_dict)
                new_db_article = await article_service.process_and_create_article(
                    db=db,
                    article=validated_article_data,
                    ingestion_time=request_timestamp
                )
                
                message = f"'{new_db_article.html_file_path}' has been successfully added to the LKS X VIL data dump"
                success_messages.append(message)
                
                transaction_logger.info(f"SUCCESS: Article '{article_identifier}' ingested. DB ID: {new_db_article.article_id}")
                success_count += 1

            except ValidationError as e:
                failure_count += 1
                transaction_logger.error(f"FAILURE: Article '{article_identifier}' failed validation. Reason: {e.errors()}")
                continue
            except Exception as e:
                failure_count += 1
                transaction_logger.error(f"FAILURE: Article '{article_identifier}' failed processing. Reason: {type(e).__name__} - {e}")
                continue

        if not success_messages:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Data was provided, but no articles could be successfully processed due to errors."
            )

        return {
            "message": f"Successfully processed {len(success_messages)} article(s).",
            "processed_articles": success_messages
        }

    finally:
        end_time = datetime.now(timezone.utc)
        duration = end_time - start_time
        
        transaction_logger.info("="*50)
        transaction_logger.info("PROCESSING SUMMARY")
        transaction_logger.info(f"Total articles in payload: {len(articles_to_process)}")
        transaction_logger.info(f"Successfully ingested: {success_count}")
        transaction_logger.info(f"Failed to ingest: {failure_count}")
        transaction_logger.info(f"Total processing time: {duration}")
        transaction_logger.info("END OF TRANSACTION")
        transaction_logger.info("="*50)

        transaction_logger.removeHandler(file_handler)
        file_handler.close()
