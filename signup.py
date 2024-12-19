import tkinter as tk
from tkinter import ttk, messagebox
import json

class SignUp(tk.Tk):
    def __init__(self, parent):
        super().__init__()
        self.title("Sign Up")

        ttk.Label(self, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1)

        ttk.Label(self, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        ttk.Label(self, text="Confirm Password:").grid(row=2, column=0, sticky="e")
        self.confirm_password_entry = ttk.Entry(self, show="*")
        self.confirm_password_entry.grid(row=2, column=1)

        self.create_button = ttk.Button(self, text="Create New User", command=self.create_user)
        self.create_button.grid(row=3, columnspan=2)

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        with open("data.json", "r") as file:
            users = json.load(file)
        
        for user in users:
            if user["username"] == username:
                messagebox.showerror("Error", "Username already exists")
                return
        
        new_user = {"user_id": len(users) + 1, "username": username, "password": password, "tasks": []}
        users.append(new_user)
        with open("data.json", "w") as file:
            json.dump(users, file, indent=4)
        
        messagebox.showinfo("Success", "User created successfully")
        self.destroy()

if __name__ == "__main__":
    signup_window = SignUp(None)
    signup_window.mainloop()
