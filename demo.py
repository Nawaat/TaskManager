#!/usr/bin/env python3
"""
Démonstration du module TaskManager
"""
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority, Status
from src.task_manager.services import EmailService

def main():
    print("=== Démonstration TaskManager ===\n")
    # Créez un gestionnaire
    manager = TaskManager("demo_tasks.json")

    # Ajoutez plusieurs tâches avec différentes priorités
    id1 = manager.add_task("Préparer le rapport", priority=Priority.HIGH)
    id2 = manager.add_task("Envoyer l'email", priority=Priority.MEDIUM)
    id3 = manager.add_task("Faire la veille", priority=Priority.LOW)
    id4 = manager.add_task("Corriger les bugs", priority=Priority.URGENT)

    # Marquez certaines comme terminées
    manager.get_task(id1).mark_completed()
    manager.get_task(id4).mark_completed()

    # Affichez les statistiques
    stats = manager.get_statistics()
    print("Statistiques :")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # Sauvegardez dans un fichier
    manager.save_to_file()
    print("\nTâches sauvegardées dans demo_tasks.json")

    # Rechargez et vérifiez
    manager2 = TaskManager("demo_tasks.json")
    manager2.load_from_file()
    print(f"\nTâches rechargées : {len(manager2.tasks)} tâches trouvées.")
    for t in manager2.tasks:
        print(f"- {t.title} [{t.priority.name}] - Statut: {t.status.name}")

    print("\nDémo terminée avec succès !")

if __name__ == "__main__":
    main() 