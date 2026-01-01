from typing import Any, Dict, Generic, Type, TypeVar, Optional
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
    
    def get_by_vil_id(self, db: Session, *, vil_id: int) -> Optional[ModelType]:
        """
        Retrieves a record by its vil_id.
        """
        return db.query(self.model).filter(self.model.vil_id == vil_id).first()
    
    def get_by_universal_id(self, db: Session, universal_id: Any) -> Optional[ModelType]:
        """
        Retrieves a record by its universal_id.
        """
        return db.query(self.model).filter(self.model.universal_id == universal_id).first()

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        """
        Updates an existing model instance with data from a dictionary.
        Does NOT commit the transaction.
        """
        # Get the primary key name of the model
        pk_name = self.model.__mapper__.primary_key[0].name
        
        for field, value in obj_in.items():
            # Don't try to update the primary key
            if field != pk_name:
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        return db_obj
