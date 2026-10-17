"""ЛР21 "Сериализация": показываем, КАК решается каждое задание.
Запуск:  python lab21_demo.py
"""
import os
import pickle
import time

from main import build_demo_workspace
from storage.app_settings import AppSettings, load_settings, save_settings
from storage.pickle_storage import load_workspace, save_workspace
from storage.report_cache import get_report
from utils.bintree_codec import TreeNode, deserialize, load_tree, save_tree, serialize

DATA = "data"


def title(text):
    print("\n" + "=" * 60 + "\n" + text + "\n" + "=" * 60)


# ---------------------------------------------------------------- Раздел 1
title("РАЗДЕЛ 1 (Python): pickle, список + словарь")
ws = build_demo_workspace()
save_workspace(ws, f"{DATA}/workspace.pkl")
print("1) Сохранили. Размер файла:", os.path.getsize(f"{DATA}/workspace.pkl"), "байт")
with open(f"{DATA}/workspace.pkl", "rb") as f:
    print("2) Первые байты файла :", f.read(16))
restored = load_workspace(f"{DATA}/workspace.pkl")
print("3) Загрузили обратно. Проекты:", list(restored.projects))
print("   Задачи 1-го проекта:", [t.title for t in restored.projects[1].tasks])
print("4) Копия равна оригиналу?", restored == ws)
print("5) Это ТОТ ЖЕ объект в памяти?", restored is ws)

# ------------------------------------------------- Раздел 2, задание 3
title("РАЗДЕЛ 2, задание 3: своё бинарное дерево")

tree = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
data = serialize(tree)
print("Байты (hex):", data.hex(" "))
print("Размер:", len(data), "байт = 3 заголовок + 5 узлов*5 + 6 пустых*1")
print("Восстановили, дерево совпадает?", deserialize(data) == tree)
save_tree(tree, f"{DATA}/tree.bin")
print("Через файл тоже работает?", load_tree(f"{DATA}/tree.bin") == tree)
print("Пустое дерево:", serialize(None).hex(" "), "->", deserialize(serialize(None)))
try:
    deserialize(data[:-3])          # специально "обрезаем" данные
except ValueError as e:
    print("Обрезанные данные ловим ошибкой:", e)

# ----------------------------------------------------- Раздел 3, сценарий 1
title("РАЗДЕЛ 3, сценарий 1: настройки при закрытии/запуске")


class FakeApp:
    """Заменяет настоящее окно: у него есть запуск и закрытие."""

    def start(self):
        self.settings = load_settings(f"{DATA}/settings.json")   # ПРИ ЗАПУСКЕ
        print("   запуск, настройки:", self.settings)

    def close(self):
        save_settings(self.settings, f"{DATA}/settings.json")    # ПРИ ЗАКРЫТИИ
        print("   закрытие, настройки сохранены")


if os.path.exists(f"{DATA}/settings.json"):
    os.remove(f"{DATA}/settings.json")
print("Первый запуск (файла нет):")
app = FakeApp(); app.start()
app.settings.window_width, app.settings.last_project_id = 1280, 1
app.close()
print("Второй запуск (файл есть):")
FakeApp().start()

# ----------------------------------------------------- Раздел 3, сценарий 2
title("РАЗДЕЛ 3, сценарий 2: кэш отчёта")
cache = f"{DATA}/report_cache.pkl"
if os.path.exists(cache):
    os.remove(cache)
project = ws.projects[1]
for n in (1, 2):
    t = time.perf_counter()
    report, from_cache = get_report(project, cache)
    print(f"Запуск {n}: {time.perf_counter() - t:.3f} сек, из кэша: {from_cache}, "
          f"выполнено {report.percent_done:.0f}%")

