from tkinter import *
from tkinter import ttk

income = 0
expense = 0

transactions = []

def add_income():
    global income
    amount = float(amount_entry.get())
    category = category_var.get()

    income += amount
    transactions.append(f"Income | {category} | ₹{amount}")

    history_listbox.insert(END, f"Income | {category} | ₹{amount}")

    update_balance()
    amount_entry.delete(0, END)

def add_expense():
    global expense
    amount = float(amount_entry.get())
    category = category_var.get()

    expense += amount
    transactions.append(f"Expense | {category} | ₹{amount}")

    history_listbox.insert(END, f"Expense | {category} | ₹{amount}")

    update_balance()
    amount_entry.delete(0, END)

def update_balance():
    balance = income - expense

    result_label.config(
        text=f"Income: ₹{income}\nExpense: ₹{expense}\nBalance: ₹{balance}"
    )

root = Tk()
root.title("Expense Tracker")
root.geometry("500x500")

Label(root, text="Amount").pack(pady=5)

amount_entry = Entry(root, width=30)
amount_entry.pack()

Label(root, text="Category").pack(pady=5)

category_var = StringVar()
category_box = ttk.Combobox(
    root,
    textvariable=category_var,
    values=["Food", "Travel", "Shopping", "Bills", "Education"]
)
category_box.pack()
category_box.current(0)

Button(root, text="Add Income", command=add_income).pack(pady=5)
Button(root, text="Add Expense", command=add_expense).pack(pady=5)

result_label = Label(
    root,
    text="Income: ₹0\nExpense: ₹0\nBalance: ₹0",
    font=("Arial", 12)
)
result_label.pack(pady=10)

Label(root, text="Transaction History").pack()

history_listbox = Listbox(root, width=50, height=10)
history_listbox.pack(pady=10)

root.mainloop()