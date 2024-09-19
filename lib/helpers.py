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
    """List all items in a table form"""
    items = Item.all_items()
    table = PrettyTable(['id', 'Name', 'Price', 'StockLevel'])

    for item in items:
        stock = session.query(StockLevel).filter_by(item_id = item.id).first()
        stock_quantity = stock.quantity if stock else "Null"
        table.add_row([item.id, item.name, item.price, stock_quantity])

    print(table)

def add_item():
    """"Create a new item and give it a category and a supplier"""
    name = input("    Enter the name of the new item: ")
    price = input("    Enter the price of the new item: ")
    category_name = input("    Enter the category name of the new item: ")
    quantity = input("    Enter the quantity of the new item: ")
    supplier_name = input("    Enter the supplier name of the new item: ")
    supplier = session.query(Supplier).filter_by(name = supplier_name).first()
    
    if not supplier:
        supplier_contact = input("    Enter the supplier contact of the new item: ")
        supplier = Supplier(name = supplier_name, contact = supplier_contact)
        session.add(supplier)
        session.commit()

    Item.add_item(name, price, category_name, quantity)
    new_item = session.query(Item).filter_by(name = name).first()
    new_item.suppliers.append(supplier)
    session.commit()
     
    if new_item:
        print(f"{Fore.GREEN}New Item {name} successfully added!!!")
    else:
        print(f"{Fore.RED}Error adding new item. Please Try Again.")
    

def delete_item_by_name():
    """Delete an item by it's name"""
    name = input("    Enter the name of the item to be deleted: ")
    item_to_be_deleted = session.query(Item).filter_by(name = name).first()
    if item_to_be_deleted:
        confirmation = input(f"Are you sure you want to delete {item_to_be_deleted.name} with id {item_to_be_deleted.id}? (yes/no): ").lower()
        if confirmation == 'yes':
            Item.delete_item(item_name = name)
            print(f"{Fore.GREEN}An item has been deleted")
        else:
            print(f"{Fore.YELLOW}Deletion Canceled.")
    else:
        print(f"{Fore.RED} Item with name {name} cannot be found.")

def delete_item_by_id():
    """Delete an item by it's ID"""
    id = input("    Enter the id of the item to be deleted: ")
    item_to_be_deleted = session.query(Item).filter_by(id = id).first()
    if item_to_be_deleted:
        confirmation = input(f"Are you sure you want to delete {item_to_be_deleted.name} with id {item_to_be_deleted.id}? (yes/no): ").lower()
        if confirmation == 'yes':
            Item.delete_item(item_id = id)
        else:
            print(f"{Fore.YELLOW}Deletion Canceled.")
            print(f"{Fore.GREEN}An item has been deleted")
    else:
       print(f"{Fore.RED} Item with ID {id} cannot be found.") 

def get_stock_level_by_name():
    """Get item stocklevel by name"""
    name = input("    Enter the item_name to get it's stock level.")
    item = session.query(Item).filter_by(name = name).first()
    stocks = session.query(StockLevel).filter_by(item_id = item.id).first()
    if item:
        print(f"{Fore.GREEN}Item {item.name}, has {stocks.quantity} items in stock.")
    else:
        print("Item not found.")

def get_stock_level_by_id():
    """Get item's stocklevel by entering it's ID"""
    id = input("    Enter the item_id to get it's stock level.")
    item = session.query(Item).filter_by(id = id).first()
    stocks = session.query(StockLevel).filter_by(item_id = id).first()
    if item:
        print(f"{Fore.GREEN}Item {item.name}, has {stocks.quantity} items in stock.")
    else:
        print("Item not found.")

def items_below_stock():
    """Get items below theshold value and display them"""
    print(f"{Fore.RED}**********NOTIFICATIONS - LOW STOCKS < 50!!!**********")
    low_stocks = StockLevel.get_items_below_threshold()
    for item in low_stocks:
        for stock in item.stock_level:
            print(f"{Fore.LIGHTRED_EX}> id: {item.id}: {item.name} stockslevel is at {stock.quantity}")

def increase_stocks():
    """Increase an item's stocks"""
    id = input("Enter the id of item to be updated. ")
    value = input("Enter the number of new stocks added: ")
    item = session.query(Item).filter_by(id = id).first()
    if item:
        StockLevel.increase_stocks_level(id, int(value))
        print(f"{Fore.GREEN} Stock level of item<id: {item.id}, name: {item.name}> increased to {[stock.quantity for stock in item.stock_level]}")

def decrease_stocks():
    """Decrease an item's stocks"""
    id = input("Enter the id of item to be updated. ")
    value = input("Enter the amount decrease in stocks: ")
    item = session.query(Item).filter_by(id = id).first()
    stocks = session.query(StockLevel).filter_by(item_id = id).first()
    if item and stocks.quantity > int(value):
        StockLevel.decrease_stocks_level(id, int(value))
        print(f"{Fore.GREEN} Stock level of item<id: {item.id}, name: {item.name}> decreased to {[(stock.quantity - int(value)) for stock in item.stock_level]}")
    else:
        print(f"{Fore.LIGHTYELLOW_EX}***The order is more than the available stock***")

def get_item_suppliers():
    """Get an item's suppliers"""
    id = input("Enter the id of item to check it's suppliers. ")
    item = session.query(Item).filter_by(id = id).first()
    suppliers = item.item_suppliers()
    table = PrettyTable(["Supplier's Name", "Supplier's Contact"])
    for supplier in suppliers:
        table.add_row([supplier.name, supplier.contact])
    print(table)

def get_all_suppliers():
    """Get all supplier's details and display in a table"""
    suppliers = session.query(Supplier).all()

    table = PrettyTable(['Name', 'Contact'])

    for supplier in suppliers:
        table.add_row([supplier.name, supplier.contact])

    print(table)


def write_order():
    """Write an order and write it in a file."""
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
    
    """Create a table to display information"""
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
    """Get an item's category"""
    id = input("Enter id of item to get it's category. ")
    item = session.query(Item).filter_by(id = id).first()
    print(f"{Fore.YELLOW}id: {item.id} name: {item.name} category: {item.category.name}")

def category_items():
    """Get all items in a category"""
    name = input("Enter name of category to get items. ")
    category = session.query(Category).filter_by(name = name).first()
    items = category.items
    print(f"Items in the {category.name} category")
    for item in items:
        print(f"{Fore.YELLOW}id: {item.id} name: {item.name} price: {item.price}")

def generate_inventory_report():
    """Generate an inventory report and write it in table form in a file."""
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

def update_item_by_id():
    """Update an item's details by entering it's ID"""
    id = input("Enter id of item to be updated. ")
    item = session.query(Item).filter_by(id = id).first()

    if item:
        print(f"{Fore.LIGHTGREEN_EX} Updating item with ID {id}...")
        new_name = input("Enter new name of the item (leave blank to keep current name): ")
        new_price = input("Enter new price of the item (leave blank to keep current price): ")
        new_category_id = input("Enter new category_id of the item (leave blank to keep current category_id): ")

        new_name = new_name if new_name else None
        new_price = float(new_price) if new_price else None
        new_category_id = int(new_category_id) if new_category_id else None

        item.update_item(name = new_name, price = new_price, category_id = new_category_id)
    else:
        print(f"{Fore.RED}Item with ID {id} not found.")
