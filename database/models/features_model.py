from sqlalchemy import Column, BigInteger, DateTime, Text
from database.db_session import Base

class Features(Base):
    """
    SQLAlchemy ORM model for the 'features' table.
    """
    __tablename__ = "features"

    feature_id = Column(BigInteger, primary_key=True, autoincrement=True)
    vil_id = Column(BigInteger, nullable=True)
    feature_date = Column(DateTime, nullable=True, index=True)
    subject = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    file_storage_path = Column(Text, nullable=False)
    html_file_path = Column(Text, nullable=False, unique=True)
    created_dt = Column(DateTime, nullable=True)
    updated_dt = Column(DateTime, nullable=True)
    ingestion_dt = Column(DateTime, nullable=False)

    def __repr__(self):
        """
        Provides a developer-friendly representation of the object, useful for debugging.
        """
        return f"<Features(feature_id={self.feature_id}, date='{self.feature_date}')>"
