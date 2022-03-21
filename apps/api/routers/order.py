from datetime import datetime
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
from models.customer import Customer, LoyaltyTier
from models.order import Order
from util import calculate_tier

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
            .where(Order.purchase_on > tier_start_date())
            .join(Customer.orders)
            .group_by(Customer.id)
        ).scalar()
        or 0
    )

    customer.tier = cast(Any, calculate_tier(customer_spending))
    db.add(customer)
    db.commit()

    return {}
