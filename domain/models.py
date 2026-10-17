"""Доменные модели системы."""
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: Status = Status.TODO
    priority: Priority = Priority.MEDIUM
    deadline: date | None = None
    assignee: str = ""


@dataclass
class Project:
    id: int
    name: str
    tasks: list[Task] = field(default_factory=list)  # <- СПИСОК

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


@dataclass
class Workspace:
    """Корневой объект: всё, что система хранит о пользователе."""
    projects: dict[int, Project] = field(default_factory=dict)  # <- СЛОВАРЬ

    def add_project(self, project: Project) -> None:
        self.projects[project.id] = project
