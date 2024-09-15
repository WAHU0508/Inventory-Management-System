from models import Item, Category, StockLevel
from prettytable import PrettyTable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///inventories.db')
Session = sessionmaker(bind=engine)
session = Session()

def exit_program():
    print("Goodbye!!!!")
    exit()

def list_items():
    items = Item.all_items()
    table = PrettyTable(['id', 'Name', 'Price'])

    for item in items:
        table.add_row([item.id, item.name, item.price])

    print(table)

def add_item():
    name = input("    Enter the name of the new item: ")
    price = input("    Enter the price of the new item: ")
    category_name = input("    Enter the category name of the new item: ")
    quantity = input("    Enter the quantity of the new item: ")
    
    Item.add_item(name, price, category_name, quantity)
    new_item = session.query(Item).filter_by(name = name).first()
    if new_item:
        print(f"New Item {name} successfully added!!!")
    else:
        print(f"Error adding new item. Please Try Again.")
