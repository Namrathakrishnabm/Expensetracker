import sqlite3
import csv
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt

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

    for item in tree.get_children():
        tree.delete(item)
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
    "SELECT id, type, category, amount, date FROM transactions"
    )

    rows = cursor.fetchall()

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

    history_listbox.delete(selected)
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
    history_listbox.select_set(0, END)
def delete_all_transactions():
    confirm = messagebox.askyesno(
        "Confirm",
        "Delete all transactions?"
    )

    if confirm:
        history_listbox.delete(0, END)
def search_transaction():
    keyword = search_var.get()

    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT type, category, amount, date
    FROM transactions
    WHERE category LIKE ?
    OR type LIKE ?
    OR date LIKE ?
""", (
    '%' + keyword + '%',
    '%' + keyword + '%',
    '%' + keyword + '%',
    '%' + keyword + '%'
))

    rows = cursor.fetchall()

    for row in rows:
        tree.insert(
            "",
            END,
            values=(
                "",
                row[0],
                row[1],
                row[2],
                row[3]
            )
      )

    conn.close()

root = Tk()
root.title("Expense Tracker")
root.geometry("700x600")
root.configure(bg="#121826")

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

search_var = StringVar()

Entry(
    root,
    textvariable=search_var,
    width=30
).pack()

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
Button(
    root,
    text="Edit Transaction",
    command=edit_transaction
).pack(pady=5)
Button(
    root,
    text="Search",
    command=search_transaction
).pack()
Button(
    root,
    text="Refresh",
    command=load_transactions
).pack()

cards_frame = Frame(root, bg=BG)
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

income_label.grid(row=0, column=0, padx=10)
expense_label.grid(row=0, column=1, padx=10)
balance_label.grid(row=0, column=2, padx=10)

Label(root, text="Transaction History").pack()

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
    root,
    columns=("ID", "Type", "Category", "Amount", "Date"),
    show="headings",
    height=12
)

tree.heading("ID", text="ID")
tree.heading("Type", text="Type")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Date", text="Date")

tree.column("ID", width=50)
tree.column("Type", width=100)
tree.column("Category", width=120)
tree.column("Amount", width=100)
tree.column("Date", width=200)

tree.pack(pady=10, fill="both", expand=True)

load_transactions()

root.mainloop()