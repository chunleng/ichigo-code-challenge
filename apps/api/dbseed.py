from faker import Faker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import delete

from database import SessionLocal
from models.customer import Customer


def seed():
    fake = Faker()
    db: Session = SessionLocal()
    db.execute(delete(Customer))
    db.add_all([Customer(name=fake.name()) for _ in range(10)])
    db.commit()
