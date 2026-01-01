from sqlalchemy import Column, BigInteger, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from database.db_session import Base

class CGST(Base):
    """
    SQLAlchemy ORM model for the 'cgst' table.
    """
    __tablename__ = "cgst"

    case_id = Column(BigInteger, primary_key=True, autoincrement=True)
    universal_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    vil_id = Column(BigInteger, nullable=False, unique=True)
    prod_id = Column(Text, nullable=True)
    prod_name = Column(Text, nullable=True)
    sub_prod_id = Column(Text, nullable=True)
    sub_prod_name = Column(Text, nullable=True)
    sub_subprod_id = Column(Text, nullable=True)
    circular_date = Column(DateTime, nullable=True, index=True)
    circular_no = Column(Text, nullable=False, index=True, unique=True)
    cir_subject = Column(Text, nullable=True)
    html_file_path = Column(Text, nullable=False, unique=True)
    created_dt = Column(DateTime, nullable=True)
    updated_dt = Column(DateTime, nullable=True)
    ingestion_dt = Column(DateTime, nullable=False)
    file_storage_path = Column(Text, nullable=False)


    def __repr__(self):
        """
        Provides a developer-friendly representation of the object, useful for debugging.
        """
        return f"<CGST(case_id={self.case_id}, circular_no='{self.circular_no}')>"