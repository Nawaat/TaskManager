# TaskManager

## Arborescence réelle du projet :

TaskManager/
├── src/
│   └── task_manager/
│       ├── __init__.py
│       ├── manager.py            # Classe TaskManager pour gérer projets/tâches
│       ├── task.py               # Entité Task (priorité, statut, etc.)
│       └── services.py           # Services externes (email, rapport)
├── tests/
│   ├── __init__.py
│   ├── test_manager.py           # Tests unitaires du gestionnaire
│   ├── test_task.py              # Tests unitaires de l'entité Task
│   ├── test_services.py          # Tests d'intégration des services externes
│   └── fixtures/
│       └── sample_data.json      # Exemple de données pour les tests
├── .github/workflows/
│   └── ci.yml                    # Workflow GitHub Actions pour l’intégration continue
├── requirements.txt              # Dépendances (ex. pytest, coverage)
├── pyproject.toml                # Configuration de black, coverage, etc.
├── README.md                     # Description du projet
└── .gitignore                    # 

## Installation des dépendances

```bash
pip install -r requirements.txt
```

## Lancer les tests unitaires et d'intégration

Assurez-vous d'être à la racine du projet, puis lancez :

```bash
pytest
```

Tous les tests unitaires et d'intégration seront exécutés automatiquement.

## Structure des tests
- `tests/test_task.py` : tests de l'entité Task
- `tests/test_manager.py` : tests du gestionnaire TaskManager (avec mocks)
- `tests/test_services.py` : tests d'intégration des services externes (EmailService, ReportService, mocks)
- `tests/test_models.py` : tests des autres entités
- `tests/test_integration.py` : tests d'intégration du flux complet

## Couverture des tests
- Les services externes (email, rapport) sont testés avec des mocks pour simuler les dépendances et éviter les effets de bord.
- Le projet est conçu pour être facilement testable et extensible.
- Vous pouvez générer un rapport de couverture avec :

```bash
pytest --cov=src
```

## Notes
- Les services externes (email, rapport) sont simulés et peuvent être mockés dans les tests.
- Le projet est conçu pour être facilement testable et extensible. 