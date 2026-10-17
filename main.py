"""Точка входа. Пока только собирает демо-данные, чтобы было что сохранять."""
from domain.models import Priority, Project, Task, Workspace


def build_demo_workspace() -> Workspace:
    ws = Workspace()
    p = Project(id=1, name="Курсовой проект")
    p.add_task(Task(1, "Разобрать задание", priority=Priority.HIGH))
    p.add_task(Task(2, "Нарисовать диаграмму классов"))
    ws.add_project(p)
    return ws


if __name__ == "__main__":
    ws = build_demo_workspace()
    for project in ws.projects.values():
        print(project.name, "-", len(project.tasks), "задачи")

