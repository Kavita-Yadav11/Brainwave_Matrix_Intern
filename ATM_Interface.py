import tkinter as tk
from tkinter import messagebox
import json
import os

# Load accounts from a JSON file if it exists
def load_accounts():
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as file:
            return json.load(file)
    return {}

# Save accounts to a JSON file
def save_accounts():
    with open("accounts.json", "w") as file:
        json.dump(accounts, file)

# Simulated database (now loading from file)
accounts = load_accounts()

def create_account():
    def submit():
        username = username_entry.get()
        pin = pin_entry.get()

        if username in accounts:
            messagebox.showerror("Error", "Username already exists.")
            return

        if len(pin) != 4 or not pin.isdigit():
            messagebox.showerror("Error", "PIN must be a 4-digit number.")
            return

        accounts[username] = {"pin": pin, "balance": 0}
        save_accounts()  # Save the updated accounts to the file
        messagebox.showinfo("Success", f"Account created for {username}!")
        create_window.destroy()

    create_window = tk.Toplevel(root)
    create_window.title("Create Account")
    create_window.geometry("400x200")
    create_window.configure(bg="#D4A0A7")

    tk.Label(create_window, text="Username:", bg="#F7C8D3", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10)
    username_entry = tk.Entry(create_window, font=("Arial", 12))
    username_entry.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(create_window, text="PIN:", bg="#F7C8D3", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10)
    pin_entry = tk.Entry(create_window, show="*", font=("Arial", 12))
    pin_entry.grid(row=1, column=1, pady=10, padx=10)

    tk.Button(create_window, text="Submit", command=submit, font=("Arial", 12)).grid(row=2, columnspan=2, pady=20)

def login():
    def submit():
        username = username_entry.get()
        pin = pin_entry.get()

        if username not in accounts or accounts[username]["pin"] != pin:
            messagebox.showerror("Error", "Invalid username or PIN.")
            return

        login_window.destroy()
        atm_menu(username)

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x200")
    login_window.configure(bg= "#D4A0A7")

    tk.Label(login_window, text="Username:", bg="#F7C8D3", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10)
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    username_entry.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(login_window, text="PIN:", bg="#F7C8D3", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10)
    pin_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
    pin_entry.grid(row=1, column=1, pady=10, padx=10)

    tk.Button(login_window, text="Submit", command=submit, font=("Arial", 12)).grid(row=2, columnspan=2, pady=20)

def atm_menu(username):
    def deposit():
        def submit():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError
                accounts[username]["balance"] += amount
                save_accounts()  # Save updated account balance
                messagebox.showinfo("Success", f"Deposited {amount}. New balance: {accounts[username]['balance']}")
                deposit_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount.")

        deposit_window = tk.Toplevel(root)
        deposit_window.title("Deposit")
        deposit_window.geometry("400x200")
        deposit_window.configure(bg="#f0f0f0")

        tk.Label(deposit_window, text="Amount:", bg="#FFFFFF", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10)
        amount_entry = tk.Entry(deposit_window, font=("Arial", 12))
        amount_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Button(deposit_window, text="Submit", command=submit, font=("Arial", 12)).grid(row=1, columnspan=2, pady=20)

    def withdraw():
        def submit():
            try:
                amount = float(amount_entry.get())
                if amount <= 0 or amount > accounts[username]["balance"]:
                    raise ValueError
                accounts[username]["balance"] -= amount
                save_accounts()  # Save updated account balance
                messagebox.showinfo("Success", f"Withdrew {amount}. New balance: {accounts[username]['balance']}")
                withdraw_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount or insufficient balance.")

        withdraw_window = tk.Toplevel(root)
        withdraw_window.title("Withdraw")
        withdraw_window.geometry("400x200")
        withdraw_window.configure(bg="#FFFFFF")

        tk.Label(withdraw_window, text="Amount:", bg="#FFFFFF", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10)
        amount_entry = tk.Entry(withdraw_window, font=("Arial", 12))
        amount_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Button(withdraw_window, text="Submit", command=submit, font=("Arial", 12)).grid(row=1, columnspan=2, pady=20)

    def check_balance():
        messagebox.showinfo("Balance", f"Your balance is: {accounts[username]['balance']}")

    def change_pin():
        def submit():
            current_pin = current_pin_entry.get()
            new_pin = new_pin_entry.get()

            if accounts[username]["pin"] != current_pin:
                messagebox.showerror("Error", "Incorrect current PIN.")
                return

            if len(new_pin) != 4 or not new_pin.isdigit():
                messagebox.showerror("Error", "PIN must be a 4-digit number.")
                return

            accounts[username]["pin"] = new_pin
            save_accounts()  # Save updated pin
            messagebox.showinfo("Success", "PIN changed successfully.")
            pin_window.destroy()

        pin_window = tk.Toplevel(root)
        pin_window.title("Change PIN")
        pin_window.geometry("400x200")
        pin_window.configure(bg="#f0f0f0")

        tk.Label(pin_window, text="Current PIN:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10)
        current_pin_entry = tk.Entry(pin_window, show="*", font=("Arial", 12))
        current_pin_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(pin_window, text="New PIN:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10)
        new_pin_entry = tk.Entry(pin_window, show="*", font=("Arial", 12))
        new_pin_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Button(pin_window, text="Submit", command=submit, font=("Arial", 12)).grid(row=2, columnspan=2, pady=20)

    atm_window = tk.Toplevel(root)
    atm_window.title(f"Welcome, {username}")
    atm_window.geometry("400x400")
    atm_window.configure(bg="#98FB98")

    tk.Button(atm_window, text="Deposit", command=deposit, font=("Arial", 12), width=20).pack(pady=10)
    tk.Button(atm_window, text="Withdraw", command=withdraw, font=("Arial", 12), width=20).pack(pady=10)
    tk.Button(atm_window, text="Check Balance", command=check_balance, font=("Arial", 12), width=20).pack(pady=10)
    tk.Button(atm_window, text="Change PIN", command=change_pin, font=("Arial", 12), width=20).pack(pady=10)
    tk.Button(atm_window, text="Logout", command=atm_window.destroy, font=("Arial", 12), width=20).pack(pady=10)

root = tk.Tk()
root.title("ATM Interface")
root.geometry("300x400")
root.configure(bg="#ADD8E6")
root.eval('tk::PlaceWindow . center')

# Main menu
tk.Label(root, text="ATM Interface", bg="#ADD8E6", font=("Arial", 16)).pack(pady=20)
tk.Button(root, text="Create Account", command=create_account, font=("Arial", 12), width=20).pack(pady=10)
tk.Button(root, text="Login", command=login, font=("Arial", 12), width=20).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12), width=20).pack(pady=10)

root.mainloop()
