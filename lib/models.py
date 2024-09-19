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

"""Item_suppliers association table"""
item_supplier = Table(
    'item_suppliers',
    Base.metadata,
    Column('item_id', ForeignKey('items.id'), primary_key=True),
    Column('supplier_id', ForeignKey('suppliers.id'), primary_key=True),
    extend_existing=True,
)

class Item(Base):
    """Create items table"""
    __tablename__ = 'items'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    category_id = Column(Integer(), ForeignKey('categories.id'))
    
    """one to one relationship"""
    stock_level = relationship("StockLevel", backref="item")
    """many to many relationship"""
    suppliers = relationship('Supplier', secondary=item_supplier, back_populates='items')

    @classmethod
    def all_items(cls):
        """Method to get all items"""
        items = session.query(cls).all()
        return items
    
    @classmethod
    def add_item(cls, name, price, category_name, quantity):
        """Method to add a new item and give it a category"""
        category = session.query(Category).filter_by(name = category_name).first()
        """If the category name doesn't exist, create a new category"""
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
    def delete_item(cls, item_name=None, item_id=None):
        """Method to delete an item be name or by id."""
        if item_name:
            item = session.query(cls).filter_by(name = item_name).first()
        if item_id:
            item = session.query(cls).filter_by(id = item_id).first()
        if item:
            stocks_level = session.query(StockLevel).filter_by(id = item.id).first()
            session.delete(item)
            session.delete(stocks_level)
            session.commit()
    
    def item_suppliers(self):
        """get an item's suppliers"""
        return self.suppliers
    
    def update_item(self, name=None, price=None, category_id=None):
        """Update an item's name, price or category id"""
        if name is not None:
            self.name = name
        if price is not None:
            self.price = price
        if category_id is not None:
            self.category_id = category_id
        session.commit()
        print(f"Item ID: {self.id} updated successfully.")


    def __repr__(self):
        return f'<Item: id = {self.id}, ' + \
            f'name = {self.name}, ' + \
            f'price = {self.price}>'
    

class Category(Base):
    """Create a categories table"""
    __tablename__ = 'categories'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)

    items = relationship("Item", backref="category")

    def items_in_category(self):
        """method to get items in a category"""
        return self.items
    

    def __repr__(self):
        return f'<Category: id = {self.id}, ' + \
            f'name = {self.name}>'

class StockLevel(Base):
    """Create stocklevels table"""
    __tablename__ = 'stocklevels'
    
    id = Column(Integer(), primary_key=True)
    item_id = Column(Integer(), ForeignKey('items.id'))
    quantity = Column(Integer(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=func.now())

    @classmethod
    def get_items_below_threshold(cls):
        """"Get items whose stocklevels are below threshold valu"""
        low_stock = session.query(cls).filter(cls.quantity < 50).all()

        low_stocked_items = []

        for stock in low_stock:
            item = session.query(Item).filter(Item.id == stock.item_id).first()
            if item:
                low_stocked_items.append(item)

        return low_stocked_items
    
    @classmethod
    def increase_stocks_level(cls, item_id, value = 0):
        """Increase stocks of item by a given value"""
        stocks = session.query(cls).filter_by(item_id = item_id).first()
        if stocks:
            stocks.quantity += value
            session.commit()

    @classmethod
    def decrease_stocks_level(cls, item_id, value = 0):
        """Decrease stocks of item by a given value"""
        stocks = session.query(cls).filter_by(item_id = item_id).first()
        if stocks:
            stocks.quantity -= value
            session.commit()    
    

    def __repr__(self):
        return f'<StockLevel: id = {self.id}, ' + \
            f'item_id = {self.item_id}, ' + \
            f'quantity = {self.quantity}>'
    
class Supplier(Base):
    """Create suppliers table"""
    __tablename__ = 'suppliers'

    id = Column(Integer(), primary_key = True)
    name = Column(String())
    contact = Column(String())

    items = relationship('Item', secondary=item_supplier, back_populates='suppliers')

    @classmethod
    def add_supplier(self, name, contact):
        """Create a new supplier"""
        new_supplier = Supplier(name = name, contact = contact)
        session.add(new_supplier)
        session.commit()

    def items_supplied(self):
        """Get items supplied by a supplier"""
        self.items

    def __repr__(self):
        return f'<Supplier: id = {self.id}, ' + \
            f'name = {self.name}, ' + \
            f'contact = {self.contact}>'
