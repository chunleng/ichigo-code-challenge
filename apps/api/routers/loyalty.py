from datetime import date
from typing import Optional, cast

from fastapi.params import Depends
from fastapi.routing import APIRouter
from pydantic.main import BaseModel
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import sum
from starlette.responses import JSONResponse

from database import get_db
from models.customer import Customer, LoyaltyTier
from models.order import Order
from util import (calculate_tier, next_tier, tier_end_date, tier_minimum,
                  tier_start_date)

router = APIRouter()


class CustomerLoyaltyInformation(BaseModel):
    purchase_amount_in_cents: int
    purchase_amount_to_next_tier_in_cents: int
    purchase_amount_period_from: date
    current_tier: LoyaltyTier
    downgrade_tier: Optional[LoyaltyTier]
    downgrade_on: date
    purchase_amount_to_maintain_tier_in_cents: int


@router.get(
    "/GetLoyaltyInformationByCustomer",
    operation_id="GetLoyaltyInformationByCustomer",
    response_class=JSONResponse,
    response_model=CustomerLoyaltyInformation,
)
async def get_loyalty_information_by_customer(
    id: str, db: Session = cast(Session, Depends(get_db))
):
    customer = cast(Customer, db.query(Customer).get(id))

    if customer is None:
        return JSONResponse({}, 404)

    start_date = tier_start_date()
    customer_spending = (
        db.execute(
            select(sum(Order.total_in_cents))
            .where(Customer.id == id)
            .where(Order.purchase_on >= start_date)
            .join(Customer.orders)
            .group_by(Customer.id)
        ).scalar()
        or 0
    )

    next_cycle_start_date = date(start_date.year + 1, start_date.month, start_date.day)
    next_cycle_customer_spending = (
        db.execute(
            select(sum(Order.total_in_cents))
            .where(Customer.id == id)
            .where(Order.purchase_on >= next_cycle_start_date)
            .join(Customer.orders)
            .group_by(Customer.id)
        ).scalar()
        or 0
    )

    customer_tier = cast(LoyaltyTier, customer.tier)
    will_downgrade_next_cycle = False
    if tier_minimum[customer_tier] > next_cycle_customer_spending:
        will_downgrade_next_cycle = True

    return CustomerLoyaltyInformation(
        purchase_amount_in_cents=customer_spending,
        purchase_amount_to_next_tier_in_cents=(
            max(tier_minimum[next_tier(customer_tier)] - customer_spending, 0)
        ),
        purchase_amount_period_from=start_date,
        current_tier=customer_tier,
        downgrade_tier=(
            calculate_tier(next_cycle_customer_spending)
            if will_downgrade_next_cycle
            else None
        ),
        downgrade_on=tier_end_date(),
        purchase_amount_to_maintain_tier_in_cents=(
            tier_minimum[customer_tier] - next_cycle_customer_spending
            if will_downgrade_next_cycle
            else 0
        ),
    )
