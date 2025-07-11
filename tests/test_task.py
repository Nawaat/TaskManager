import pytest
from datetime import datetime
from src.task_manager.task import Task, Priority, Status

class TestTaskCreation:
    """Tests de création de tâches"""
    def test_create_task_minimal(self):
        """Test création tâche avec paramètres minimaux"""
        t = Task("Titre minimal")
        assert t.title == "Titre minimal"
        assert t.description == ""
        assert t.priority == Priority.MEDIUM
        assert t.status == Status.TODO
        assert isinstance(t.created_at, datetime)
        assert t.completed_at is None
        assert t.project_id is None
        assert t.id is not None

    def test_create_task_complete(self):
        """Test création tâche avec tous les paramètres"""
        t = Task("Titre", "Desc", Priority.HIGH)
        assert t.title == "Titre"
        assert t.description == "Desc"
        assert t.priority == Priority.HIGH
        assert t.status == Status.TODO
        assert isinstance(t.created_at, datetime)
        assert t.completed_at is None
        assert t.project_id is None
        assert t.id is not None

    def test_create_task_empty_title_raises_error(self):
        """Test titre vide lève une erreur"""
        with pytest.raises(ValueError):
            Task("")

    def test_create_task_invalid_priority_raises_error(self):
        """Test priorité invalide lève une erreur"""
        with pytest.raises(ValueError):
            Task("Titre", priority="NOT_A_PRIORITY")

class TestTaskOperations:
    """Tests des opérations sur les tâches"""
    def setup_method(self):
        """Fixture : tâche de test"""
        self.task = Task("Tâche test", "Desc", Priority.LOW)

    def test_mark_completed_changes_status(self):
        """Test marquage comme terminée"""
        self.task.mark_completed()
        assert self.task.status == Status.DONE
        assert isinstance(self.task.completed_at, datetime)

    def test_update_priority_valid(self):
        """Test mise à jour priorité valide"""
        self.task.update_priority(Priority.URGENT)
        assert self.task.priority == Priority.URGENT

    def test_update_priority_invalid_raises_error(self):
        """Test mise à jour priorité invalide lève une erreur"""
        with pytest.raises(ValueError):
            self.task.update_priority("NOT_A_PRIORITY")

    def test_assign_to_project(self):
        """Test assignation à un projet"""
        self.task.assign_to_project("project123")
        assert self.task.project_id == "project123"

class TestTaskSerialization:
    """Tests de sérialisation JSON"""
    def setup_method(self):
        self.task = Task("Titre", "Desc", Priority.HIGH)
        self.task.mark_completed()
        self.task.assign_to_project("proj42")

    def test_to_dict_contains_all_fields(self):
        """Test conversion en dictionnaire"""
        d = self.task.to_dict()
        assert set(d.keys()) == {"id", "title", "description", "priority", "status", "created_at", "completed_at", "project_id"}
        assert isinstance(d["priority"], str)
        assert isinstance(d["status"], str)
        assert isinstance(d["created_at"], str)
        assert isinstance(d["completed_at"], str) or d["completed_at"] is None

    def test_from_dict_recreates_task(self):
        """Test recréation depuis dictionnaire"""
        d = self.task.to_dict()
        t2 = Task.from_dict(d)
        assert t2.id == self.task.id
        assert t2.title == self.task.title
        assert t2.description == self.task.description
        assert t2.priority == self.task.priority
        assert t2.status == self.task.status
        assert t2.created_at == self.task.created_at
        assert t2.completed_at == self.task.completed_at
        assert t2.project_id == self.task.project_id 