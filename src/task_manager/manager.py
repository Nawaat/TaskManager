import json
from typing import List, Optional
from .task import Task, Priority, Status
import os

class TaskManager:
    """Gestionnaire principal des tâches"""
    def __init__(self, storage_file="tasks.json"):
        self.tasks: List[Task] = []
        self.storage_file = storage_file

    def add_task(self, title, description="", priority=Priority.MEDIUM):
        task = Task(title, description, priority)
        self.tasks.append(task)
        return task.id

    def get_task(self, task_id) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks_by_status(self, status: Status) -> List[Task]:
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        return [task for task in self.tasks if task.priority == priority]

    def delete_task(self, task_id) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def save_to_file(self, filename=None):
        file = filename or self.storage_file
        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def load_from_file(self, filename=None):
        file = filename or self.storage_file
        if not os.path.exists(file):
            self.tasks = []
            return
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                print("DEBUG - JSON chargé :", data)  # 👈 ajoute ça
                self.tasks = [Task.from_dict(d) for d in data]
                print("DEBUG - Tâches recréées :", self.tasks)  # 👈 et ça
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
            self.tasks = []

    def get_statistics(self):
        stats = {
            "total_tasks": len(self.tasks),
            "completed_tasks": len([t for t in self.tasks if t.status == Status.DONE]),
            "tasks_by_priority": {},
            "tasks_by_status": {},
        }
        for p in Priority:
            stats["tasks_by_priority"][p.name] = len([t for t in self.tasks if t.priority == p])
        for s in Status:
            stats["tasks_by_status"][s.name] = len([t for t in self.tasks if t.status == s])
        return stats
