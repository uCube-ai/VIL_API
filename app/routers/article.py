import logging
from typing import List, Dict, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from database.db_session import get_db
from app.services import article_service
from app.schemas import article_schema # This import now gives us access to all schemas


router = APIRouter()
logger = logging.getLogger(__name__)


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
    table_info = None
    for item in payload:
        if item.get("type") == "table" and item.get("name") == "articles":
            table_info = item
            break

    if not table_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The JSON payload is missing the required 'articles' table data block."
        )

    articles_to_process = table_info.get("data", [])
    if not articles_to_process:
        logger.info("Received a valid payload, but there were no articles to process.")
        return {
            "message": "Payload processed, but no articles were found in the data array.",
            "processed_articles": []
        }

    success_messages = []
    
    for index, article_dict in enumerate(articles_to_process):
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

        except ValidationError as e:
            logger.warning(f"Skipping article at index {index} due to validation error: {e.errors()}")
            continue
        except Exception as e:
            logger.error(f"Failed to process article at index {index}. Error: {e}")
            continue

    if not success_messages:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Data was provided, but no articles could be successfully processed due to errors."
        )

    logger.info(f"Successfully processed and created {len(success_messages)} articles.")
    
    return {
        "message": f"Successfully processed {len(success_messages)} article(s).",
        "processed_articles": success_messages
    }
