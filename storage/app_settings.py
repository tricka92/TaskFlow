"""ЛР21, Раздел 3, Сценарий 1: настройки приложения
"""
import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path


@dataclass
class AppSettings:
    window_width: int = 1289          # значения по умолчанию =
    window_height: int = 700          # первый запуск программы
    last_project_id: int | None = None  # последний открытый проект
    language: str = "ru"


def save_settings(settings: AppSettings, path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        # asdict превращает dataclass в обычный словарь, а json.dump -> в текст.
        json.dump(asdict(settings), f, ensure_ascii=False, indent=2)


def load_settings(path) -> AppSettings:
    """Всегда возвращает рабочие настройки, даже если файл потерян или испорчен."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return AppSettings()          # нет файла / файл испорчен -> по умолчанию
    if not isinstance(data, dict):
        return AppSettings()
    # Берём только те ключи, которые наш класс знает. Так файл от старой или
    # новой версии программы не ломает загрузку
    known = {f.name for f in fields(AppSettings)}
    return AppSettings(**{k: v for k, v in data.items() if k in known})
