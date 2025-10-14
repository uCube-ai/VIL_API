from database.models.ce_model import CE
from database.crud.base import CRUDBase 


class CRUDCE(CRUDBase[CE]):
    pass

ce = CRUDCE(CE)