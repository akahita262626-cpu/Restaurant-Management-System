import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

MENU_FILE = "menu.csv"
ORDER_FILE = "orders.csv"


# Initialize order file
def init_order_file():
    try:
        pd.read_csv(ORDER_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Customer", "Item", "Quantity", "Price", "Total"])
        df.to_csv(ORDER_FILE, index=False)


# Initialize menu file (only once)
def init_menu_file():
    try:
        pd.read_csv(MENU_FILE)
    except FileNotFoundError:
        menu = pd.DataFrame({
            "ItemID": [1, 2, 3],
            "ItemName": ["Burger", "Pizza", "Pasta"],
            "Price": [120, 250, 180]
        })
        menu.to_csv(MENU_FILE, index=False)


# Show menu
def show_menu():
    menu = pd.read_csv(MENU_FILE)
    print("\n--- MENU ---")
    print(menu)


# Take order
def take_order():
    menu = pd.read_csv(MENU_FILE)
    customer = input("Customer Name: ")

    show_menu()

    try:
        item_id = int(input("Enter Item ID: "))
        qty = int(input("Quantity: "))
    except ValueError:
        print("❌ Invalid input!")
        return

    item = menu[menu["ItemID"] == item_id]

    if item.empty:
        print("❌ Item ID not found!")
        return

    price = item.iloc[0]["Price"]
    item_name = item.iloc[0]["ItemName"]
    total = price * qty

    order = pd.DataFrame(
        [[customer, item_name, qty, price, total]],
        columns=["Customer", "Item", "Quantity", "Price", "Total"]
    )

    order.to_csv(ORDER_FILE, mode='a', header=False, index=False)
    print(f"✅ Order Added! Bill Amount: ₹{total}")


# Total sales
def total_sales():
    df = pd.read_csv(ORDER_FILE)
    print("💰 Total Sales: ₹", np.sum(df["Total"]))


# Menu performance
def menu_performance():
    df = pd.read_csv(ORDER_FILE)

    if df.empty:
        print("No orders yet!")
        return

    performance = df.groupby("Item")["Quantity"].sum()
    print("\n📊 Menu Performance:\n", performance)

    performance.plot(kind='bar')
    plt.title("Menu Performance")
    plt.xlabel("Item")
    plt.ylabel("Quantity Sold")
    plt.show()


# Customer preferences
def customer_preferences():
    df = pd.read_csv(ORDER_FILE)

    if df.empty:
        print("No orders yet!")
        return

    pref = df.groupby("Customer")["Total"].sum()
    print("\n👤 Customer Preferences:\n", pref)


# Main menu
def main():
    init_menu_file()
    init_order_file()

    while True:
        print("""
1. Show Menu
2. Take Order
3. Total Sales
4. Menu Performance
5. Customer Preferences
6. Exit
""")
        try:
            choice = int(input("Choose option: "))
        except ValueError:
            print("❌ Invalid choice!")
            continue

        if choice == 1:
            show_menu()
        elif choice == 2:
            take_order()
        elif choice == 3:
            total_sales()
        elif choice == 4:
            menu_performance()
        elif choice == 5:
            customer_preferences()
        elif choice == 6:
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid Choice")


main()
