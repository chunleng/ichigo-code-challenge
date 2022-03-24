from datetime import date, datetime
from typing import Any, Optional, cast

from fastapi.params import Depends
from fastapi.routing import APIRouter
from pydantic.main import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import sum
from starlette.responses import JSONResponse

from database import get_db
from models.customer import Customer
from models.order import Order
from util import calculate_tier, tier_start_date

router = APIRouter()


class CreateOrderRequest(BaseModel):
    customer_id: str
    customer_name: str
    order_id: str
    total_in_cents: int
    date: datetime


@router.post(
    "/CreateOrder",
    operation_id="CreateOrder",
    response_class=JSONResponse,
)
async def create_order(
    body: CreateOrderRequest, db: Session = cast(Session, Depends(get_db))
):
    customer: Optional[Customer] = db.query(Customer).get(body.customer_id)

    if customer is None:
        customer = Customer(id=body.customer_id)

    customer.name = cast(Any, body.customer_name)
    db.add(customer)

    try:
        db.add(
            Order(
                id=body.order_id,
                total_in_cents=body.total_in_cents,
                purchase_on=body.date,
                customer_id=body.customer_id,
            )
        )
        db.flush()
    except IntegrityError:
        return {"code": "order_duplicate"}

    customer_spending = (
        db.execute(
            select(sum(Order.total_in_cents))
            .where(Customer.id == body.customer_id)
            .where(Order.purchase_on >= tier_start_date())
            .join(Customer.orders)
            .group_by(Customer.id)
        ).scalar()
        or 0
    )

    customer.tier = cast(Any, calculate_tier(customer_spending))
    db.commit()

    return {}


class OrderResponse(BaseModel):
    id: str
    purchase_on: date
    total_in_cents: int
    customer_id: str

    class Config:
        orm_mode = True


@router.get(
    "/ListOrdersByCustomerId",
    operation_id="ListOrdersByCustomerId",
    response_class=JSONResponse,
    response_model=list[OrderResponse],
)
async def list_orders_by_customer_id(
    id: str,
    page: int = 1,
    page_size: int = 0,
    db: Session = cast(Session, Depends(get_db)),
):
    if db.query(Customer).get(id) is None:
        return JSONResponse({}, status_code=404)

    query = (
        db.query(Order)
        .where(Order.customer_id == id)
        .where(Order.purchase_on >= tier_start_date())
    )

    if page_size > 0:
        query = query.offset((page - 1) * page_size).limit(page_size)

    orders = query.all()
    return orders
