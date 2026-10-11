# Smart Attendance System

ASDD mini project (Experiment 10). Flow: **Jira → GitHub → Jenkins → Docker → Airflow**.

Teachers mark attendance, students see their percentage per subject, and anyone
below 75% is flagged in a low-attendance report (also generated daily by Airflow).

## Features
- Role-based login (teacher / student)
- Teacher: mark present/absent per subject and date
- Student: view attendance percentage per subject
- Teacher: low-attendance report (below 75%)
- Daily automated CSV report via Airflow

## Demo accounts
| Role | Username | Password |
|------|----------|----------|
| Teacher | teacher1 | teach123 |
| Student | amit / neha / rahul | pass123 |

## Run locally
```bash
pip install -r requirements.txt
python app/app.py          # http://localhost:5000
pytest -v                  # run tests
```

## Run with Docker
```bash
docker build -t smart-attendance .
docker run -d -p 5000:5000 -v attendance-data:/data smart-attendance
```

## CI/CD (Jenkins)
The `Jenkinsfile` runs: Checkout → Install Dependencies → Test → Docker Build → Docker Deploy.
Create a Pipeline job in Jenkins ("Pipeline script from SCM"), point it at this repo,
and enable the GitHub webhook / poll SCM so each push triggers a build.
The Jenkins user must be able to run `docker` (add it to the `docker` group).

## Airflow
Copy `dags/low_attendance_dag.py` into your Airflow `dags/` folder, set `DB_PATH`
to the app's `attendance.db` and `REPORT_DIR` to an output folder, then enable the
`low_attendance_daily_report` DAG. It writes `low_attendance_<date>.csv` daily.

## Agile planning
See `JIRA_PLAN.md` for the problem statement, epics, user stories and sprint plan.
Branches use `SAS-<n>-short-name`, and commits start with the ticket ID, e.g. `SAS-6: add attendance form`.

## Structure
```
smart-attendance/
├── app/            Flask app + templates
├── tests/          pytest tests
├── dags/           Airflow DAG
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── JIRA_PLAN.md
└── README.md
Attendance marking form: teachers mark present/absent
```
