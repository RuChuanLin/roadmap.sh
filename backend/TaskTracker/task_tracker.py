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
        "id": 1 if not tasks else tasks[-1]["id"] + 1,
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

def update_task(task_id, description=None, status=None):
    """Update a task's description or status."""
    initialize_file()
    with open(TASKS_FILE, "r") as file:
        tasks = json.load(file)
    
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        print(f"Task with ID {task_id} not found.")
        return
    
    if description:
        task["description"] = description
    if status:
        task["status"] = status
    
    task["updatedAt"] = datetime.now().isoformat()
    
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)
    
    print(f"Task {task_id} updated successfully.")

def delete_task(task_id):
    """Delete a task by ID."""
    initialize_file()
    with open(TASKS_FILE, "r") as file:
        tasks = json.load(file)

    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        print(f"Task with ID {task_id} not found.")
        return

    tasks = [t for t in tasks if t["id"] != task_id]

    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {task_id} deleted successfully.")


def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", choices=["todo", "in-progress", "done"], help="Filter tasks by status")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("--description", help="New task description")
    update_parser.add_argument("--status", choices=["todo", "in-progress", "done"], help="New task status")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")
    

    # Parse arguments
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks(args.status)
    elif args.command == "update":
        update_task(args.id, args.description, args.status)
    elif args.command == "delete":
        delete_task(args.id)
    else:
        print("Invalid command or missing arguments.")


if __name__ == "__main__":
    main()
