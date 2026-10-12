import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "students.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS students (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   email TEXT NOT NULL,
                   course TEXT NOT NULL)"""
        )


@app.route("/")
def index():
    with get_db() as db:
        students = db.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    return render_template("index.html", students=students, edit=None)


@app.route("/add", methods=["POST"])
def add():
    f = request.form
    with get_db() as db:
        db.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
                   (f["name"], f["email"], f["course"]))
    return redirect(url_for("index"))


@app.route("/edit/<int:sid>", methods=["GET", "POST"])
def edit(sid):
    with get_db() as db:
        if request.method == "POST":
            f = request.form
            db.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?",
                       (f["name"], f["email"], f["course"], sid))
            return redirect(url_for("index"))
        student = db.execute("SELECT * FROM students WHERE id=?", (sid,)).fetchone()
        students = db.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    return render_template("index.html", students=students, edit=student)


@app.route("/delete/<int:sid>", methods=["POST"])
def delete(sid):
    with get_db() as db:
        db.execute("DELETE FROM students WHERE id=?", (sid,))
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "ok"}


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
