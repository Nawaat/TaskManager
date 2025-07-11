import smtplib
import datetime
import csv
import re

class EmailService:
    """Service d'envoi d'emails (à mocker dans les tests)"""
    def __init__(self, smtp_server="smtp.gmail.com", port=587):
        self.smtp_server = smtp_server
        self.port = port

    def _validate_email(self, email):
        # Validation simple de l'email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Adresse email invalide")

    def send_task_reminder(self, email, task_title, due_date):
        self._validate_email(email)
        # Simulation d'envoi
        print(f"[SIMULATION] Rappel envoyé à {email} pour la tâche '{task_title}' avant le {due_date}")
        return True

    def send_completion_notification(self, email, task_title):
        self._validate_email(email)
        # Simulation d'envoi
        print(f"[SIMULATION] Notification de complétion envoyée à {email} pour la tâche '{task_title}'")
        return True

class ReportService:
    """Service de génération de rapports"""
    def generate_daily_report(self, tasks, date=None):
        if date is None:
            date = datetime.datetime.now().date()
        else:
            date = date.date() if isinstance(date, datetime.datetime) else date
        # Filtrer les tâches créées ou complétées ce jour-là
        tasks_of_day = [
            t for t in tasks
            if (t.created_at.date() == date) or (t.completed_at and t.completed_at.date() == date)
        ]
        total = len(tasks_of_day)
        completed = len([t for t in tasks_of_day if getattr(t, 'status', None) and t.status.name == 'DONE'])
        by_priority = {}
        by_status = {}
        for t in tasks_of_day:
            p = getattr(t, 'priority', None)
            s = getattr(t, 'status', None)
            if p:
                by_priority[p.name] = by_priority.get(p.name, 0) + 1
            if s:
                by_status[s.name] = by_status.get(s.name, 0) + 1
        return {
            "date": str(date),
            "total_tasks": total,
            "completed_tasks": completed,
            "tasks_by_priority": by_priority,
            "tasks_by_status": by_status,
        }

    def export_tasks_csv(self, tasks, filename):
        try:
            with open(filename, "w", newline='', encoding="utf-8") as csvfile:
                fieldnames = ["id", "title", "description", "priority", "status", "created_at", "completed_at", "project_id"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for t in tasks:
                    d = t.to_dict() if hasattr(t, 'to_dict') else dict(t)
                    writer.writerow(d)
        except Exception as e:
            print(f"Erreur lors de l'export CSV : {e}") 