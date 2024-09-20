# Inventory-Management-System
Sharon Gikenye's Project
Phase-3 End of Phase Project

This is an inventory management system that helps to streamline the tracking and management of stock in a more efficien, reliable and organized manner. This will enable businesses to monitor stock levels, categorize items and receive low-stock alerts, and generate detailed inventory reports, helping businesses to make informed decisions, reduce waste and improve overall operations. This system is built with Python and SQLAlchemy for database interactions. It allows users to manage items, suppliers and stock levels.

## Table of Contents
1. Features
2. Installation
3. How to run the Application
4. Usage
5. database Structure


### Features:
- Provide an easy to use command-line-interface for adding, updating and removing items from the inventory.
- Categorize items and track their stock levels.
- Alert users when the stock levels are low.
- Manage supplier information
- Create an order for items and write it in a txt file
- Generate inventory reports to provide an overview of the current stock status and write in a txt file.

### Installation
1. Clone this repository:
``` bash
    git clone git@github.com:WAHU0508/Inventory-Management-System.git
```
2. Run the following command to install all the application's dependencies and go into the virtual env:
``` bash
    pipenv install && pipenv shell
```
3. cd into the lib directory and run
``` bash
    python cli.py
```
This will launch the Inventory Management System's menu interface, where you can choose various options to manage the inventory.


### Usage
You will find a well structured user friendly command-line-interface which has the following functionalities:
0. Exit the program.
1. List all the items.
    Displays all items in the inventory in a table form.
2. Add, update or delete item.
    - add new items to the inventory and specify the supplier of the item.
    - update the name, price or category of an existing item.
    - Delete an item by name or by ID
3. Get item's stock level.
    - Check the stocks level of an item by it's name or by ID.
4. Update stocks.
    - Increase or decrease an item's stock-levels
5. Suppliers menu.
    - View suppliers associated with items.
6. Category menu.
    - View categories associated with items.
7. Write order
    - create an order and write it in the [orders.txt](./lib/orders.txt)
8. Generate Inventory Report 
    - generate a report and write it in the [report.txt](./lib/report.txt)

### Application Structure.
The application has the following tables: items, categories, stocklevels, suppliers and an association table.
The relationships are as follows:
    categories - items (one to many)
    items - stocklevels (one to one)
    items - suppliers (many to many)
This design was best in order to have proper design flexibility and scalability. The separation of concerns, flexibility management and normalization were taken into consideration for the design process.
cd into the [lib folder](./lib) to access [models.py](./lib/models.py), [helpers.py](./lib/helpers.py) and [cli.py](./lib/cli.py)
The data is seeded to the database py running 
``` bash
    python seed.py
```
in the lib directory.

### Contributing
If you'd like o contribute to the project, feel free to submit a pull request with detailed information on what you've added or changed. Please ensure that your changes are tested and do not break any existing functionality.