from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Item, Category, StockLevel, Supplier

if __name__ == '__main__':
    engine = create_engine('sqlite:///inventories.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Item).delete()
    session.query(Category).delete()
    session.query(StockLevel).delete()
    session.query(Supplier).delete()

    categories = [
        Category(name = 'Electronics'),
        Category(name = 'Books'),
        Category(name = 'Fashion'),
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

    suppliers = [
        Supplier(name = 'Shein', contact = '25-360-479'),
        Supplier(name = 'Forever 21', contact = '25-360-489'),
        Supplier(name = 'Lenovo', contact = '25-330-479'),
        Supplier(name = 'HP', contact = '25-360-579'),
        Supplier(name = 'Apple Store', contact = '25-290-479'),
        Supplier(name = 'Textbook Center', contact = '25-280-479'),
        Supplier(name = 'Savanis', contact = '25-270-479'),
        Supplier(name = 'Shein', contact = '25-260-479'),
        Supplier(name = 'Al Yassin', contact = '25-250-479'),
        Supplier(name = 'Samsung', contact = '25-240-479'),
        Supplier(name = 'Zoey Kids', contact = '25-230-479')
    ]
    session.add_all(suppliers)
    session.commit()

    items[0].suppliers.append(suppliers[4])
    items[0].suppliers.append(suppliers[9])
    items[1].suppliers.append(suppliers[3])
    items[1].suppliers.append(suppliers[2])
    items[2].suppliers.append(suppliers[5])
    items[2].suppliers.append(suppliers[6])
    items[3].suppliers.append(suppliers[0])
    items[3].suppliers.append(suppliers[1])
    items[4].suppliers.append(suppliers[8])
    items[4].suppliers.append(suppliers[9])
    items[5].suppliers.append(suppliers[10])

    session.commit()
