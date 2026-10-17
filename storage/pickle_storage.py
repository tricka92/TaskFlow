"""ЛР21, Раздел 1 (Python): двоичная сериализация через модуль pickle.

Что сохраняем: объект Workspace целиком. Внутри него:
  - словарь  (projects: {id проекта -> Project})
  - списки   (у каждого Project есть список tasks)
Это ровно то, что просит задание: "структура данных со списком и словарём".
"""
import pickle
from pathlib import Path

from domain.models import Workspace


def save_workspace(ws: Workspace, path) -> None:
    # СЕРИАЛИЗАЦИЯ: объект в памяти -> байты в файле.
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)  # создаём папку, если её нет
    with open(path, "wb") as f:
        pickle.dump(ws, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_workspace(path) -> Workspace:
    #ДЕСЕРИАЛИЗАЦИЯ: байты из файла -> снова объект Workspace.

    path = Path(path)
    if not path.exists():
        return Workspace()
    with open(path, "rb") as f:
        return pickle.load(f)
