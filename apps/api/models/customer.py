from enum import Enum

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from database import Base


class LoyaltyTier(Enum):
    bronze = "bronze"
    silver = "silver"
    gold = "gold"


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    tier = Column(
        ENUM(LoyaltyTier), nullable=False, server_default=LoyaltyTier.bronze.value
    )

    orders = relationship("Order", back_populates="customer")
