from sqlalchemy.orm import Session
from database.models.article_model import Article
from app.schemas.article_schema import ArticleCreate

def create_article(db: Session, article_data: dict) -> Article:
    """
    Creates a new article record in the database.
    
    Args:
        db: The SQLAlchemy database session.
        article_data: A dictionary containing all the data for the new article.
    
    Returns:
        The newly created Article SQLAlchemy object.
    """
    # Create an instance of the Article model
    db_article = Article(**article_data)
    
    # Add the instance to the session, commit, and refresh to get the new article_id
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    return db_article