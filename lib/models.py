from sqlalchemy import ForeignKey, Table, Column, Integer, String, MetaData, func, DateTime, create_engine
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///inventories.db')
Session = sessionmaker(bind=engine)
session = Session()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(DECIMAL(10, 2))

    category_id = Column(Integer(), ForeignKey('categories.id'))

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

class StockLevel(Base):
    __tablename__ = 'stocklevels'

    id = Column(Integer(), primary_key=True)
    item_id = Column(Integer(), ForeignKey('items.id'))
    quantity = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    

# class Supplier(Base):
#     pass