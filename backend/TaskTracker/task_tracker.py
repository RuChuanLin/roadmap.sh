import argparse
import json
import os
from datetime import datetime

# File to store tasks
TASKS_FILE = "tasks.json"

def initialize_file():
    """Ensure the tasks file exists."""
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as file:
            json.dump([], file)

def add_task(description):
    """Add a new task to the list."""
    initialize_file()
    with open(TASKS_FILE, "r") as file:
        tasks = json.load(file)
    
    task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }
    tasks.append(task)
    
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)
    print(f"Task added: {task['id']} - {task['description']}")

def list_tasks(status=None):
    """List all tasks or filter by status."""
    initialize_file()
    with open(TASKS_FILE, "r") as file:
        tasks = json.load(file)
    
    if not tasks:
        print("No tasks available.")
        return
    
    filtered_tasks = tasks if status is None else [task for task in tasks if task["status"] == status]
    if not filtered_tasks:
        print(f"No tasks with status '{status}'.")
        return
    
    print(f"{'ID':<5} {'Status':<15} {'Description'}")
    print("-" * 40)
    for task in filtered_tasks:
        print(f"{task['id']:<5} {task['status']:<15} {task['description']}")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", choices=["todo", "in-progress", "done"], help="Filter tasks by status")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks(args.status)
    else:
        print("Invalid command or missing arguments.")


if __name__ == "__main__":
    main()
