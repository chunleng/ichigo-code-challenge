from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, autoincrement=False)
    total_in_cents = Column(Integer, nullable=False)
    purchase_on = Column(DateTime, server_default=now(), nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="orders", uselist=False)
