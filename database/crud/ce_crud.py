from database.models.ce_model import CE
from .base import CRUDBase 


class CRUDArticle(CRUDBase[CE]):
    pass

ce = CRUDArticle(CE)