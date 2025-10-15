from database.models.vat_model import VAT
from database.crud.base import CRUDBase 


class CRUDVAT(CRUDBase[VAT]):
    pass

vat = CRUDVAT(VAT)
