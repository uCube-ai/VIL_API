from database.models.article_model import Article
from database.crud.base import CRUDBase 


class CRUDArticle(CRUDBase[Article]):
    pass

article = CRUDArticle(Article)