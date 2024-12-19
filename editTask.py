import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import json

class EditTask(tk.Toplevel):
    def __init__(self, parent, app, task_data):
        super().__init__(parent)
        self.app = app
        self.title("Edit Task")
        self.task_data = task_data

        ttk.Label(self, text="Name: ").grid(row=0, column=0, sticky="e")
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, task_data[1])
        self.name_entry.grid(row=0, column=1)

        ttk.Label(self, text="Description: ").grid(row=1, column=0, sticky="e")
        self.description_entry = ttk.Entry(self)
        self.description_entry.insert(0, task_data[2])
        self.description_entry.grid(row=1, column=1)

        ttk.Label(self, text="Due Date: ").grid(row=2, column=0, sticky="e")
        self.dueDate_entry = DateEntry(self, selectmode="day", date_pattern="yyyy-mm-dd", date=task_data[3])
        self.dueDate_entry.grid(row=2, column=1)

        ttk.Label(self, text="Priority").grid(row=3, column=0, sticky="e")
        self.priority_combobox = ttk.Combobox(self, values=["Normal", "Medium", "High"])
        self.priority_combobox.insert(0, task_data[4])
        self.priority_combobox.grid(row=3, column=1)

        ttk.Label(self, text="Status").grid(row=4, column=0, sticky="e")
        self.status_combobox = ttk.Combobox(self, values=["Pending", "In Progress", "Completed"])
        self.status_combobox.insert(0, task_data[5])
        self.status_combobox.grid(row=4, column=1)

        self.save_button = ttk.Button(self, text="Save Changes", command=self.save_changes)
        self.save_button.grid(row=5, columnspan=2)

    def save_changes(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        due_date = self.dueDate_entry.get()
        priority = self.priority_combobox.get()
        status = self.status_combobox.get()
        formatted_due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').strftime('%Y-%m-%d')

        with open("data.json", "r") as file:
            data = json.load(file)

        if self.app.user:
            for user_data in data:
                tasks = user_data.get("tasks", [])
                for task in tasks:
                    if task["id"] == self.task_data[0]:
                        task["name"] = name
                        task["description"] = description
                        task["dueDate"] = formatted_due_date
                        task["priority"] = priority
                        task["status"] = status
                        break

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

        self.app.user = self.reload_user_data()

        self.app.load_tasks()
        self.destroy()

    def reload_user_data(self):
        with open("data.json", "r") as file:
            all_users_data = json.load(file)
        
        for user_data in all_users_data:
            if user_data['user_id'] == self.app.user['user_id']:
                return user_data
        return None
