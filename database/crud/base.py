from typing import Any, Dict, Generic, Type, TypeVar
from sqlalchemy.orm import Session
from database.db_session import Base

# Define custom types for SQLAlchemy model and Pydantic schema
ModelType = TypeVar("ModelType", bound=Base)

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        Generic CRUD base class with default methods for Create, Read, Update, Delete.

        * `model`: A SQLAlchemy model class
        """
        self.model = model

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        """
        Creates a new record in the database and flushes to get the ID.
        Does NOT commit the transaction.

        Args:
            db: The SQLAlchemy database session.
            obj_in: A dictionary with the data for the new record.

        Returns:
            The newly created SQLAlchemy model object, populated with an ID.
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        
        # Flush the session. This sends the SQL to the DB and populates the primary key,
        # but the transaction is still open.
        db.flush()
        
        return db_obj

    def update_path(self, db: Session, *, db_obj: ModelType, path: str) -> ModelType:
        """
        Generic function to update the file_storage_path for a given object.
        Does NOT commit the transaction.
        """
        db_obj.file_storage_path = path
        db.add(db_obj) 
        return db_obj
