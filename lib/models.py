from sqlalchemy import ForeignKey, Table, Column, Integer, String, MetaData, func, DateTime, create_engine
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

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
    name = Column(String(), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    category_id = Column(Integer(), ForeignKey('categories.id'))

    @classmethod
    def all_items(cls):
        items = session.query(cls).all()
        return items
    @classmethod
    def add_item(cls, name, price, category_name, quantity):
        category = session.query(Category).filter_by(name = category_name).first()

        if not category:
            new_category = Category(name = category_name)
            session.add(new_category)
            session.commit()
            category = new_category

        new_item = cls(name = name, price = price, category_id = category.id)
        session.add(new_item)
        session.commit()

        new_stock = StockLevel(item_id = new_item.id, quantity = quantity)
        session.add(new_stock)
        session.commit()
    @classmethod
    def delete_item(cls, item_name):
        item = session.query(cls).filter_by(name = item_name).first()
        if item:
            session.delete(item)
            session.commit()
            print(f"Item has {item_name} been deleted")

    def __repr__(self):
        return f'<Item: id = {self.id}, ' + \
            f'name = {self.name}, ' + \
            f'price = {self.price}>'
    

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)

class StockLevel(Base):
    __tablename__ = 'stocklevels'

    id = Column(Integer(), primary_key=True)
    item_id = Column(Integer(), ForeignKey('items.id'))
    quantity = Column(Integer(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=func.now())
    

# class Supplier(Base):
#     pass