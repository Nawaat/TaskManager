from unittest.mock import patch, mock_open
import json
from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status

class TestTaskManagerBasics:
    """Tests basiques du gestionnaire"""
    def setup_method(self):
        """Fixture : gestionnaire de test"""
        self.manager = TaskManager("test_tasks.json")

    def test_add_task_returns_id(self):
        """Test ajout tâche retourne un ID"""
        task_id = self.manager.add_task("Titre", "Desc", Priority.HIGH)
        assert isinstance(task_id, str)
        assert any(t.id == task_id for t in self.manager.tasks)

    def test_get_task_existing(self):
        """Test récupération tâche existante"""
        task_id = self.manager.add_task("Titre", "Desc", Priority.LOW)
        task = self.manager.get_task(task_id)
        assert task is not None
        assert task.title == "Titre"
        assert task.priority == Priority.LOW

    def test_get_task_nonexistent_returns_none(self):
        """Test récupération tâche inexistante"""
        task = self.manager.get_task("id_inexistant")
        assert task is None

class TestTaskManagerFiltering:
    """Tests de filtrage des tâches"""
    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")
        t1 = self.manager.add_task("T1", priority=Priority.HIGH)
        t2 = self.manager.add_task("T2", priority=Priority.LOW)
        t3 = self.manager.add_task("T3", priority=Priority.HIGH)
        t4 = self.manager.add_task("T4", priority=Priority.MEDIUM)
        # Marquer une tâche comme terminée
        task3 = self.manager.get_task(t3)
        if task3:
            task3.mark_completed()

    def test_get_tasks_by_status(self):
        """Test filtrage par statut"""
        todos = self.manager.get_tasks_by_status(Status.TODO)
        assert all(t.status == Status.TODO for t in todos)
        assert len(todos) == 3

    def test_get_tasks_by_priority(self):
        """Test filtrage par priorité"""
        highs = self.manager.get_tasks_by_priority(Priority.HIGH)
        assert all(t.priority == Priority.HIGH for t in highs)
        assert len(highs) == 2

class TestTaskManagerPersistence:
    """Tests de sauvegarde/chargement avec mocks"""
    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")
        self.manager.add_task("T1", priority=Priority.HIGH)
        self.manager.add_task("T2", priority=Priority.LOW)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file_success(self, mock_json_dump, mock_file):
        """Test sauvegarde réussie"""
        manager = TaskManager("test_tasks.json")
        manager.add_task("T1", priority=Priority.HIGH)
        manager.add_task("T2", priority=Priority.LOW)
        manager.save_to_file()
        mock_file.assert_called_with("test_tasks.json", "w", encoding="utf-8")
        assert mock_json_dump.called

    @patch("os.path.exists", return_value=True)
    @patch("json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_from_file_success(self, mock_file, mock_json_load, mock_exists):
        """Test chargement réussi"""
        manager = TaskManager("test_tasks.json")
        # Simuler un dictionnaire JSON valide
        tdict = {
            "id": "123",
            "title": "Titre",
            "description": "",
            "priority": "HIGH",
            "status": "TODO",
            "created_at": "2024-06-13T12:00:00",
            "completed_at": None,
            "project_id": None
        }
        mock_json_load.return_value = [tdict]

        manager.load_from_file()

        assert len(manager.tasks) == 1
        task = manager.tasks[0]
        assert task.title == "Titre"
        assert task.priority == Priority.HIGH
        assert task.status == Status.TODO


    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_from_nonexistent_file(self, mock_file):
        """Test chargement fichier inexistant"""
        manager = TaskManager("test_tasks.json")
        manager.tasks = [Task("T", priority=Priority.LOW)]
        manager.load_from_file()
        assert manager.tasks == []

def test_delete_task_not_found():
    manager = TaskManager()
    assert manager.delete_task("id_inexistant") is False

def test_save_to_file_exception(monkeypatch):
    manager = TaskManager()
    def raise_exc(*a, **kw): raise IOError("Erreur écriture")
    monkeypatch.setattr("builtins.open", lambda *a, **kw: (_ for _ in ()).throw(IOError("Erreur écriture")))
    manager.save_to_file()  # Doit juste afficher une erreur, pas lever

def test_load_from_file_exception(monkeypatch):
    manager = TaskManager()
    def raise_exc(*a, **kw): raise IOError("Erreur lecture")
    monkeypatch.setattr("builtins.open", lambda *a, **kw: (_ for _ in ()).throw(IOError("Erreur lecture")))
    manager.load_from_file()  # Doit juste afficher une erreur, pas lever

def test_get_statistics_empty():
    manager = TaskManager()
    stats = manager.get_statistics()
    assert stats["total_tasks"] == 0
    assert stats["completed_tasks"] == 0
