"""Airflow DAG: daily low-attendance report.

Reads the attendance SQLite database, finds students below 75% in any subject
and writes the result to a dated CSV file.

Setup: copy this file into your Airflow `dags/` folder and set the environment
variables DB_PATH (path to attendance.db) and REPORT_DIR (output folder).
"""
import csv
import os
import sqlite3
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

DB_PATH = os.environ.get("DB_PATH", "/data/attendance.db")
REPORT_DIR = os.environ.get("REPORT_DIR", "/tmp/attendance_reports")
THRESHOLD = 75.0


def fetch_low_attendance():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT u.name AS student, a.subject,
               SUM(a.present) AS attended, COUNT(*) AS total,
               ROUND(100.0 * SUM(a.present) / COUNT(*), 1) AS percent
        FROM attendance a JOIN users u ON u.id = a.student_id
        GROUP BY u.id, a.subject
        HAVING percent < ?
        ORDER BY u.name, a.subject
        """,
        (THRESHOLD,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def write_report(ds=None, **_):
    os.makedirs(REPORT_DIR, exist_ok=True)
    rows = fetch_low_attendance()
    day = ds or datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(REPORT_DIR, f"low_attendance_{day}.csv")
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["student", "subject", "attended", "total", "percent"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} low-attendance rows to {path}")


with DAG(
    dag_id="low_attendance_daily_report",
    description="Daily report of students below 75% attendance",
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=5)},
    tags=["asdd", "attendance"],
) as dag:
    PythonOperator(task_id="generate_low_attendance_report", python_callable=write_report)
