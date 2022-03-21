from typing import cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from pydantic.main import BaseModel
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse

import models.order  # type: ignore
from database import Base, engine, get_db
from dbseed import seed
from models.customer import Customer

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Auto create table and seed the table
# To save development time and project complexity, tables and test values are automatically created on load, the
# following could be done if we are doing deployment
# - Table creation -> alembic (Python version of rails' db:migrate)
# - DB seed, created as seperate script
Base.metadata.create_all(bind=engine)
seed()


class Foo(BaseModel):
    class Order(BaseModel):
        total_in_cents: int

        class Config:
            orm_mode = True

    name: str
    orders: list[Order]

    class Config:
        orm_mode = True


@app.get(
    "/GetFoo",
    operation_id="GetFoo",
    response_class=JSONResponse,
    response_model=Foo,
    tags=[""],
)
async def get_foo(db: Session = cast(Session, Depends(get_db))):
    return db.query(Customer).options(joinedload(Customer.orders)).first()
