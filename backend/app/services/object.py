import json
import os
from datetime import datetime
from typing import List, Optional


DATA_FILE = "tasks.json"


class Task:
    def __init__(self, title: str, description: str, due_date: str,
                 priority: int, completed: bool = False, created_at: Optional[str] = None):
        self.title = title.strip()
        self.description = description.strip()
        self.due_date = due_date.strip()  # YYYY-MM-DD
        self.priority = priority  # 1 (low) to 5 (high)
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            priority=data["priority"],
            completed=data["completed"],
            created_at=data["created_at"]
        )


class TaskManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.tasks: List[Task] = []
        self.load()

    # ---------------- Persistence ----------------
    def load(self):
        if not os.path.exists(self.filepath):
            self.tasks = []
            return

        with open(self.filepath, "r") as f:
            data = json.load(f)
            self.tasks = [Task.from_dict(t) for t in data]

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    # ---------------- CRUD ----------------
    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save()

    def delete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save()

    def mark_complete(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save()

    # ---------------- Queries ----------------
    def list_tasks(self, show_completed: bool = True):
        for i, task in enumerate(self.tasks):
            if not show_completed and task.completed:
                continue
            self._print_task(i, task)

    def search(self, keyword: str):
        for i, task in enumerate(self.tasks):
            if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower():
                self._print_task(i, task)

    def sort_by_due_date(self):
        self.tasks.sort(key=lambda t: datetime.strptime(t.due_date, "%Y-%m-%d"))
        self.save()

    def sort_by_priority(self):
        self.tasks.sort(key=lambda t: t.priority, reverse=True)
        self.save()

    # ---------------- Helpers ----------------
    def _print_task(self, index: int, task: Task):
        status = "✓" if task.completed else "✗"
        print(f"""
[{index}] {task.title}  (Priority: {task.priority}) [{status}]
    Description : {task.description}
    Due Date    : {task.due_date}
    Created At  : {task.created_at}
        """)


# ---------------- Input Helpers ----------------
def input_date(prompt: str) -> str:
    while True:
        date_str = input(prompt)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")


def input_priority(prompt: str) -> int:
    while True:
        try:
            p = int(input(prompt))
            if 1 <= p <= 5:
                return p
        except ValueError:
            pass
        print("Priority must be between 1 and 5.")


# ---------------- CLI ----------------
def main():
    manager = TaskManager(DATA_FILE)

    MENU = """
==== Task Manager ====
1. Add Task
2. List Tasks
3. List Pending Tasks
4. Search Tasks
5. Mark Task Complete
6. Delete Task
7. Sort by Due Date
8. Sort by Priority
9. Exit
"""

    while True:
        print(MENU)
        choice = input("Choose: ").strip()

        if choice == "1":
            title = input("Title: ")
            desc = input("Description: ")
            due = input_date("Due date (YYYY-MM-DD): ")
            prio = input_priority("Priority (1-5): ")
            manager.add_task(Task(title, desc, due, prio))

        elif choice == "2":
            manager.list_tasks()

        elif choice == "3":
            manager.list_tasks(show_completed=False)

        elif choice == "4":
            kw = input("Keyword: ")
            manager.search(kw)

        elif choice == "5":
            idx = int(input("Task index: "))
            manager.mark_complete(idx)

        elif choice == "6":
            idx = int(input("Task index: "))
            manager.delete_task(idx)

        elif choice == "7":
            manager.sort_by_due_date()
            print("Sorted by due date.")

        elif choice == "8":
            manager.sort_by_priority()
            print("Sorted by priority.")

        elif choice == "9":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
