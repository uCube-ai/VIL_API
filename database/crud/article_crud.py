from database.models.article_model import Article
from .base import CRUDBase 


class CRUDArticle(CRUDBase[Article]):
    pass

article = CRUDArticle(Article)