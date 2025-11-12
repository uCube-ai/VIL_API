from sqlalchemy import Column, BigInteger, DateTime, Text
from database.db_session import Base

class VAT(Base):
    """
    SQLAlchemy ORM model for the 'vat' table.
    """
    __tablename__ = "vat"

    case_id = Column(BigInteger, primary_key=True, autoincrement=True)
    vil_id = Column(BigInteger, nullable=False, unique=True)
    prod_id = Column(Text, nullable=True)
    prod_name = Column(Text, nullable=True)
    sub_prod_id = Column(Text, nullable=True)
    sub_prod_name = Column(Text, nullable=True)
    sub_subprod_id = Column(Text, nullable=True)
    state_id = Column(Text, nullable=True)
    circular_date = Column(DateTime, nullable=True, index=True)
    eq_citation = Column(Text, nullable=True)
    circular_no = Column(Text, nullable=False, index=True, unique=True)
    case_no = Column(Text, nullable=True)
    order_no = Column(Text, nullable=True)
    judge_name = Column(Text, nullable=True)
    cir_subject = Column(Text, nullable=True)
    party_name = Column(Text, nullable=True)
    html_file_path = Column(Text, nullable=False, unique=True)
    file_storage_path = Column(Text, nullable=False)
    created_dt = Column(DateTime, nullable=True)
    updated_dt = Column(DateTime, nullable=True)
    ingestion_dt = Column(DateTime, nullable=False)


    def __repr__(self):
        """
        Provides a developer-friendly representation of the object, useful for debugging.
        """
        return f"<VAT(case_id={self.case_id}, circular_no='{self.circular_no}')>"