from database.models.budgets_union_model import BudgetsUnion
from database.crud.base import CRUDBase 


class CRUDArticle(CRUDBase[BudgetsUnion]):
    pass

budget_union = CRUDArticle(BudgetsUnion)