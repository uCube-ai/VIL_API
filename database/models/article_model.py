from sqlalchemy import Column, BigInteger, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from database.db_session import Base

class Article(Base):
    """
    SQLAlchemy ORM model for the 'articles' table.
    """
    __tablename__ = "articles"

    article_id = Column(BigInteger, primary_key=True, autoincrement=True)
    universal_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    vil_id = Column(BigInteger, nullable=False, unique=True)
    article_date = Column(DateTime, nullable=True, index=True)
    summary = Column(Text, nullable=True)
    author = Column(Text, nullable=True)
    html_file_path = Column(Text, nullable=False, unique=True)
    created_dt = Column(DateTime, nullable=True)
    updated_dt = Column(DateTime, nullable=True)
    ingestion_dt = Column(DateTime, nullable=False)
    file_storage_path = Column(Text, nullable=False)


    def __repr__(self):
        """
        Provides a developer-friendly representation of the object, useful for debugging.
        """
        return f"<Article(article_id={self.article_id}, author='{self.author}', date='{self.article_date}')>"
