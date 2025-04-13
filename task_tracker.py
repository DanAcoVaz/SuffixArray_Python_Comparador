import os
import json
from datetime import datetime

TASK_FILE = "tasks.json"

class TaskEntry:
    def __init__(self, name, details="", deadline=None, done=False):
        self.name = name
        self.details = details
        self.deadline = deadline
        self.done = done

    def serialize(self):
        return {
            "name": self.name,
            "details": self.details,
            "deadline": self.deadline,
            "done": self.done
        }

    @classmethod
    def deserialize(cls, data):
        return cls(
            name=data["name"],
            details=data.get("details", ""),
            deadline=data.get("deadline", None),
            done=data.get("done", False)
        )

def read_tasks():
    if not os.path.isfile(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as file:
        items = json.load(file)
        return [TaskEntry.deserialize(obj) for obj in items]

def write_tasks(task_list):
    with open(TASK_FILE, "w") as file:
        json.dump([t.serialize() for t in task_list], file, indent=4)

def create_task(name, details="", deadline=None):
    task_list = read_tasks()
    new_task = TaskEntry(name, details, deadline)
    task_list.append(new_task)
    write_tasks(task_list)
    print(f"Added task: {name}")

def show_tasks():
    task_list = read_tasks()
    if not task_list:
        print("No tasks available.")
        return
    for i, task in enumerate(task_list, start=1):
        mark = "✔" if task.done else "✘"
        print(f"{i}. [{mark}] {task.name} - {task.details} (Due: {task.deadline})")

def mark_done(task_num):
    task_list = read_tasks()
    if 0 <= task_num < len(task_list):
        task_list[task_num].done = True
        write_tasks(task_list)
        print(f"Marked '{task_list[task_num].name}' as done.")
    else:
        print("Task index out of range.")

def start_app():
    while True:
        print("\nTask Tracker")
        print("1. New Task")
        print("2. View Tasks")
        print("3. Finish Task")
        print("4. Quit")
        user_choice = input("Choose: ")
        if user_choice == "1":
            name = input("Title: ")
            details = input("Details: ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            create_task(name, details, deadline)
        elif user_choice == "2":
            show_tasks()
        elif user_choice == "3":
            number = int(input("Which task to finish?: ")) - 1
            mark_done(number)
        elif user_choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    start_app()
