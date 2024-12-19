import tkinter as tk
from tkinter import ttk

class Task():
    def __init__(self, id, name, description, status, due_date, priority):
        self.id = id
        self.name = name
        self.description = description
        self.status = status
        self.dueDate = due_date
        self.priority = priority