from database.models.dgft_model import DGFT
from database.crud.base import CRUDBase 


class CRUDDGFT(CRUDBase[DGFT]):
    pass

dgft = CRUDDGFT(DGFT)