import tkinter as tk
import datetime, calendar
import matplotlib.pyplot as plt
import numpy as num
from tkinter import ttk
from addTask import AddTask
from editTask import EditTask
from deleteTask import DeleteTask

class TaskManagerApp(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user

        self.title("Task Manager")
        self.geometry("1200x800")

        top_filter_frame = ttk.Frame(self)
        top_filter_frame.pack(side="top", fill="x")

        ttk.Label(top_filter_frame, text="Filter by:").grid(row=0, column=0, padx=(15, 0))
        ttk.Label(top_filter_frame, text="Sort by:").grid(row=0, column=3, padx=(15, 0))

        self.priority_var = tk.StringVar(value="Priority")
        self.priority_dropdown = ttk.OptionMenu(top_filter_frame, self.priority_var, "Priority", "Priority", "High", "Medium", "Normal", command=self.filter_priority)
        self.priority_dropdown.grid(row=0, column=1, padx=(0, 15))

        self.status_var = tk.StringVar(value="Status")
        self.status_dropdown = ttk.OptionMenu(top_filter_frame, self.status_var, "Status", "Status", "Pending", "In Progress", "Completed", command=self.filter_status)
        self.status_dropdown.grid(row=0, column=2, padx=(0, 15))

        self.sort_var = tk.StringVar(value="Sort")
        self.sort_dropdown = ttk.OptionMenu(top_filter_frame, self.sort_var, "Sort", "ID", "Title", "Due Date", "Priority", command=self.sort_tasks)
        self.sort_dropdown.grid(row=0, column=4, padx=(0, 15))

        ttk.Label(top_filter_frame, text="Filter by Title/Description:").grid(row=0, column=5, padx=(15, 0))
        self.filter_entry = ttk.Entry(top_filter_frame)
        self.filter_entry.grid(row=0, column=6, padx=(0, 15))

        self.filter_text_button = ttk.Button(top_filter_frame, text="Apply Filter", command=self.filter_text)
        self.filter_text_button.grid(row=0, column=7)

        ttk.Label(top_filter_frame, text="Filter by Date:").grid(row=0, column=8, padx=(15, 0))
        self.date_entry = tk.Entry(top_filter_frame)
        self.date_entry.grid(row=0, column=9, padx=(0, 15))

        self.filter_date_button = ttk.Button(top_filter_frame, text="Apply Filter", command=self.filter_by_specific_date)
        self.filter_date_button.grid(row=0, column=10)

        ttk.Label(top_filter_frame, text="Date Range:").grid(row=0, column=11, padx=(15, 0))
        self.date_range_var = tk.StringVar(value="All")
        self.date_range_dropdown = ttk.OptionMenu(top_filter_frame, self.date_range_var, "All", "All", "Today", "This Week", "This Month", "This Year", command=self.filter_date_range)
        self.date_range_dropdown.grid(row=0, column=12, padx=(0, 15))

        self.tasks_frame = ttk.Frame(self)
        self.tasks_frame.pack(fill="both", expand=True)

        self.tasks_label = ttk.Label(self.tasks_frame, text="Tasks:")
        self.tasks_label.pack()

        self.tasks_tree = ttk.Treeview(self.tasks_frame, columns=("ID", "Name", "Description", "Due Date", "Priority", "Status"), show="headings")
        self.tasks_tree.heading("ID", text="ID")
        self.tasks_tree.heading("Name", text="Name")
        self.tasks_tree.heading("Description", text="Description")
        self.tasks_tree.heading("Due Date", text="Due Date")
        self.tasks_tree.heading("Priority", text="Priority")
        self.tasks_tree.heading("Status", text="Status")

        self.tasks_tree.column("ID", width=40) 
        self.tasks_tree.column("Name", width=120)
        self.tasks_tree.column("Description", width=280)
        self.tasks_tree.column("Due Date", width=100)
        self.tasks_tree.column("Priority", width=100)
        self.tasks_tree.column("Status", width=100)

        self.tasks_tree.pack(fill="both", expand=True)

        bottom_button_frame = ttk.Frame(self)
        bottom_button_frame.pack(side="bottom", fill="x")

        self.add_task = ttk.Button(bottom_button_frame, text="Add Task", command=self.addTask)
        self.add_task.pack(side="left", padx=(15, 10))

        self.edit_task = ttk.Button(bottom_button_frame, text="Edit Task", command=self.editTask)
        self.edit_task.pack(side="left", padx=10)

        self.delete_task = ttk.Button(bottom_button_frame, text="Delete Task", command=self.deleteTask)
        self.delete_task.pack(side="left", padx=(10, 15))

        self.graph_button = ttk.Button(bottom_button_frame, text="Show Task Status Graph", command=self.task_status_graph)
        self.graph_button.pack(side="left", padx=(10, 15))

        self.load_tasks()

    def load_tasks(self):
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        if self.user:
            tasks = self.user.get("tasks", [])
            for task in tasks:
                task_id = task.get("id", "")
                name = task.get("name", "")
                description = task.get("description", "")
                due_date = task.get("dueDate", "")
                priority = task.get("priority", "")
                status = task.get("status", "")
                self.tasks_tree.insert("", "end", values=(task_id, name, description, due_date, priority, status))
        else:
            print("No user data available.")


    def filter_text(self):
        self.tasks_tree.delete(*self.tasks_tree.get_children())

        filter_text = self.filter_entry.get().lower()

        tasks = self.user.get("tasks", [])
        for task in tasks:
            title = task.get("name", "").lower()
            description = task.get("description", "").lower()
            if filter_text in title or filter_text in description:
                task_id = task.get("id", "")
                name = task.get("name", "")
                description = task.get("description", "")
                due_date = task.get("dueDate", "")
                priority = task.get("priority", "")
                status = task.get("status", "")
                self.tasks_tree.insert("", "end", values=(task_id, name, description, due_date, priority, status))

    def filter_by_specific_date(self):
        self.tasks_tree.delete(*self.tasks_tree.get_children())

        filter_date = self.date_entry.get()

        try:
            datetime.datetime.strptime(filter_date, "%Y-%m-%d")
        except ValueError:
            tk.messagebox.showerror("Invalid Date Format", "Date format must be YYYY-MM-DD")
            return

        tasks = self.user.get("tasks", [])
        for task in tasks:
            due_date = task.get("dueDate")
            if filter_date == due_date:
                task_id = task.get("id", "")
                name = task.get("name", "")
                description = task.get("description", "")
                due_date = task.get("dueDate", "")
                priority = task.get("priority", "")
                status = task.get("status", "")
                self.tasks_tree.insert("", "end", values=(task_id, name, description, due_date, priority, status))

                         
    def filter_date_range(self, selected_option):
        today = datetime.date.today()
        if selected_option == "All":
            self.load_tasks()
        elif selected_option == "Today":
            self.filter_date(today, today)
        elif selected_option == "This Week":
            start_of_week = today - datetime.timedelta(days=today.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)
            self.filter_date(start_of_week, end_of_week)
        elif selected_option == "This Month":
            start_of_month = today.replace(day=1)
            end_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1])
            self.filter_date(start_of_month, end_of_month)
        elif selected_option == "This Year":
            start_of_year = today.replace(month=1, day=1)
            end_of_year = today.replace(month=12, day=31)
            self.filter_date(start_of_year, end_of_year)

    
    def filter_date(self, start_date, end_date):
        self.tasks_tree.delete(*self.tasks_tree.get_children())

        tasks = self.user.get("tasks", [])
        for task in tasks:
            due_date = task.get("dueDate")
            due_date_obj = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
            if due_date_obj >= start_date and due_date_obj <= end_date:
                task_id = task.get("id", "")
                name = task.get("name", "")
                description = task.get("description", "")
                due_date = task.get("dueDate", "")
                priority = task.get("priority", "")
                status = task.get("status", "")
                self.tasks_tree.insert("", "end", values=(task_id, name, description, due_date, priority, status))


    def addTask(self):
        add_task_window = AddTask(self, self)

    def editTask(self):
        selected_item = self.tasks_tree.selection()
        if selected_item:
            item_data = self.tasks_tree.item(selected_item)
            task_data = item_data['values']
            task_id = task_data[0]
            edit_task_window = EditTask(self, self, task_data)

    def deleteTask(self):
        selected_item = self.tasks_tree.selection()
        if selected_item:
            item_data = self.tasks_tree.item(selected_item)
            task_data = item_data['values']
            task_id = task_data[0]
            delete_task_window = DeleteTask(self, self, task_data, task_id)

    def sort_tasks(self, selected_option):
        if selected_option == "Title":
            self.sort_by_title()
        elif selected_option == "Due Date":
            self.sort_by_due_date()
        elif selected_option == "Priority":
            self.sort_by_priority()
        elif selected_option == "ID":
            self.sort_by_id()
    
    def sort_by_title(self):
        items = list(self.tasks_tree.get_children())

        items.sort(key=lambda item: self.tasks_tree.item(item, "values")[1].lower())

        for index, item in enumerate(items, start=1):
            self.tasks_tree.move(item, "", index)

    def sort_by_due_date(self):
        items = list(self.tasks_tree.get_children())

        items.sort(key=lambda item: self.tasks_tree.item(item, "values")[3])

        for index, item in enumerate(items, start=1):
            self.tasks_tree.move(item, "", index)

    def sort_by_priority(self):
        items = list(self.tasks_tree.get_children())

        priority_order = {"High": 1, "Medium": 2, "Low": 3}

        items.sort(key=lambda item: priority_order.get(self.tasks_tree.item(item, "values")[4], 4))

        for index, item in enumerate(items, start=1):
            self.tasks_tree.move(item, "", index)

    def sort_by_id(self):
        items = list(self.tasks_tree.get_children())

        items.sort(key=lambda item: self.tasks_tree.item(item, "values")[0])

        for index, item in enumerate(items, start=1):
            self.tasks_tree.move(item, "", index)

    def filter_priority(self, selected_option):
        tasks = self.user.get("tasks", [])

        if self.status_var.get() != "Status":
            tasks = [task for task in tasks if task.get("status") == self.status_var.get()]

        if selected_option == "Priority":
            filtered_tasks = tasks
        else:
            filtered_tasks = [task for task in tasks if task.get("priority") == selected_option]

        self.tasks_tree.delete(*self.tasks_tree.get_children())

        for task in filtered_tasks:
            self.tasks_tree.insert("", "end", values=(task["id"], task["name"], task["description"], task["dueDate"], task["priority"], task["status"]))


    def filter_status(self, selected_option):
        tasks = self.user.get("tasks", [])

        if self.priority_var.get() != "Priority":
            tasks = [task for task in tasks if task.get("priority") == self.priority_var.get()]

        if selected_option == "Status":
            filtered_tasks = tasks
        else:
            filtered_tasks = [task for task in tasks if task.get("status") == selected_option]

        self.tasks_tree.delete(*self.tasks_tree.get_children())

        for task in filtered_tasks:
            self.tasks_tree.insert("", "end", values=(task["id"], task["name"], task["description"], task["dueDate"], task["priority"], task["status"]))


    def task_status_graph(self):
        stats_count = {"Pending": 0, "In Progress": 0, "Completed": 0}
        tasks = self.user.get("tasks", [])
        for task in tasks:
            status = task.get("status", "")
            if status in stats_count:
                stats_count[status] += 1

        statuses = list(stats_count.keys())
        counts = list(stats_count.values())
        x = num.arange(len(statuses))

        colors=['red', 'green', 'blue']

        plt.bar(x, counts, align='center', alpha=0.5, color=colors)
        plt.xticks(x, statuses)
        plt.ylabel('Number of tasks')
        plt.title('Task Status')

        plt.show()

if __name__ == "__main__":
    user = {...}
    app = TaskManagerApp(user)
    app.mainloop()