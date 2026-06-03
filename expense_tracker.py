income = 0
expense = 0

while True:
    print("\n1. Add Income")
    print("2. Add Expense")
    print("3. Show Balance")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        amount = float(input("Enter income amount: "))
        income += amount

    elif choice == "2":
        amount = float(input("Enter expense amount: "))
        expense += amount

    elif choice == "3":
        print("Income:", income)
        print("Expense:", expense)
        print("Balance:", income - expense)

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")