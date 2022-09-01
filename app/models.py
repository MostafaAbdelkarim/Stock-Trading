from sqlalchemy import Column, Integer, String, ForeignKey, Table
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class UserStock(Base):
    __tablename__ = "user_stock"
    Base.metadata

    user_id = Column(ForeignKey("users.id"), primary_key=True)
    stock_id = Column(ForeignKey("stocks.stock_id"), primary_key=True)
    quantity = Column(Integer)


class Stock(Base):
    __tablename__ = 'stocks'

    stock_id = Column(String, primary_key=True, nullable=False, default=uuid4)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    availability = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=text('now()'))
    users = relationship(
        "User", secondary=UserStock.__tablename__, back_populates='stocks')


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, nullable=False, default=uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    stocks = relationship("Stock", secondary=UserStock.__tablename__,
                          back_populates='users')
