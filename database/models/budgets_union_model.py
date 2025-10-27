from sqlalchemy import Column, BigInteger, DateTime, Text
from database.db_session import Base

class BudgetsUnion(Base):
    """
    SQLAlchemy ORM model for the 'Budgets Union' table.
    """
    __tablename__ = "budgets_union"

    circular_id = Column(BigInteger, primary_key=True, autoincrement=True)
    vil_id = Column(BigInteger, nullable=True)
    circular_date = Column(DateTime, nullable=True, index=True)
    circular_no = Column(Text, nullable=True)
    cir_subject = Column(Text, nullable=True)
    file_storage_path = Column(Text, nullable=False)
    html_file_path = Column(Text, nullable=False, unique=True)
    created_dt = Column(DateTime, nullable=True)
    updated_dt = Column(DateTime, nullable=True)
    ingestion_dt = Column(DateTime, nullable=False)

    def __repr__(self):
        """
        Provides a developer-friendly representation of the object, useful for debugging.
        """
        return f"<BudgetsUnion(circular_id={self.circular_id}, circular_no='{self.circular_no}')>"
