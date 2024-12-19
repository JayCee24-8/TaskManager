# Task Manager Application

## Overview

**Task Manager Application** is a feature-rich tool for managing tasks. Built using Python with the **Tkinter** library for GUI development, this application includes functionalities such as user authentication, task CRUD operations, filtering, sorting, and task visualization through bar graphs. Data is stored in a JSON file for easy management and persistence.

---

## Features

### User Authentication
- **Login**: Users can log in with a username and password.
- **Sign Up**: New users can create accounts with a username and password.

### Task Management
- **Add Tasks**: Users can add new tasks with details like name, description, priority, due date, and status.
- **Edit Tasks**: Modify existing tasks.
- **Delete Tasks**: Remove tasks from the list.

### Filters and Sorting
- **Filter tasks by**:
  - Title/Description
  - Priority
  - Status
  - Due Date
- **Sort tasks by**:
  - Title
  - Due Date
  - Priority
  - ID

### Task Visualization
- **Bar Graph**: A graphical representation of tasks based on their status (Pending, In Progress, Completed).

### Data Storage
- All user and task data are stored in a JSON file (`data.json`) for persistence.

---

## File Structure

```plaintext
Task Manager/
│
├── app.py           # Entry point of the application
├── home.py          # Main application window for task management
├── login.py         # Login window
├── signup.py        # Signup window for new users
├── task.py          # Task model
├── addTask.py       # Add Task window
├── editTask.py      # Edit Task window
├── deleteTask.py    # Delete Task window
├── data.json        # JSON file for storing user and task data
```

## Getting Started

### Prerequisites
- **Python**: Version 3.6 or higher
- **matplotlib** library for visualization

### Installation
1. Clone the repository or download the source code.
2. Install the required dependencies:
   ```bash
   pip install matplotlib
3. Ensure data.json exists in the root directory with an initial empty user list: []

### Running the Application
Run the following command to start the application:
  ```bash
  python app.py
  ```
### Modules Description
- **app.py**:
  Manages the application flow:
  Displays the login window.
  Handles login and launches the task manager interface.
  Retrieves user data from ```data.json```.
  
- **home.py**:
  Implements the main task management UI.
  Features task listing, filtering, sorting, and graph generation.
  
- **login.py**:
  Provides a login interface.
  Authenticates users by matching credentials in data.json.
  
- **signup.py**:
  Allows new users to register.
  Adds new user data to data.json.
  
- **task.py**:
  Defines the Task model with attributes such as:
    - ID
    - name
    - description
    - priority
    - due_date
    - status


