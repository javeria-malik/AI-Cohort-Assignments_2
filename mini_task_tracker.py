"""
Mini Task Tracker
Week 1, Day 2 - AI Engineering Cohort Mini Project

A simple, menu-driven command-line task tracker that persists tasks 
in a local JSON file (tasks.json).
"""

import json
import os

# File where tasks are persisted
DATA_FILE = "tasks.json"

# Each task is stored as a dictionary: {"title": "Task description", "done": False}
tasks = []


def load_tasks():
    """
    Load tasks from tasks.json at startup.
    If the file does not exist or contains invalid JSON, starts with an empty list.
    """
    global tasks
    if not os.path.exists(DATA_FILE):
        tasks = []
        return tasks

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)
            if not isinstance(tasks, list):
                tasks = []
    except (json.JSONDecodeError, OSError):
        # Gracefully handle empty or malformed files
        tasks = []

    return tasks


def save_tasks():
    
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2)
    except OSError as error:
        print(f"Error saving tasks to file: {error}")


def add_task():
    title = input("Task title: ").strip()

    # Validate that title is not empty
    if not title:
        print("Task title cannot be empty.")
        return

    # Create new task dictionary
    new_task = {"title": title, "done": False}
    tasks.append(new_task)
    save_tasks()
    print("Task added.")


def view_tasks():
   
    if not tasks:
        print("No tasks found.")
        return

    for index, task in enumerate(tasks, start=1):
        status = "Done" if task.get("done") else "Pending"
        print(f"{index}. {task.get('title', '')} [{status}]")


def complete_task():
   
    if not tasks:
        print("No tasks available to complete.")
        return

    raw_input = input("Task number: ").strip()

    try:
        task_number = int(raw_input)
        if 1 <= task_number <= len(tasks):
            tasks[task_number - 1]["done"] = True
            save_tasks()
            print("Task completed.")
        else:
            print(f"Invalid task number. Please enter a number between 1 and {len(tasks)}.")
    except ValueError:
        print("Invalid input. Please enter a valid task number.")


def delete_task():
   
    if not tasks:
        print("No tasks available to delete.")
        return

    raw_input = input("Task number: ").strip()

    try:
        task_number = int(raw_input)
        if 1 <= task_number <= len(tasks):
            tasks.pop(task_number - 1)
            save_tasks()
            print("Task deleted.")
        else:
            print(f"Invalid task number. Please enter a number between 1 and {len(tasks)}.")
    except ValueError:
        print("Invalid input. Please enter a valid task number.")


def main():
   
    load_tasks()

    print("--- TASK TRACKER ---")
    print("1. Add  2. View  3. Complete  4. Delete  5. Exit")

    while True:
        choice = input("Choice: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()

