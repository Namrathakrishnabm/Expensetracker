import sqlite3
import csv
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    category TEXT,
    amount REAL,
    date TEXT
)
""")

conn.commit()
conn.close()

BG = "#121826"
CARD = "#1E293B"
TEXT = "#F8FAFC"
ACCENT = "#3B82F6"

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
    
    cursor.execute(
    "INSERT INTO transactions(type, category, amount, date) VALUES (?, ?, ?, ?)",
    ("Income", category, amount, current_date)
)

    conn.commit()
    conn.close()
    transactions.append(f"Income | {category} | ₹{amount}")

    
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

    
    update_balance()
    amount_entry.delete(0, END)

def update_balance():
    balance = income - expense

    income_label.config(
          text=f"Income\n₹{income}"
    )

    expense_label.config(
           text=f"Expense\n₹{expense}"
    )

    balance_label.config(
           text=f"Balance\n₹{balance}"
    )
def load_transactions():
    global income, expense

    income = 0
    expense = 0

    for item in tree.get_children():
        tree.delete(item)
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
    "SELECT id, type, category, amount, date FROM transactions"
    )

    rows = cursor.fetchall()

    transactions_label.config(
    text=f"Transactions\n{len(rows)}"
    )
    for row in rows:
        trans_id, trans_type, category, amount, date = row

        tree.insert(
            "",
            END,
            values=(
               trans_id,
               trans_type,
               category,
               amount,
               date
            )
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
    selected = tree.selection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a transaction"
        )
        return

    item = tree.item(selected[0])
    trans_id = item["values"][0]

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id=?",
        (trans_id,)
    )

    conn.commit()
    conn.close()

    load_transactions()

    messagebox.showinfo(
        "Success",
        "Transaction deleted successfully!"
    )

def edit_transaction():

    selected = tree.selection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a transaction"
        )
        return

    item = tree.item(selected[0])
    trans_id = item["values"][0]

    edit_window = Toplevel(root)
    edit_window.title("Edit Transaction")
    edit_window.geometry("300x200")

    Label(edit_window, text="Amount").pack()

    amount_edit = Entry(edit_window)
    amount_edit.pack()

    Label(edit_window, text="Category").pack()

    category_edit = Entry(edit_window)
    category_edit.pack()

    def save_changes():

        new_amount = amount_edit.get()
        new_category = category_edit.get()

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE transactions
            SET category=?, amount=?
            WHERE id=?
            """,
            (
                new_category,
                new_amount,
                trans_id
            )
        )

        conn.commit()
        conn.close()

        load_transactions()

        edit_window.destroy()

        messagebox.showinfo(
            "Success",
            "Transaction Updated!"
        )

    Button(
        edit_window,
        text="Save",
        command=save_changes
    ).pack(pady=10)
def select_all_transactions():

    for item in tree.get_children():
        tree.selection_add(item)
def delete_all_transactions():

    confirm = messagebox.askyesno(
        "Confirm",
        "Delete all transactions?"
    )

    if confirm:

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM transactions"
        )

        conn.commit()
        conn.close()

        load_transactions()

        messagebox.showinfo(
            "Success",
            "All transactions deleted!"
        )
def search_transaction():

    keyword = search_var.get()
    selected_filter = filter_var.get()

    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # IVIDE PASTE CHEYYUKA
    if selected_filter == "Today":

        cursor.execute("""
            SELECT id, type, category, amount, date
            FROM transactions
            WHERE date(date) = date('now')
        """)

    elif selected_filter == "This Month":

        cursor.execute("""
            SELECT id, type, category, amount, date
            FROM transactions
            WHERE strftime('%Y-%m', date)
                  = strftime('%Y-%m', 'now')
        """)

    else:

        cursor.execute("""
            SELECT id, type, category, amount, date
            FROM transactions
            WHERE category LIKE ?
            OR type LIKE ?
            OR date LIKE ?
        """, (
            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%'
        ))

    rows = cursor.fetchall()

    for row in rows:
        tree.insert(
            "",
            END,
            values=row
      )

    conn.close()

root = Tk()
root.title("Expense Tracker")
root.geometry("700x600")
root.configure(bg=BG)

sidebar = Frame(root, bg="#0F172A", width=180)
sidebar.pack(side=LEFT, fill=Y)

content = Frame(root, bg=BG)
content.pack(side=RIGHT, fill=BOTH, expand=True)

button_frame = Frame(content, bg=BG)
button_frame.pack(pady=10)

Label(
    sidebar,
    text="Expense Tracker",
    bg="#0F172A",
    fg="white",
    font=("Arial", 14, "bold")
).pack(pady=20)

Button(sidebar, text="Dashboard", width=18).pack(pady=5)
Button(sidebar, text="Transactions", width=18).pack(pady=5)
Button(sidebar, text="Charts", width=18).pack(pady=5)
Button(sidebar, text="Export", width=18).pack(pady=5)

Label(
    content,
    text="Expense Tracker",
    font=("Arial", 18, "bold"),
    bg="#1E3A5F",
    fg="white"
).pack(pady=10)

Label(
    content,
    text="Amount",
    bg="#1E3A5F",
    fg="white"
).pack(pady=5)

amount_entry = Entry(content, width=30,font=("Arial",12))
amount_entry.pack()

Label(content, text="Category").pack(pady=5)

category_var = StringVar()
category_box = ttk.Combobox(
    content,
    textvariable=category_var,
    values=["Food", "Travel", "Shopping", "Bills", "Education"]
)
category_box.pack()
category_box.current(0)

search_var = StringVar()

Entry(
    content,
    textvariable=search_var,
    width=30
).pack()

filter_var = StringVar()

filter_box = ttk.Combobox(
    content,
    textvariable=filter_var,
    values=[
        "All",
        "Today",
        "This Month"
    ],
    width=20
)

filter_box.pack(pady=5)
filter_box.current(0)

Button(
    button_frame,
    text="Add Income",
    command=add_income
).grid(row=0, column=0, padx=5)

Button(
    button_frame,
    text="Add Expense",
    command=add_expense
).grid(row=0, column=1, padx=5)

Button(
    button_frame,
    text="Search",
    command=search_transaction
).grid(row=0, column=2, padx=5)

Button(
    button_frame,
    text="Refresh",
    command=load_transactions
).grid(row=0, column=3, padx=5)

Button(
    button_frame,
    text="Edit",
    command=edit_transaction
).grid(row=0, column=4, padx=5)

Button(
    button_frame,
    text="Delete",
    command=delete_transaction
).grid(row=0, column=5, padx=5)

Button(
    button_frame,
    text="Export",
    command=export_csv
).grid(row=0, column=6, padx=5)

Button(
    button_frame,
    text="Chart",
    command=show_chart
).grid(row=0, column=7, padx=5)

cards_frame = Frame(content, bg=BG)
cards_frame.pack(pady=10)

income_label = Label(
    cards_frame,
    text="Income\n₹0",
    bg="#16A34A",
    fg="white",
    width=15,
    height=3,
    font=("Arial", 12, "bold")
)

expense_label = Label(
    cards_frame,
    text="Expense\n₹0",
    bg="#DC2626",
    fg="white",
    width=15,
    height=3,
    font=("Arial", 12, "bold")
)

balance_label = Label(
    cards_frame,
    text="Balance\n₹0",
    bg="#2563EB",
    fg="white",
    width=15,
    height=3,
    font=("Arial", 12, "bold")
)

transactions_label = Label(
    cards_frame,
    text="Transactions\n0",
    bg="#7C3AED",
    fg="white",
    width=15,
    height=3,
    font=("Arial", 12, "bold")
)

transactions_label.grid(row=0, column=3, padx=10)

income_label.grid(row=0, column=0, padx=10)
expense_label.grid(row=0, column=1, padx=10)
balance_label.grid(row=0, column=2, padx=10)

Label(content, text="Transaction History").pack()

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="#1E293B",
    foreground="white",
    fieldbackground="#1E293B",
    rowheight=25
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)

tree = ttk.Treeview(
    content,
    columns=("ID", "Type", "Category", "Amount", "Date"),
    show="headings",
    height=12
)

tree.heading("ID", text="ID")
tree.heading("Type", text="Type")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Date", text="Date")

tree.column("ID", width=60)
tree.column("Type", width=120)
tree.column("Category", width=150)
tree.column("Amount", width=120)
tree.column("Date", width=220)

tree.pack(pady=10, fill="both", expand=True)

load_transactions()

root.mainloop()