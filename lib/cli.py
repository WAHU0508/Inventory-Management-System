from helpers import (
    heading,
    exit_program,
    list_items,
    add_item,
    delete_item_by_name,
    delete_item_by_id,
    get_stock_level_by_name,
    get_stock_level_by_id,
    items_below_stock,
    increase_stocks,
    decrease_stocks,
    get_item_suppliers,
    get_all_suppliers,
    write_order,
    item_category,
    category_items,
    update_item_by_id,
    generate_inventory_report
)

def main():
    heading()
    while True:
        items_below_stock()
        menu()
        choice = input(">>> ")
        if choice == "0":
            exit_program()

        elif choice == "1":
            list_items()

        elif choice == '2':
            while True:
                print("\nADD, UPDATE OR DELETE AN ITEM:")
                print("    0. Back to previous menu")
                print("    1. Add new item")
                print("    2. Update an item")
                print("    3. Delete an item")
                choice = input(">>>> ")
                if choice == "0":
                    break
                elif choice == "1":
                    add_item()
                elif choice == "2":
                    update_item_by_id()
                elif choice == "3":
                    while True:
                        print("\nDELETE ITEM BY NAME OR BY ID:")
                        print("    0. Back to previous menu")
                        print("    1. Delete by name")
                        print("    2. Delete by id")
                        choice = input(">>>> ")
                        if choice == "0":
                            break
                        elif choice == "1":
                            delete_item_by_name()
                        elif choice == "2":
                            delete_item_by_id()
                        else:
                            print("Invalid choice.")
                else:
                    print("Invalid choice.")

        elif choice == '3':
            while True:
                print("\nGET AN ITEM'S STOCK LEVEL:")
                print("    0. Back to previous menu")
                print("    1. Get stock level by item name")
                print("    2. Get stock level by item id")
                choice = input(">>>> ")
                if choice == "0":
                    break
                elif choice == "1":
                    get_stock_level_by_name()
                elif choice == "2":
                    get_stock_level_by_id()
                else:
                    print("Invalid choice.")
        elif choice == '4':
            while True:
                print("\nUPDATE AN ITEM'S STOCK LEVEL:")
                print("    0. Back to previous menu")
                print("    1. Increase stocks")
                print("    2. Decrease stocks")
                choice = input(">>>> ")
                if choice == "0":
                    break
                elif choice == '1':
                    increase_stocks()
                elif choice == '2':
                    decrease_stocks()
                else:
                    print("Invalid choice.")
        elif choice == '5':
            while True:
                print("\nSUPPLIERS MENU:")
                print("    0. Back to previous menu")
                print("    1. Check an item's suppliers")
                print("    2. Get all suppliers")
                choice = input(">>>> ")
                if choice == "0":
                    break
                elif choice == "1":
                    get_item_suppliers()
                elif choice == "2":
                    get_all_suppliers()
                else:
                    print("Invalid choice.")     
        elif choice == '6':
            while True:
                print("\nCATEGORY MENU:")
                print("    0. Back to previous menu")
                print("    1. Check an item's category")
                print("    2. Check items in a category")
                choice = input(">>>> ")
                if choice == "0":
                    break
                elif choice == '1':
                    item_category()
                elif choice == '2':
                    category_items()
                else:
                    print("Invalid choice.")
        elif choice == '7':
            write_order()
        elif choice == '8':
            generate_inventory_report()
        else:
            print("Invalid Choice.")

def menu():
    print("\nPlease select an option: ")
    print("0. Exit the program.")
    print("1. List all the items.")
    print("2. Add, update or delete item.")
    print("3. Get item's stock level.")
    print("4. Update stocks.")
    print("5. Suppliers menu.")
    print("6. Category menu.")
    print("7. Write order.")
    print("8. Generate Inventory Report.")

if __name__ == "__main__":
    main()