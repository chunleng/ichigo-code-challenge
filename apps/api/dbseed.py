from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import delete

from database import SessionLocal
from models.customer import Customer


def seed():
    db: Session = SessionLocal()
    db.execute(delete(Customer))
    db.add_all([Customer(name="TEST") for _ in range(10)])
    db.commit()
