# my_project/app/services/article_service.py

import os
import aiofiles
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

from app.core.config import settings
from app.schemas.article_schema import ArticleCreate
from database.crud import crud_article
from database.models.article_model import Article

async def process_and_create_article(db: Session, article: ArticleCreate) -> Article:
    """
    Handles the business logic of processing an article:
    1. Saves the 'file_data' as a .txt file.
    2. Prepares the data dictionary for the database.
    3. Calls the CRUD function to create the database record.
    """
    # --- 1. File Saving Logic ---
    
    # Sanitize the original filename from the payload
    original_filename = os.path.basename(article.file_path)
    safe_base_filename = secure_filename(original_filename)

    # Change the extension from .htm (or whatever it was) to .txt
    filename_without_ext, _ = os.path.splitext(safe_base_filename)
    new_filename = f"{filename_without_ext}.txt"
    
    # Define the target directory and ensure it exists
    # e.g., 'my_project/storage/articles'
    target_dir = os.path.join(settings.STORAGE_PATH, "articles")
    os.makedirs(target_dir, exist_ok=True)
    
    # Construct the full path for the new .txt file
    file_storage_path = os.path.join(target_dir, new_filename)

    # Asynchronously write the file content
    async with aiofiles.open(file_storage_path, 'w', encoding='utf-8') as f:
        await f.write(article.file_data)
        
    # --- 2. Data Preparation for Database ---
    
    article_data_for_db = {
        "article_date": article.article_date,
        "summary": article.summary,
        "author": article.author,
        "created_dt": article.created_dt,
        "updated_dt": article.updated_dt,
        "html_file_path": article.file_path,  # Storing the original path
        "file_storage_path": file_storage_path # Storing the new .txt path
    }

    # --- 3. Database Creation ---
    
    # Call the synchronous CRUD function to create the record
    # Note: DB operations are often run in a thread pool by FastAPI for async endpoints
    new_db_article = crud_article.create_article(db=db, article_data=article_data_for_db)
    
    return new_db_article