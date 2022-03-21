from datetime import datetime
from typing import Final, cast

from fastapi.testclient import TestClient
from pytest import fixture
from pytest_freezegun import freeze_time
from sqlalchemy.orm.session import Session

from models.customer import Customer, LoyaltyTier
from models.order import Order
from routers.order import CreateOrderRequest
from util import tier_minimum

TARGET_URL: Final[str] = "/CreateOrder"


@fixture
def post_data():
    return CreateOrderRequest(
        customer_id="123",
        customer_name="Taro Suzuki",
        order_id="T123",
        total_in_cents=3450,
        date=datetime(2022, 3, 4, 5, 29, 59, 850),
    )


def test_create_order_new_customer(
    client: TestClient, post_data: CreateOrderRequest, db: Session
):
    response = client.post(TARGET_URL, data=post_data.json())

    assert response.status_code == 200
    assert response.json() == {}

    customer = cast(Customer, db.query(Customer).one())
    assert customer.id == post_data.customer_id
    assert customer.name == post_data.customer_name
    assert customer.tier == LoyaltyTier.bronze
    assert cast(Order, customer.orders[0]).id == post_data.order_id
    assert cast(Order, customer.orders[0]).total_in_cents == post_data.total_in_cents
    assert cast(Order, customer.orders[0]).purchase_on == post_data.date


def test_create_order_new_customer_promote_tier(
    client: TestClient, post_data: CreateOrderRequest, db: Session
):
    post_data.total_in_cents = tier_minimum[LoyaltyTier.gold]
    response = client.post(TARGET_URL, data=post_data.json())

    assert response.status_code == 200
    assert response.json() == {}

    customer = cast(Customer, db.query(Customer).one())
    assert customer.tier == LoyaltyTier.gold


def test_create_order_existing_customer(
    client: TestClient, post_data: CreateOrderRequest, db: Session
):
    db.add(Customer(id=post_data.customer_id, name=f"{post_data.customer_name} Before"))
    db.commit()
    response = client.post(TARGET_URL, data=post_data.json())

    assert response.status_code == 200
    assert response.json() == {}

    customer = cast(Customer, db.query(Customer).one())
    assert customer.name == post_data.customer_name


def test_create_order_promote_tier_with_existing_order(
    client: TestClient, post_data: CreateOrderRequest, db: Session
):
    db.add(Customer(id=post_data.customer_id, name=post_data.customer_name))
    db.add_all(
        [
            Order(id=str(i), total_in_cents=1, customer_id=post_data.customer_id)
            for i in range(2)
        ]
    )
    db.commit()
    post_data.total_in_cents = tier_minimum[LoyaltyTier.gold] - 2

    response = client.post(TARGET_URL, data=post_data.json())

    assert response.status_code == 200
    assert response.json() == {}

    customer = cast(Customer, db.query(Customer).one())
    assert customer.tier == LoyaltyTier.gold


@freeze_time("2022-03-24")
def test_create_order_promote_tier_with_expired_order(
    client: TestClient, post_data: CreateOrderRequest, db: Session
):
    db.add(Customer(id=post_data.customer_id, name=post_data.customer_name))
    db.add(
        Order(
            id="1",
            total_in_cents=1,
            customer_id=post_data.customer_id,
            purchase_on=datetime(2020, 12, 31),
        )
    )
    db.commit()
    post_data.total_in_cents = tier_minimum[LoyaltyTier.gold] - 1

    response = client.post(TARGET_URL, data=post_data.json())

    assert response.status_code == 200
    assert response.json() == {}
    customer = cast(Customer, db.query(Customer).one())
    assert customer.tier == LoyaltyTier.silver
