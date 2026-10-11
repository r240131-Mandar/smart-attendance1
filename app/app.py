import os
import sqlite3
from datetime import date

from flask import Flask, g, redirect, render_template, request, session, url_for, flash

THRESHOLD = 75.0


def create_app(db_path=None):
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    app.config["DB_PATH"] = db_path or os.environ.get(
        "DB_PATH", os.path.join(os.path.dirname(__file__), "attendance.db")
    )

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DB_PATH"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        init_db(get_db())

    # ---------- helpers ----------
    def percentage_rows(db, student_id=None):
        """Attendance percentage per student per subject."""
        query = """
            SELECT u.id AS student_id, u.name AS student, a.subject,
                   SUM(a.present) AS attended, COUNT(*) AS total,
                   ROUND(100.0 * SUM(a.present) / COUNT(*), 1) AS percent
            FROM attendance a JOIN users u ON u.id = a.student_id
        """
        params = ()
        if student_id is not None:
            query += " WHERE u.id = ?"
            params = (student_id,)
        query += " GROUP BY u.id, a.subject ORDER BY u.name, a.subject"
        return db.execute(query, params).fetchall()

    # ---------- routes ----------
    @app.route("/")
    def index():
        if "user_id" not in session:
            return redirect(url_for("login"))
        if session["role"] == "teacher":
            return redirect(url_for("mark"))
        return redirect(url_for("my_attendance"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = get_db().execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (request.form["username"], request.form["password"]),
            ).fetchone()
            if user:
                session.update(user_id=user["id"], role=user["role"], name=user["name"])
                return redirect(url_for("index"))
            flash("Invalid username or password")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/mark", methods=["GET", "POST"])
    def mark():
        if session.get("role") != "teacher":
            return redirect(url_for("login"))
        db = get_db()
        students = db.execute(
            "SELECT id, name FROM users WHERE role = 'student' ORDER BY name"
        ).fetchall()
        if request.method == "POST":
            subject = request.form["subject"].strip()
            day = request.form.get("date") or date.today().isoformat()
            if not subject:
                flash("Subject is required")
            else:
                present_ids = set(request.form.getlist("present"))
                db.execute(
                    "DELETE FROM attendance WHERE subject = ? AND date = ?", (subject, day)
                )
                for s in students:
                    db.execute(
                        "INSERT INTO attendance (student_id, subject, date, present) VALUES (?,?,?,?)",
                        (s["id"], subject, day, 1 if str(s["id"]) in present_ids else 0),
                    )
                db.commit()
                flash(f"Attendance saved for {subject} on {day}")
            return redirect(url_for("mark"))
        return render_template("mark.html", students=students, today=date.today().isoformat())

    @app.route("/my-attendance")
    def my_attendance():
        if session.get("role") != "student":
            return redirect(url_for("login"))
        rows = percentage_rows(get_db(), session["user_id"])
        return render_template("my_attendance.html", rows=rows, threshold=THRESHOLD)

    @app.route("/report")
    def report():
        if session.get("role") != "teacher":
            return redirect(url_for("login"))
        rows = [r for r in percentage_rows(get_db()) if r["percent"] < THRESHOLD]
        return render_template("report.html", rows=rows, threshold=THRESHOLD)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


def init_db(db):
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('teacher','student'))
        );
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES users(id),
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            present INTEGER NOT NULL CHECK (present IN (0,1))
        );
        """
    )
    if db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        seed = [
            ("teacher1", "teach123", "Prof. Sharma", "teacher"),
            ("amit", "pass123", "Amit Patil", "student"),
            ("neha", "pass123", "Neha Joshi", "student"),
            ("rahul", "pass123", "Rahul Deshmukh", "student"),
        ]
        db.executemany(
            "INSERT INTO users (username, password, name, role) VALUES (?,?,?,?)", seed
        )
    db.commit()


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
