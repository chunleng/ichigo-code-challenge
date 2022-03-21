from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from dbseed import seed
from routers import order

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Auto create table and seed the table
# To save development time and project complexity, tables and test values are automatically created on load, the
# following could be done if we are doing deployment
# - Table creation -> alembic (Python version of rails' db:migrate)
# - DB seed, created as seperate script
Base.metadata.create_all(bind=engine)
seed()

app.include_router(order.router)
