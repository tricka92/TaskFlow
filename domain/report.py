"""Отчёт по проекту. Строить его "долго" - поэтому нужен кэш (ЛР21, сценарий 2)."""
import time
from dataclasses import dataclass
from datetime import datetime

from domain.models import Project, Status


@dataclass
class ProjectReport:
    project_name: str
    total_tasks: int
    done_tasks: int
    tasks_by_status: dict
    generated_at: datetime

    @property
    def percent_done(self) -> float:
        return 100 * self.done_tasks / self.total_tasks if self.total_tasks else 0.0


def build_project_report(project: Project, delay: float = 1.0) -> ProjectReport:
    time.sleep(delay)
    by_status = {s.value: 0 for s in Status}
    for task in project.tasks:
        by_status[task.status.value] += 1
    return ProjectReport(
        project_name=project.name,
        total_tasks=len(project.tasks),
        done_tasks=by_status[Status.DONE.value],
        tasks_by_status=by_status,
        generated_at=datetime.now(),
    )
