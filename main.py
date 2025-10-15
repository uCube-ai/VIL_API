from fastapi import FastAPI
from app.routers import article, budgets_union, ce, cgst, cu, dgft, sgst, st
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
app.include_router(ce.router, prefix="/ce", tags=["Central Excise"])
app.include_router(cgst.router, prefix="/cgst", tags=["Central Goods and Services Tax"])
app.include_router(cu.router, prefix="/cu", tags=["Customs"])
app.include_router(dgft.router, prefix="/dgft", tags=["Directorate General of Foreign Trade"])
app.include_router(sgst.router, prefix="/sgst", tags=["State Goods and Services Tax"])
app.include_router(st.router, prefix="/st", tags=["Service Tax"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the LKS X VIL Data Ingestion API"}