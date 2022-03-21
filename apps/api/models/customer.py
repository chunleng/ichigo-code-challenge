from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
