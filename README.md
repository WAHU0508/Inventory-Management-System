# Inventory-Management-System
Sharon Gikenye's Project
Phase-3 End of Phase Project

This is an inventory management system that helps to streamline the tracking and management of stock in a more efficien, reliable and organized manner. This will enable businesses to monitor stock levels, categorize items and receive low-stock alerts, and generate detailed inventory reports, helping businesses to make informed decisions, reduce waste and improve overall operations.

## The MVP features:
1. Provide an easy to use command-line-interface for adding, updating and removing items from the inventory.
2. Categorize items and track their stock levels.
3. Alert users when the stock levels are low.
4. Generate inventory reports to provide an overview of the current stock status.

## Application Design.
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

### Application Features
Run the following command to install all the application's dependencies:
``` bash
    pipenv install && pipenv shell
```
cd into lib folder then run:
``` bash
    python cli.py
```

You will find a well structured user friendly command-line-interface which has the following functionalities:
0. Exit the program.
1. List all the items.
2. Add, update or delete item.
3. Get item's stock level.
4. Update stocks where you can increase or decrease an item's stocklevels
5. Suppliers menu where you can get an item's suppliers or a list of all the suppliers
6. Category menu.
7. Write order - create an order and write it in the [orders.txt](./lib/orders.txt)
8. Generate Inventory Report - generate a report and write it in the [report.txt](./lib/report.txt)

