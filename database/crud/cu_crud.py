from database.models.cu_model import CU
from database.crud.base import CRUDBase


class CRUDCU(CRUDBase[CU]):
    pass

cu = CRUDCU(CU)