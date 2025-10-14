from sqlalchemy import Column, BigInteger, DateTime, Text
from database.db_session import Base

class DGFT(Base):
    """
    SQLAlchemy ORM model for the 'dgft' table.
    """
    __tablename__ = "dgft"

    case_id = Column(BigInteger, primary_key=True, autoincrement=True)
    prod_id = Column(Text, nullable=True)
    prod_name = Column(Text, nullable=True)
    sub_prod_id = Column(Text, nullable=True)
    sub_prod_name = Column(Text, nullable=True)
    sub_subprod_id = Column(Text, nullable=True)
    state_id = Column(Text, nullable=True) 
    circular_date = Column(DateTime, nullable=True, index=True)
    circular_no = Column(Text, nullable=False, index=True, unique=True)
    cir_subject = Column(Text, nullable=True)
    html_file_path = Column(Text, nullable=False, unique=True)
    file_storage_path = Column(Text, nullable=False)
    created_dt = Column(DateTime, nullable=True)
    updated_dt = Column(DateTime, nullable=True)
    ingestion_dt = Column(DateTime, nullable=False)


    def __repr__(self):
        """
        Provides a developer-friendly representation of the object, useful for debugging.
        """
        # CORRECTED: Uses fields that exist in this model.
        return f"<DGFT(case_id={self.case_id}, circular_no='{self.circular_no}')>"