# my_project/main.py
from fastapi import FastAPI
from app.routers import article, cases
from database import db_session

# This would create the database tables if they don't exist
# It's often better to manage this with a migration tool like Alembic
# For now, we can call it here for simplicity.
# db_session.Base.metadata.create_all(bind=db_session.engine)

app = FastAPI(
    title="LKS X VIL Data Ingestion API",
    description="API for processing articles and cases from JSON exports."
)

# Include the routers from the 'app/routers' directory
app.include_router(article.router, prefix="/articles", tags=["Articles"])
# app.include_router(cases.router, prefix="/cases", tags=["Cases"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the LKS X VIL Data Ingestion API"}