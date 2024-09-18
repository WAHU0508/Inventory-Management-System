from models import Item, Category, StockLevel, Supplier
from prettytable import PrettyTable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from colorama import Fore, Style, init

engine = create_engine('sqlite:///inventories.db')
Session = sessionmaker(bind=engine)
session = Session()

init(autoreset=True)

def heading():
    print(f"{Fore.CYAN}                                          AMAZON WAREHOUSE INVENTORY MANAGEMENT SYSTEM")
    print("------------------------------------------------------------------------------------------------------------------------\n")

def exit_program():
    print(f"{Fore.GREEN}Goodbye!!!!")
    exit()

def list_items():
    items = Item.all_items()
    table = PrettyTable(['id', 'Name', 'Price', 'StockLevel'])

    for item in items:
        stock = session.query(StockLevel).filter_by(item_id = item.id).first()
        stock_quantity = stock.quantity if stock else "Null"
        table.add_row([item.id, item.name, item.price, stock_quantity])

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

def delete_item_by_name():
    name = input("    Enter the name of the item to be deleted: ")
    item_to_be_deleted = session.query(Item).filter_by(name = name).first()
    confirmation = input(f"Are you sure you want to delete {item_to_be_deleted.name} with id {item_to_be_deleted.id}? (yes/no): ").lower()
    if confirmation == 'yes':
        Item.delete_item(item_name = name)
    else:
        print("Deletion Canceled.")

def delete_item_by_id():
    id = input("    Enter the id of the item to be deleted: ")
    item_to_be_deleted = session.query(Item).filter_by(id = id).first()
    confirmation = input(f"Are you sure you want to delete {item_to_be_deleted.name} with id {item_to_be_deleted.id}? (yes/no): ").lower()
    if confirmation == 'yes':
        Item.delete_item(item_id = id)
    else:
        print("Deletion Canceled.")

def get_stock_level_by_name():
    name = input("    Enter the item_name to get it's stock level.")
    item = session.query(Item).filter_by(name = name).first()
    stocks = session.query(StockLevel).filter_by(item_id = item.id).first()
    if item:
        print(f"Item {item.name}, has {stocks.quantity} items in stock.")
    else:
        print("Item not found.")

def get_stock_level_by_id():
    id = input("    Enter the item_id to get it's stock level.")
    item = session.query(Item).filter_by(id = id).first()
    stocks = session.query(StockLevel).filter_by(item_id = id).first()
    if item:
        print(f"Item {item.name}, has {stocks.quantity} items in stock.")
    else:
        print("Item not found.")

def items_below_stock():
    print(f"{Fore.RED}**********NOTIFICATIONS - LOW STOCKS < 50!!!**********")
    low_stocks = StockLevel.get_items_below_threshold()
    for item in low_stocks:
        for stock in item.stock_level:
            print(f"{Fore.LIGHTRED_EX}> id: {item.id}: {item.name} stockslevel is at {stock.quantity}")

def increase_stocks():
    id = input("Enter the id of item to be updated. ")
    value = input("Enter the number of new stocks added: ")
    item = session.query(Item).filter_by(id = id).first()
    if item:
        StockLevel.increase_stocks_level(id, int(value))

def decrease_stocks():
    id = input("Enter the id of item to be updated. ")
    value = input("Enter the amount decrease in stocks: ")
    item = session.query(Item).filter_by(id = id).first()
    stocks = session.query(StockLevel).filter_by(item_id = id).first()
    if item and stocks.quantity > int(value):
        StockLevel.decrease_stocks_level(id, int(value))
    else:
        print(f"{Fore.LIGHTYELLOW_EX}***The order is more than the available stock***")

def get_item_suppliers():
    id = input("Enter the id of item to check it's suppliers. ")
    item = session.query(Item).filter_by(id = id).first()
    suppliers = item.item_suppliers()
    for supplier in suppliers:
        print(f"Supplier's name: {supplier.name} Supplier's contact: {supplier.contact}")

def get_all_suppliers():
    suppliers = session.query(Supplier).all()

    table = PrettyTable(['Name', 'Contact'])

    for supplier in suppliers:
        table.add_row([supplier.name, supplier.contact])

    print(table)

def write_order():
    id = input("Enter id of item whose order is to be written. ")
    item = session.query(Item).filter_by(id = id).first()
    suppliers = item.suppliers
    print(f"item: {item.name}, id: {item.id} has suppliers:")
    for supplier in suppliers:
        print(f"id: {supplier.id}, name: {supplier.name}")
    orders = input("Enter oder in the format <id:quantity, id:quantity>: ")
    supply_order = [(int(supplier_id), int(quantity))
                    for supplier_id, quantity in (pair.split(':') for pair in orders.split(','))
                    ]
    item.write_order_if_stock_low(supply_order)
    print("The order has successfully been written!!!!")

def item_category():
    id = input("Enter id of item to get it's category. ")
    item = session.query(Item).filter_by(id = id).first()
    print(f"id: {item.id} name: {item.name} category: {item.category.name}")

def category_items():
    name = input("Enter name of category to get items. ")
    category = session.query(Category).filter_by(name = name).first()
    items = category.items
    print(f"Items in the {category.name} category")
    for item in items:
        print(f"id: {item.id} name: {item.name} price: {item.price}")
