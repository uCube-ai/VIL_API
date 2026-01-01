from sqlalchemy import Column, BigInteger, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from database.db_session import Base

class Features(Base):
    """
    SQLAlchemy ORM model for the 'features' table.
    """
    __tablename__ = "features"

    feature_id = Column(BigInteger, primary_key=True, autoincrement=True)
    universal_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    vil_id = Column(BigInteger, nullable=False, unique=True)
    feature_date = Column(DateTime, nullable=True, index=True)
    subject = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    html_file_path = Column(Text, nullable=False, unique=True)
    created_dt = Column(DateTime, nullable=True)
    updated_dt = Column(DateTime, nullable=True)
    ingestion_dt = Column(DateTime, nullable=False)
    file_storage_path = Column(Text, nullable=False)

    def __repr__(self):
        """
        Provides a developer-friendly representation of the object, useful for debugging.
        """
        return f"<Features(feature_id={self.feature_id}, date='{self.feature_date}')>"
