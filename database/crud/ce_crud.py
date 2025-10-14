from database.models.ce_model import CE
from .base import CRUDBase 


class CRUDCE(CRUDBase[CE]):
    pass

ce = CRUDCE(CE)