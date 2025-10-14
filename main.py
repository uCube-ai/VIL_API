from fastapi import FastAPI
from app.routers import article, budgets_union
from app.core import logging_config

logging_config.setup_transaction_logger()

# This would create the database tables if they don't exist
# It's often better to manage this with a migration tool like Alembic
# For now, we can call it here for simplicity.
# db_session.Base.metadata.create_all(bind=db_session.engine)

app = FastAPI(
    title="LKS X VIL Data Ingestion API",
    description="API for processing VIL data dump."
)

app.include_router(article.router, prefix="/articles", tags=["Articles"])
app.include_router(budgets_union.router, prefix="/budgets_union", tags=["Budgets Union"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the LKS X VIL Data Ingestion API"}