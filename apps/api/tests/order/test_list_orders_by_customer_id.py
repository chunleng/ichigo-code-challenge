from copy import deepcopy
from datetime import date, datetime
from typing import Any, Final, cast

from pytest import fixture
from pytest_freezegun import freeze_time
from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient

from models.customer import Customer
from models.order import Order

TARGET_URL_PREFIX: Final[str] = "/ListOrdersByCustomerId?id="


@fixture(autouse=True)
def setup(db: Session):
    db.add(Customer(id="123", name="Jack"))


@fixture
def order():
    return Order(
        id="T123",
        total_in_cents=100,
        customer_id="123",
        purchase_on=datetime(2022, 3, 24),
    )


def test_list_orders_by_customer_id_not_found(client: TestClient):
    response = client.get(TARGET_URL_PREFIX + "unknown")
    assert response.status_code == 404


def test_list_orders_by_customer_id_none(client: TestClient):
    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200
    assert response.json() == []


def test_list_orders_by_customer_id_one(client: TestClient, db: Session, order: Order):
    db.add(order)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200

    ret = response.json()
    assert len(ret) == 1
    assert ret[0]["id"] == "T123"
    assert ret[0]["purchase_on"] == date(2022, 3, 24).strftime("%Y-%m-%d")
    assert ret[0]["total_in_cents"] == 100
    assert ret[0]["customer_id"] == "123"


def test_list_orders_by_customer_id_multiple(
    client: TestClient, db: Session, order: Order
):
    for i in range(2):
        o = deepcopy(order)
        o.id = cast(Any, str(i))
        db.add(o)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200

    assert len(response.json()) == 2


@freeze_time("2020-03-24")
def test_list_orders_by_customer_id_filter(
    client: TestClient, db: Session, order: Order
):
    order.purchase_on = cast(Any, datetime(2018, 12, 31))
    db.add(order)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200
    assert len(response.json()) == 0


@freeze_time("2020-03-24")
def test_list_orders_by_customer_id_filter_edge_case(
    client: TestClient, db: Session, order: Order
):
    order.purchase_on = cast(Any, datetime(2019, 1, 1))
    db.add(order)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_orders_by_customer_id_first_page(
    client: TestClient, db: Session, order: Order
):
    for i in range(3):
        o = deepcopy(order)
        o.id = cast(Any, str(i))
        db.add(o)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123&page=1&page_size=1")
    assert response.status_code == 200

    ret = response.json()
    assert len(ret) == 1
    assert ret[0]["id"] == "0"


def test_list_orders_by_customer_id_last_page(
    client: TestClient, db: Session, order: Order
):
    for i in range(3):
        o = deepcopy(order)
        o.id = cast(Any, str(i))
        db.add(o)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123&page=3&page_size=1")
    assert response.status_code == 200

    ret = response.json()
    assert len(ret) == 1
    assert ret[0]["id"] == "2"


def test_list_orders_by_customer_id_out_of_index_page(
    client: TestClient, db: Session, order: Order
):
    for i in range(3):
        o = deepcopy(order)
        o.id = cast(Any, str(i))
        db.add(o)
    db.commit()

    response = client.get(TARGET_URL_PREFIX + "123&page=4&page_size=1")
    assert response.status_code == 200

    assert len(response.json()) == 0
