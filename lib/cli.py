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
    decrease_stocks
)

def main():
    while True:
        heading()
        items_below_stock()
        menu()
        choice = input(">>> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_items()
        elif choice == '2':
            add_item()
        elif choice == '3':
            print("DELETE ITEM BY NAME OR BY ID:")
            print("    0. Back to previous menu")
            print("    1. Delete by name")
            print("    2. Delete by id")
            choice = input(">>>> ")
            if choice == "0":
                menu()
            elif choice == "1":
                delete_item_by_name()
            elif choice == "2":
                delete_item_by_id()
            else:
                print("Invalid choice.")
        elif choice == '4':
            print("GET AN ITEM'S STOCK LEVEL:")
            print("    0. Back to previous menu")
            print("    1. Get stock level by item name")
            print("    2. Get stock level by item id")
            choice = input(">>>> ")
            if choice == "0":
                menu()
            elif choice == "1":
                get_stock_level_by_name()
            elif choice == "2":
                get_stock_level_by_id()
            else:
                print("Invalid choice.")
        elif choice == '5':
            print("UPDATE AN ITEM'S STOCK LEVEL:")
            print("    0. Back to previous menu")
            print("    1. Increase stocks")
            print("    2. Decrease stocks")
            choice = input(">>>> ")
            if choice == "0":
                menu()
            elif choice == '1':
                increase_stocks()
            elif choice == '2':
                decrease_stocks()
            else:
                print("Invalid choice.")
        else:
            print("Invalid Choice.")

def menu():
    print("Please select an option: ")
    print("0. Exit the program.")
    print("1. List all the items.")
    print("2. Add new item.")
    print("3. Delete an item.")
    print("4. Get item's stock level.")
    print("5. Update stocks.")

if __name__ == "__main__":
    main()