import tkinter as tk
from tkinter import messagebox
from config import db_config
import mysql.connector


db = mysql.connector.connect(**db_config)
cursor = db.cursor()

# 🔐 Login Function
def login():
    acc = entry_acc.get().strip()
    pin = entry_pin.get().strip()

    if not acc or not pin:
        messagebox.showwarning("Error", "Please enter both Account No and PIN")
        return

    try:
        # Use strings in the query to avoid manual int conversion crashes
        cursor.execute("SELECT * FROM users WHERE account_no=%s AND pin=%s", (acc, pin))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", "Login Successful")
            main_screen(acc)
        else:
            messagebox.showerror("Error", "Invalid Account No or PIN")

    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")


# 🖥️ Main Dashboard
def main_screen(acc):
    window.destroy()
    main = tk.Tk()
    main.title("ATM Dashboard")
    main.geometry("300x300")

    tk.Label(main, text="Welcome to ATM", font=("Arial", 14)).pack(pady=10)

    tk.Button(main, text="Check Balance", width=20,
              command=lambda: check_balance(acc)).pack(pady=5)

    tk.Button(main, text="Deposit", width=20,
              command=lambda: deposit(acc)).pack(pady=5)

    tk.Button(main, text="Withdraw", width=20,
              command=lambda: withdraw(acc)).pack(pady=5)

    tk.Button(main, text="Transaction History", width=20,
              command=lambda: transactions(acc)).pack(pady=5)

    tk.Button(main, text="Exit", width=20, command=main.destroy).pack(pady=10)

    main.mainloop()


# 💰 Check Balance
def check_balance(acc):
    cursor.execute("SELECT balance FROM users WHERE account_no=%s", (acc,))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Balance", f"Current Balance: ₹{result[0]}")
    else:
        messagebox.showerror("Error", "Account not found")


# 💵 Deposit
def deposit(acc):
    amt = simple_input("Enter Deposit Amount")

    if amt is None:
        return

    cursor.execute("UPDATE users SET balance = balance + %s WHERE account_no=%s", (amt, acc))
    cursor.execute("INSERT INTO transactions(account_no,type,amount) VALUES(%s,'Deposit',%s)", (acc, amt))
    db.commit()

    messagebox.showinfo("Success", "Amount Deposited Successfully")


# 💸 Withdraw
def withdraw(acc):
    amt = simple_input("Enter Withdraw Amount")

    if amt is None:
        return

    cursor.execute("SELECT balance FROM users WHERE account_no=%s", (acc,))
    result = cursor.fetchone()

    if result and result[0] >= amt:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE account_no=%s", (amt, acc))
        cursor.execute("INSERT INTO transactions(account_no,type,amount) VALUES(%s,'Withdraw',%s)", (acc, amt))
        db.commit()

        messagebox.showinfo("Success", "Please collect your cash")
    else:
        messagebox.showerror("Error", "Insufficient Balance")


# 📜 Transaction History
def transactions(acc):
    cursor.execute("SELECT type, amount, date FROM transactions WHERE account_no=%s", (acc,))
    data = cursor.fetchall()

    if data:
        msg = ""
        for row in data:
            msg += f"{row[0]}  ₹{row[1]}  {row[2]}\n"

        messagebox.showinfo("Transactions", msg)
    else:
        messagebox.showinfo("Transactions", "No transactions found")


# 🧾 Input Box (Improved)
def simple_input(text):
    win = tk.Toplevel()
    win.title(text)
    win.geometry("250x120")

    tk.Label(win, text=text).pack(pady=5)
    entry = tk.Entry(win)
    entry.pack(pady=5)

    def submit():
        try:
            win.value = int(entry.get())
            win.destroy()
        except:
            messagebox.showerror("Error", "Enter valid number")

    tk.Button(win, text="Submit", command=submit).pack(pady=5)

    win.value = None
    win.wait_window()
    return win.value


# 🔐 Login Window
window = tk.Tk()
window.title("ATM Login")
window.geometry("300x200")

tk.Label(window, text="Account No").pack(pady=5)
entry_acc = tk.Entry(window)
entry_acc.pack(pady=5)

tk.Label(window, text="PIN").pack(pady=5)
entry_pin = tk.Entry(window, show="*")
entry_pin.pack(pady=5)

tk.Button(window, text="Login", command=login).pack(pady=10)

window.mainloop()