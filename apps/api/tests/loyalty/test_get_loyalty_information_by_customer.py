from datetime import datetime
from typing import Any, Final, cast

from fastapi.testclient import TestClient
from pytest import fixture
from pytest_freezegun import freeze_time
from sqlalchemy.orm.session import Session

from models.customer import Customer, LoyaltyTier
from models.order import Order
from util import tier_minimum

TARGET_URL_PREFIX: Final[str] = "/GetLoyaltyInformationByCustomer?id="


@fixture(autouse=True)
def setup(db: Session):
    db.add(Customer(id="123", name="Jack"))


@fixture
def order():
    return Order(id="T123", customer_id="123", total_in_cents=0)


def test_get_loyalty_information_by_customer_not_found(client: TestClient):
    response = client.get(TARGET_URL_PREFIX + "unknown")
    assert response.status_code == 404


def test_get_loyalty_information_by_customer_success_no_order_info(client: TestClient):
    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200

    ret = response.json()

    assert ret["purchase_amount_in_cents"] == 0
    assert (
        ret["purchase_amount_to_next_tier_in_cents"] == tier_minimum[LoyaltyTier.silver]
    )
    assert ret["current_tier"] == LoyaltyTier.bronze.value
    assert ret["downgrade_tier"] is None
    assert ret["purchase_amount_to_maintain_tier_in_cents"] == 0


@freeze_time("2020-01-01")
def test_get_loyalty_information_by_customer_start_of_year(client: TestClient):
    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200

    ret = response.json()
    assert datetime.strptime(
        ret["purchase_amount_period_from"], "%Y-%m-%d"
    ) == datetime(2019, 1, 1, 0, 0)
    assert datetime.strptime(ret["downgrade_on"], "%Y-%m-%d") == datetime(
        2020, 12, 31, 0, 0
    )


@freeze_time("2020-12-31")
def test_get_loyalty_information_by_customer_end_of_year(client: TestClient):
    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200

    ret = response.json()
    assert datetime.strptime(
        ret["purchase_amount_period_from"], "%Y-%m-%d"
    ) == datetime(2019, 1, 1, 0, 0)
    assert datetime.strptime(ret["downgrade_on"], "%Y-%m-%d") == datetime(
        2020, 12, 31, 0, 0
    )


@freeze_time("2020-03-24")
def test_get_loyalty_information_by_customer_downgrade_next_cycle(
    client: TestClient, db: Session, order: Order
):
    order.total_in_cents = cast(Any, tier_minimum[LoyaltyTier.gold])
    order.purchase_on = cast(Any, datetime(2019, 1, 1))
    db.add(order)
    customer = cast(Customer, db.query(Customer).get("123"))
    customer.tier = cast(Any, LoyaltyTier.gold)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200

    ret = response.json()
    assert ret["purchase_amount_in_cents"] == order.total_in_cents
    assert ret["downgrade_tier"] == LoyaltyTier.bronze.value
    assert (
        ret["purchase_amount_to_maintain_tier_in_cents"]
        == tier_minimum[LoyaltyTier.gold]
    )


@freeze_time("2020-03-24")
def test_get_loyalty_information_by_customer_downgrade_next_cycle_edge_case(
    client: TestClient, db: Session, order: Order
):
    order.total_in_cents = cast(Any, tier_minimum[LoyaltyTier.gold])
    order.purchase_on = cast(Any, datetime(2020, 1, 1))
    db.add(order)
    customer = cast(Customer, db.query(Customer).get("123"))
    customer.tier = cast(Any, LoyaltyTier.gold)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200

    ret = response.json()
    assert ret["downgrade_tier"] is None
    assert ret["purchase_amount_to_maintain_tier_in_cents"] == 0


def test_get_loyalty_information_by_customer_success_bronze(
    client: TestClient, db: Session, order: Order
):
    purchase_amount_in_cents = tier_minimum[LoyaltyTier.silver] - 1
    order.total_in_cents = cast(Any, purchase_amount_in_cents)
    db.add(order)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200

    ret = response.json()
    assert ret["purchase_amount_in_cents"] == purchase_amount_in_cents
    assert ret["purchase_amount_to_next_tier_in_cents"] == 1
    assert ret["current_tier"] == LoyaltyTier.bronze.value
    assert ret["downgrade_tier"] is None
    assert ret["purchase_amount_to_maintain_tier_in_cents"] == 0


def test_get_loyalty_information_by_customer_success_silver(
    client: TestClient, db: Session, order: Order
):
    purchase_amount_in_cents = tier_minimum[LoyaltyTier.gold] - 1
    order.total_in_cents = cast(Any, purchase_amount_in_cents)
    db.add(order)
    customer = cast(Customer, db.query(Customer).get("123"))
    customer.tier = cast(Any, LoyaltyTier.silver)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200

    ret = response.json()
    assert ret["purchase_amount_in_cents"] == purchase_amount_in_cents
    assert ret["purchase_amount_to_next_tier_in_cents"] == 1
    assert ret["current_tier"] == LoyaltyTier.silver.value
    assert ret["downgrade_tier"] is None
    assert ret["purchase_amount_to_maintain_tier_in_cents"] == 0


def test_get_loyalty_information_by_customer_success_gold(
    client: TestClient, db: Session, order: Order
):
    purchase_amount_in_cents = tier_minimum[LoyaltyTier.gold] + 1
    order.total_in_cents = cast(Any, purchase_amount_in_cents)
    db.add(order)
    customer = cast(Customer, db.query(Customer).get("123"))
    customer.tier = cast(Any, LoyaltyTier.gold)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200

    ret = response.json()
    assert ret["purchase_amount_in_cents"] == purchase_amount_in_cents
    assert ret["purchase_amount_to_next_tier_in_cents"] == 0
    assert ret["current_tier"] == LoyaltyTier.gold.value
    assert ret["downgrade_tier"] is None
    assert ret["purchase_amount_to_maintain_tier_in_cents"] == 0
