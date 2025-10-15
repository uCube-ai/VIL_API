from database.models.features_model import Features
from database.crud.base import CRUDBase 


class CRUDFeatures(CRUDBase[Features]):
    pass

features = CRUDFeatures(Features)