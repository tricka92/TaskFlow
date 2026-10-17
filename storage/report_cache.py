"""ЛР21, Раздел 3, Сценарий 2: простое кэширование в бинарном файле."""
import pickle
from pathlib import Path

from domain.models import Project
from domain.report import ProjectReport, build_project_report


def get_report(project: Project, cache_path, delay: float = 1.0):
    cache_path = Path(cache_path)

    # 1) Пробуем взять из кэша
    if cache_path.exists():
        try:
            with open(cache_path, "rb") as f:
                cached = pickle.load(f)
            # Кэш годен, только если он про тот же проект и данные не изменились
            # (самая простая проверка: совпадает имя и число задач).
            if (isinstance(cached, ProjectReport)
                    and cached.project_name == project.name
                    and cached.total_tasks == len(project.tasks)):
                return cached, True
        except (pickle.UnpicklingError, EOFError, AttributeError):
            pass

    # 2) В кэше нет -> считаем долго и сохраняем на будущее
    report = build_project_report(project, delay)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "wb") as f:
        pickle.dump(report, f, protocol=pickle.HIGHEST_PROTOCOL)
    return report, False
