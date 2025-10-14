from sqlalchemy import Column, BigInteger, DateTime, Text
from database.db_session import Base

class Article(Base):
    """
    SQLAlchemy ORM model for the 'articles' table.
    """
    __tablename__ = "articles"

    article_id = Column(BigInteger, primary_key=True, autoincrement=True)
    article_date = Column(DateTime, nullable=True, index=True)
    summary = Column(Text, nullable=True)
    author = Column(Text, index=True, nullable=True)
    file_storage_path = Column(Text, nullable=False)
    html_file_path = Column(Text, nullable=False, unique=True)
    created_dt = Column(DateTime, nullable=True)
    updated_dt = Column(DateTime, nullable=True)

    def __repr__(self):
        """
        Provides a developer-friendly representation of the object, useful for debugging.
        """
        # Updated to match the class name
        return f"<Article(article_id={self.article_id}, author='{self.author}', date='{self.article_date}')>"
