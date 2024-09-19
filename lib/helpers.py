from models import Item, Category, StockLevel, Supplier
from prettytable import PrettyTable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from colorama import Fore, Style, init
import os

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
    if not item :
        print(f"Item with ID {id} not found.")
        return

    suppliers = item.suppliers
    print(f"item: {item.name}, id: {item.id} has suppliers:")
    for supplier in suppliers:
        print(f"id: {supplier.id}, name: {supplier.name}")

    orders = input("Enter oder in the format <id:quantity, id:quantity>: ")
    supply_orders = [(int(supplier_id), int(quantity))
                    for supplier_id, quantity in (pair.split(':') for pair in orders.split(','))
                    ]
    table = PrettyTable()
    table.field_names = ["Item ID", "Item Name", "Supplier_name", "Supplier_Contact", "Order Quantity"]

    for supplier_id, quantity in supply_orders:
        for supplier in item.suppliers:
            if supplier_id == supplier.id:
                table.add_row([item.id, item.name, supplier.name, supplier.contact, quantity])
    
    with open('orders.txt', 'a') as order_file:
        text = f"An order for <id: {item.id} name: {item.name}>"
        order_file.write(text.upper() + "\n")
        order_file.write(table.get_string() + "\n" + "\n")

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

def generate_inventory_report():
    items = session.query(Item).options(
        joinedload(Item.category),
        joinedload(Item.stock_level),
        joinedload(Item.suppliers)
    ).all()

    table = PrettyTable()
    table.field_names = ["Item ID", "Item Name", "Price", "Category", "Stock Level", "Suppliers", "Last Updated"]

    for item in items:
        category_name = item.category.name if item.category else "N/A"
        stock_level = item.stock_level[0].quantity if item.stock_level else  "N/A"
        suppliers = ", ".join([supplier.name for supplier in item.suppliers]) if item.suppliers else "N/A"
        last_updated = item.stock_level[0].updated_at.strftime("%Y-%m-%d %H:%M") if item.stock_level else "N/A"

        table.add_row([item.id, item.name, item.price, category_name, stock_level, suppliers, last_updated])
    print(table)

    with open("report.txt", "w") as report_file:
        report_file.write(str(table))
