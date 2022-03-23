# As type is not supported for Faker, use the following document for easy reference
# https://faker.readthedocs.io/en/master/providers.html
from datetime import datetime

from faker import Faker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import delete

from database import SessionLocal
from models.customer import Customer, LoyaltyTier
from models.order import Order

fake = Faker()


def seed():
    db: Session = SessionLocal()
    db.execute(delete(Order))
    db.execute(delete(Customer))
    db.add_all(
        [get_sample_customer(str(id), LoyaltyTier.bronze) for id in range(1, 4)]
        + [get_sample_customer(str(id), LoyaltyTier.silver) for id in range(4, 7)]
        + [get_sample_customer(str(id), LoyaltyTier.gold) for id in range(7, 10)]
    )
    db.commit()


def get_sample_customer(customer_id: str, tier: LoyaltyTier):
    if tier == LoyaltyTier.bronze:
        min_thousands_cent = 0
        max_thousands_cent = 9
    elif tier == LoyaltyTier.silver:
        min_thousands_cent = 10
        max_thousands_cent = 49
    elif tier == LoyaltyTier.gold:
        min_thousands_cent = 50
        max_thousands_cent = 100

    return Customer(
        id=customer_id,
        name=fake.name(),
        tier=tier,
        orders=[
            Order(
                id=f"T{customer_id}{i}",
                total_in_cents=1000,
                purchase_on=fake.past_date(
                    start_date=datetime(datetime.now().year - 1, 1, 1)
                ),
                customer_id=customer_id,
            )
            for i in range(
                fake.random_int(min=min_thousands_cent, max=max_thousands_cent)
            )
        ],
    )


if __name__ == "__main__":
    seed()
