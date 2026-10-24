from flask import Flask, abort, render_template, url_for

app = Flask(__name__)

# Страницы-заглушки: адрес -> (название, что здесь появится).
# Когда сделаешь настоящую страницу, добавь для неё отдельный маршрут @app.route("/plan"),
# и он будет использоваться вместо заглушки.
PAGES = {
    "today": ("Сегодня", "План на сегодня: что делать и что сдавать на занятиях."),
    "plan": ("План", "Календарь по дням и пересчёт плана, если что-то не успел."),
    "projects": ("Проекты и задачи", "Таблица проектов (предметов) и задач (лаб) со статусами."),
    "reports": ("Отчёты", "Автоматическое формирование отчётов: Word, Excel, печать."),
    "templates": ("Шаблоны и импорт", "Шаблон семестра, загрузка задач из Excel или CSV."),
    "settings": ("Настройки", "Лимит часов в день, дни без работы, язык интерфейса."),
}


@app.context_processor
def inject_nav():
    """Пункты меню, доступные во всех шаблонах."""
    items = [{"key": "index", "title": "Главная", "url": url_for("index")}]
    for key, (title, _) in PAGES.items():
        items.append({"key": key, "title": title, "url": url_for("page", page=key)})
    return {"nav_items": items}


@app.route("/")
def index():
    return render_template("index.html", active="index")


@app.route("/<page>")
def page(page):
    if page not in PAGES:
        abort(404)
    title, description = PAGES[page]
    return render_template("stub.html", active=page, title=title, description=description)


if __name__ == "__main__":
    app.run(debug=True)