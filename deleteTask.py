import tkinter as tk
from tkinter import ttk
import json

class DeleteTask(tk.Toplevel):
    def __init__(self, parent, app, task_data, task_id):
        super().__init__(parent)
        self.title("Delete Task")
        self.task_data = task_data
        self.task_id = task_id
        self.app = app

        ttk.Label(self, text="Name: ").grid(row=0, column=0, sticky="e")
        ttk.Label(self, text=task_data[0]).grid(row=0, column=1)

        ttk.Label(self, text="Description: ").grid(row=1, column=0, sticky="e")
        ttk.Label(self, text=task_data[1]).grid(row=1, column=1)

        ttk.Label(self, text="Due Date: ").grid(row=2, column=0, sticky="e")
        ttk.Label(self, text=task_data[2]).grid(row=2, column=1)

        ttk.Label(self, text="Priority: ").grid(row=3, column=0, sticky="e")
        ttk.Label(self, text=task_data[3]).grid(row=3, column=1)

        ttk.Label(self, text="Are you sure you want to delete this task?").grid(row=4, columnspan=2)

        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_task)
        self.delete_button.grid(row=5, columnspan=2)

    def delete_task(self):
        try:
            with open("data.json", "r+") as file:
                data = json.load(file)
                user_index = next((index for index, user in enumerate(data) if user.get("user_id") == self.app.user['user_id']), None)
                if user_index is not None:
                    tasks = data[user_index].get("tasks", [])
                    task_index = next((index for index, task in enumerate(tasks) if task.get("id") == self.task_id), None)
                    if task_index is not None:
                        del tasks[task_index]

                        for index, task in enumerate(tasks, start=1):
                            task["id"] = index

                        data[user_index]["tasks"] = tasks

                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()

                        self.app.user = data[user_index]

                    else:
                        print("Task not found.")
                else:
                    print("User not found.")

        except FileNotFoundError:
            print("Data file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON.")

        self.app.load_tasks()
        self.destroy()
