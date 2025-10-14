from database.models.budgets_union_model import BudgetsUnion
from database.crud.base import CRUDBase 


class CRUDBudgetsUnion(CRUDBase[BudgetsUnion]):
    pass

budget_union = CRUDBudgetsUnion(BudgetsUnion)