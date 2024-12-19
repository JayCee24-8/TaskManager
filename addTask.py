import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from task import Task
import json

class AddTask(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.title("Add Task")
        self.app = app
        self.user = app.user

        ttk.Label(self, text="Name: ").grid(row=0, column=0, sticky="e")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        ttk.Label(self, text="Description: ").grid(row=1, column=0, sticky="e")
        self.description_entry = ttk.Entry(self)
        self.description_entry.grid(row=1, column=1)

        ttk.Label(self, text="Due Date: ").grid(row=2, column=0, sticky="e")
        self.due_date_entry = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.due_date_entry.grid(row=2, column=1)

        ttk.Label(self, text="Priority").grid(row=3, column=0, sticky="e")
        self.priority_combobox = ttk.Combobox(self, values=["Normal", "Medium", "High"])
        self.priority_combobox.grid(row=3, column=1)

        self.create_button = ttk.Button(self, text="Create Task", command=self.create_task)
        self.create_button.grid(row=4, columnspan=2)

    def create_task(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_combobox.get()
        formatted_due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').strftime('%Y-%m-%d')

        if name and due_date and priority:
            task_count = len(self.user.get('tasks', []))
            new_task_id = task_count + 1

            new_task = Task(id=new_task_id, name=name, description=description, status="Pending", due_date=formatted_due_date, priority=priority)

            self.user.setdefault('tasks', []).append(new_task.__dict__)

            with open("data.json", "r") as file:
                all_users_data = json.load(file)

            for user_data in all_users_data:
                if user_data['user_id'] == self.user['user_id']:
                    user_data.update(self.user)
                    break

            with open("data.json", "w") as file:
                json.dump(all_users_data, file, indent=4)

            messagebox.showinfo("Success", "Task created successfully")
            self.app.load_tasks()
            self.destroy()
            
        else:
            messagebox.showwarning("Warning", "Please fill in all required fields.")
