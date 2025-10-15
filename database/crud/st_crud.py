from database.models.st_model import ST
from database.crud.base import CRUDBase 


class CRUDST(CRUDBase[ST]):
    pass

st = CRUDST(ST)