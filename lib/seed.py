from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Item, Category, StockLevel

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Item).delete()
    session.query(Category).delete()
    session.query(StockLevel).delete()

    categories = [
        Category(name = 'Electronics'),
        Category(name = 'Books'),
        Category(name = 'Clothing'),
        Category(name = 'Home Appliances'),
        Category(name = 'Toys'),
    ]
    session.add_all(categories)
    session.commit()

    items = [
        Item(name = 'Smartphone', price = 699.99, category_id = 1),
        Item(name = 'Laptop', price = 999.99, category_id = 1),
        Item(name = 'The Great Gatsby', price = 10.99, category_id = 2),
        Item(name = 'Jeans', price = 39.99, category_id = 3),
        Item(name = 'Blender', price = 59.99, category_id = 4),
        Item(name = 'Teddy Bear', price = 99.99, category_id = 5)
    ]
    session.add_all(items)
    session.commit()

    stock_levels = [
        StockLevel(item_id = 1, quantity = 50),
        StockLevel(item_id = 2, quantity = 30),
        StockLevel(item_id = 3, quantity = 100),
        StockLevel(item_id = 4, quantity = 75),
        StockLevel(item_id = 5, quantity = 20),
        StockLevel(item_id = 6, quantity = 40)
    ]
    session.add_all(stock_levels)
    session.commit()