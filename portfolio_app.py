from pathlib import Path
import sqlite3

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)
DATABASE = Path(__file__).with_name("portfolio.db")


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                tech TEXT NOT NULL,
                link TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        project_count = connection.execute(
            "SELECT COUNT(*) FROM projects"
        ).fetchone()[0]

        if project_count == 0:
            starter_projects = [
                (
                    "Мій перший сайт",
                    "Невелика сторінка про мене з фото, улюбленими предметами та цілями.",
                    "HTML, CSS",
                    "https://example.com",
                ),
                (
                    "Гра Вгадай число",
                    "Мінігра, де комп'ютер загадує число, а гравець пробує його знайти.",
                    "Python",
                    "",
                ),
                (
                    "Щоденник читача",
                    "Сторінка зі списком книжок, короткими відгуками та оцінками.",
                    "Flask, SQLite",
                    "",
                ),
            ]
            connection.executemany(
                """
                INSERT INTO projects (title, description, tech, link)
                VALUES (?, ?, ?, ?)
                """,
                starter_projects,
            )

        connection.commit()

@app.route("/")
def home():
    with get_connection() as connection:
        projects = connection.execute(
            """
            SELECT id, title, description, tech, link
            FROM projects
            ORDER BY id DESC
            """
        ).fetchall()

    return render_template("index.html", projects=projects)


@app.route("/add", methods=["GET", "POST"])
def add_project():
    form = {
        "title": "",
        "description": "",
        "tech": "",
        "link": "",
    }

    if request.method == "POST":
        form = {
            "title": request.form.get("title", "").strip(),
            "description": request.form.get("description", "").strip(),
            "tech": request.form.get("tech", "").strip(),
            "link": request.form.get("link", "").strip(),
        }

        if not form["title"] or not form["description"] or not form["tech"]:
            return render_template(
                "add_project.html",
                form=form,
                error="Заповни назву, опис і технології.",
            )

        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO projects (title, description, tech, link)
                VALUES (?, ?, ?, ?)
                """,
                (
                    form["title"],
                    form["description"],
                    form["tech"],
                    form["link"],
                ),
            )
            connection.commit()

        return redirect(url_for("home"))

    return render_template("add_project.html", form=form, error="")


@app.route("/delete/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    with get_connection() as connection:
        connection.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        connection.commit()

    return redirect(url_for("home"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)
