import tkinter as tk
from login import Login
from home import TaskManagerApp
import threading
import json

class AppManager:
    def __init__(self):
        self.login_window = None
        self.root = None

    def start(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0)

        on_login = lambda username, user_id, login_window: self.handle_login(username, user_id, login_window)
        self.login_window = Login(self.root, on_login=lambda username, user_id: on_login(username, user_id, self.login_window))
        
        self.login_window.protocol("WM_DELETE_WINDOW", self.close_root)

        self.root.mainloop()

    def close_root(self):
        if self.root:
            if self.login_window:
                self.login_window.destroy()
            self.root.destroy()

    def handle_login(self, username, user_id, login_window):
        if login_window:
            login_window.destroy()
        self.start_task_manager_app(username, user_id)

    def start_task_manager_app(self, username, user_id):
        user = self.retrieve_user(user_id)
        if user:
            threading.Thread(target=self.open_task_manager_app, args=(username, user_id, user)).start()
        else:
            print("User not found.")

    def open_task_manager_app(self, username, user_id, user):
        task_manager_app = TaskManagerApp(user)
        task_manager_app.current_user = username
        task_manager_app.current_user_id = user_id
        task_manager_app.mainloop()

    def retrieve_user(self, user_id):
        try:
            with open("data.json", "r") as file:
                users = json.load(file)
                for user in users:
                    if user.get("user_id") == user_id:
                        return user
        except FileNotFoundError:
            print("User data file not found.")
        except json.JSONDecodeError:
            print("Error decoding user data from JSON.")

        return None

if __name__ == "__main__":
    app_manager = AppManager()
    app_manager.start()