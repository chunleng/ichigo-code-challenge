from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, port
from dbseed import seed
from routers import loyalty, order

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Auto create table
# To save development time and project complexity, tables and test values are automatically created on load, alembic
# could be used if we are doing actual deployment to production (alembic is Python equivalent of rails' db:migrate)
Base.metadata.create_all(bind=engine)

# For easy setup, the dbseed is auto-applied
# This will not be necessary in test and production environments
if port != "25432":
    seed()

app.include_router(order.router)
app.include_router(loyalty.router)
