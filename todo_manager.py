import json
import os
from datetime import datetime

TODO_FILE = "tasks.json"

class Task:
    def __init__(self, title, description="", due_date=None, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", None),
            completed=data.get("completed", False)
        )

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        data = json.load(f)
        return [Task.from_dict(item) for item in data]

def save_tasks(tasks):
    with open(TODO_FILE, "w") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)

def add_task(title, description="", due_date=None):
    tasks = load_tasks()
    task = Task(title, description, due_date)
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{title}' added.")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for idx, task in enumerate(tasks, 1):
        status = "✓" if task.completed else "✗"
        print(f"{idx}. [{status}] {task.title} - {task.description} (Due: {task.due_date})")

def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index].completed = True
        save_tasks(tasks)
        print(f"Task '{tasks[index].title}' marked as completed.")
    else:
        print("Invalid task index.")

def main():
    while True:
        print("\nTo-Do Manager")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            title = input("Task title: ")
            desc = input("Description: ")
            due = input("Due date (YYYY-MM-DD): ")
            add_task(title, desc, due)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            idx = int(input("Task number to complete: ")) - 1
            complete_task(idx)
        elif choice == "4":
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
