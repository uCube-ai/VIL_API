
from database.models.sgst_model import SGST
from database.crud.base import CRUDBase 


class CRUDSGST(CRUDBase[SGST]):
    pass

sgst = CRUDSGST(SGST)