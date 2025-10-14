from database.models.cgst_model import CGST
from database.crud.base import CRUDBase 


class CRUDCGST(CRUDBase[CGST]):
    pass

cgst = CRUDCGST(CGST)