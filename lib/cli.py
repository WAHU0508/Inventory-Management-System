from helpers import (
    exit_program,
    list_items,
    add_item
)

def main():
    while True:
        menu()
        choice = input(">>> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_items()
        elif choice == '2':
            add_item()
        else:
            print("Invalid Choice.")

def menu():
    print("Please select an option: ")
    print("0. Exit the program.")
    print("1. List all the items.")
    print("2. Add new item.")

if __name__ == "__main__":
    main()