import os
import json
import aiofiles
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.schemas.article_schema import ArticleCreate
from database.crud import article_crud
from database.models.article_model import Article

logger = logging.getLogger(__name__)

async def process_and_create_article(db: Session, article: ArticleCreate, ingestion_time: datetime) -> Article:
    """
    Handles the business logic of processing an article:
    1. Calls the CRUD layer to create a record and get an ID.
    2. Uses the new ID to create and save a JSON file.
    3. Calls the CRUD layer to update the record with the file path.
    4. Commits the transaction or rolls back on failure.
    """
    try:
        # --- 1. Initial Database Record Creation ---
        initial_data = {
            "article_date": article.article_date,
            "summary": article.summary,
            "author": article.author,
            "created_dt": article.created_dt,
            "updated_dt": article.updated_dt,
            "html_file_path": article.file_path,
            "file_storage_path": "",  # Placeholder
            "ingestion_dt": ingestion_time
        }
        # Call the CRUD function to create the record in the session and get the ID
        db_article = article_crud.create_article_record(db=db, article_data=initial_data)

        # --- 2. File Saving Logic ---
        if not db_article.article_id:
            raise Exception("Failed to retrieve article_id after flushing the session.")
        
        new_filename = f"{db_article.article_id}_article.json"
        target_dir = os.path.join(settings.STORAGE_PATH, "articles")
        os.makedirs(target_dir, exist_ok=True)
        file_storage_path = os.path.join(target_dir, new_filename)

        # Asynchronously write the JSON file
        json_content_to_save = article.model_dump(mode='json')
        async with aiofiles.open(file_storage_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(json_content_to_save, indent=4))

        # --- 3. Update Database Record with File Path ---
        article_crud.update_article_storage_path(
            db=db, db_article=db_article, path=file_storage_path
        )

        # --- 4. Finalize Transaction ---
        # If all steps above were successful, commit all changes to the database.
        db.commit()
        
        # Refresh the instance to get the final state from the committed transaction.
        db.refresh(db_article)
        
        return db_article

    except (SQLAlchemyError, IOError, Exception) as e:
        # If any part of the process fails (DB or file I/O), roll back everything.
        logger.error(f"Error processing article. Rolling back transaction. Error: {e}")
        db.rollback()
        # Re-raise the exception so the router can handle it and return an error response.
        raise