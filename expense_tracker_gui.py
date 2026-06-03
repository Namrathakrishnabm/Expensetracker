import sqlite3
import csv
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt

income = 0
expense = 0

transactions = []

def add_income():
    global income

    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid amount"
        )
        return
   
    amount = float(amount_entry.get())
    category = category_var.get()

    income += amount
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    

    amount = float(amount_entry.get())
    category = category_var.get()

    income += amount
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
    "INSERT INTO transactions(type, category, amount, date) VALUES (?, ?, ?, ?)",
    ("Income", category, amount, current_date)
)

    conn.commit()
    conn.close()
    transactions.append(f"Income | {category} | ₹{amount}")

    history_listbox.insert(
    END,
    f"{current_date} | Income | {category} | ₹{amount}"
)
    update_balance()
    amount_entry.delete(0, END)

def add_expense():
    global expense

    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror(
             "Error",
             "Please enter a valid amount"
       )
        return
    amount = float(amount_entry.get())
    category = category_var.get()

    expense += amount
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        "INSERT INTO transactions(type, category, amount, date) VALUES (?, ?, ?, ?)",
        ("Expense", category, amount, current_date)
    )

    conn.commit()
    conn.close()
    transactions.append(f"Expense | {category} | ₹{amount}")

    history_listbox.insert(
    END,
    f"{current_date} | Expense | {category} | ₹{amount}"
)
    update_balance()
    amount_entry.delete(0, END)

def update_balance():
    balance = income - expense

    result_label.config(
        text=f"Income: ₹{income}\nExpense: ₹{expense}\nBalance: ₹{balance}"
    )
def load_transactions():
    global income, expense

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT type, category, amount, date FROM transactions"
    )

    rows = cursor.fetchall()

    for row in rows:
        trans_type, category, amount, date = row

        history_listbox.insert(
            END,
            f"{date} | {trans_type} | {category} | ₹{amount}"
        )

        if trans_type == "Income":
            income += amount
        else:
            expense += amount

    conn.close()

    update_balance()

def show_chart():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type='Expense'
        GROUP BY category
    """)

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No expense data available")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title("Expenses by Category")
    plt.show()
def export_csv():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT type, category, amount, date FROM transactions"
    )

    rows = cursor.fetchall()

    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Type", "Category", "Amount", "Date"])

        for row in rows:
            writer.writerow(row)

    conn.close()

    messagebox.showinfo(
    "Success",
    "CSV Exported Successfully!"
    )
def delete_transaction():
    selected = history_listbox.curselection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a transaction"
        )
        return

    history_listbox.delete(selected)
def select_all_transactions():
    history_listbox.select_set(0, END)
def delete_all_transactions():
    confirm = messagebox.askyesno(
        "Confirm",
        "Delete all transactions?"
    )

    if confirm:
        history_listbox.delete(0, END)

root = Tk()
root.title("Expense Tracker")
root.geometry("700x600")
root.configure(bg="#1E3A5F")

Label(
    root,
    text="Expense Tracker",
    font=("Arial", 18, "bold"),
    bg="#1E3A5F",
    fg="white"
).pack(pady=10)

Label(
    root,
    text="Amount",
    bg="#1E3A5F",
    fg="white"
).pack(pady=5)

amount_entry = Entry(root, width=30,font=("Arial",12))
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

Button(root,text="Add Income",command=add_income,width=20,font=("Arial", 10)).pack(pady=5)
Button(root, text="Add Expense", command=add_expense).pack(pady=5)
Button(root, text="Show Pie Chart", command=show_chart).pack(pady=5)
Button(root, text="Export CSV", command=export_csv).pack(pady=5)
Button(
    root,
    text="Delete Transaction",
    command=delete_transaction
).pack(pady=5)
Button(
    root,
    text="Select All",
    command=select_all_transactions
).pack(pady=5)
Button(
    root,
    text="Delete All",
    command=delete_all_transactions
).pack(pady=5)

result_label = Label(
    root,
    text="Income: ₹0\nExpense: ₹0\nBalance: ₹0",
    font=("Arial", 12)
)

result_label.pack(pady=10)

Label(root, text="Transaction History").pack()

history_listbox = Listbox(
    root,
    width=80,
    height=15,
    bg="#F8FAFC",
    fg="black"
)
history_listbox.pack(pady=10)

load_transactions()

root.mainloop()