import pytest
from unittest.mock import patch, Mock, mock_open
from src.task_manager.services import EmailService, ReportService
from src.task_manager.task import Task, Priority
from datetime import datetime

class TestEmailService:
    """Tests du service email avec mocks"""
    def setup_method(self):
        self.email_service = EmailService()

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_task_reminder_success(self, mock_smtp):
        """Test envoi rappel réussi"""
        # Le service simule l'envoi, donc on vérifie juste le retour
        result = self.email_service.send_task_reminder("test@example.com", "Tâche", "2024-06-13")
        assert result is True

    def test_send_task_reminder_invalid_email(self):
        """Test envoi avec email invalide"""
        with pytest.raises(ValueError):
            self.email_service.send_task_reminder("invalidemail", "Tâche", "2024-06-13")

class TestReportService:
    """Tests du service de rapports"""
    def setup_method(self):
        self.report_service = ReportService()
        # Crée une liste de tâches de test
        self.tasks = [
            Task("T1", priority=Priority.HIGH),
            Task("T2", priority=Priority.LOW),
            Task("T3", priority=Priority.HIGH)
        ]
        self.tasks[0].mark_completed()

    def test_generate_daily_report_fixed_date(self):
        """Test génération rapport avec date fixe"""
        fixed_date = datetime(2024, 6, 13)
        report = self.report_service.generate_daily_report(self.tasks, date=fixed_date)
        assert isinstance(report, dict)
        assert "total_tasks" in report
        assert "completed_tasks" in report
        assert "tasks_by_priority" in report
        assert "tasks_by_status" in report

    @patch('builtins.open', new_callable=mock_open)
    def test_export_tasks_csv(self, mock_file):
        """Test export CSV"""
        filename = "test_export.csv"
        self.report_service.export_tasks_csv(self.tasks, filename)
        mock_file.assert_called_with(filename, "w", newline='', encoding="utf-8")
        handle = mock_file()
        # Vérifie qu'il y a eu écriture (appel à write)
        assert handle.write.call_count > 0 