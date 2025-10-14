from sqlalchemy.orm import Session
from database.models.article_model import Article

def create_article_record(db: Session, article_data: dict) -> Article:
    """
    Creates an Article object in the session and flushes to get the ID.
    Does NOT commit the transaction.

    Args:
        db: The SQLAlchemy database session.
        article_data: A dictionary with the initial data for the new article.

    Returns:
        The newly created Article SQLAlchemy object, now populated with an ID.
    """
    # Create an instance of the Article model with a placeholder for the path
    db_article = Article(**article_data)
    
    # Add the object to the session
    db.add(db_article)
    
    # Flush the session. This sends the SQL to the DB and populates the article_id, but the transaction is still open.
    db.flush()
    
    return db_article

def update_article_storage_path(db: Session, db_article: Article, path: str) -> Article:
    """
    Updates the file_storage_path for a given Article object within the session.
    Does NOT commit the transaction.

    Args:
        db: The SQLAlchemy database session.
        db_article: The Article object to update.
        path: The new file storage path.

    Returns:
        The updated Article object.
    """
    db_article.file_storage_path = path
    db.add(db_article)   
    return db_article