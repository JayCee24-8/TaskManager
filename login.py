import tkinter as tk
from tkinter import ttk, messagebox
import json
from signup import SignUp

class Login(tk.Tk):
    def __init__(self, parent, on_login=None):
        super().__init__()
        self.title("Login")
        self.on_login = on_login

        ttk.Label(self, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1)

        ttk.Label(self, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        self.signup_button = ttk.Button(self, text="Sign Up", command=self.open_signup_window)
        self.signup_button.grid(row=3, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_id = self.authenticate_user(username, password)
        if user_id:
            if self.on_login:   
                self.on_login(username, user_id)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_signup_window(self):
        signup_window = SignUp(self)
        signup_window.mainloop()

    def authenticate_user(self, username, password):
        with open("data.json", "r") as file:
            users = json.load(file)
        
        for user in users:
            if user["username"] == username and user["password"] == password:
                return user["user_id"]
        return None

if __name__ == "__main__":
    def on_login(username, user_id):
        print(f"User {username} with ID {user_id} logged in")

    login_window = Login(on_login=on_login)
    login_window.mainloop()
