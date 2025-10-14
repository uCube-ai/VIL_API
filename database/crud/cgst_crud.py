from database.models.cgst_model import CGST
from .base import CRUDBase 


class CRUDCGST(CRUDBase[CGST]):
    pass

cgst = CRUDCGST(CGST)