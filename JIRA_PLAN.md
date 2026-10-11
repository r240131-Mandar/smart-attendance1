# Smart Attendance System: Jira Plan

**Jira project:** Smart Attendance System (key: `SAS`), template: Scrum

## Problem Statement
Manual attendance in colleges is slow, error-prone and hard to analyse. Students
with low attendance are noticed too late. The Smart Attendance System lets teachers
mark attendance digitally, lets students track their percentage, and automatically
flags students below 75%.

## Epics
| Key | Epic |
|-----|------|
| SAS-1 | Authentication |
| SAS-2 | Attendance Management |
| SAS-3 | Reports and Alerts |
| SAS-4 | DevOps Pipeline |

## User Stories (Product Backlog)
| Key | Epic | Story | Story Points | Priority |
|-----|------|-------|--------------|----------|
| SAS-5 | SAS-1 | As a user, I want to log in with a role (teacher/student) so that I see the right pages. | 3 | High |
| SAS-6 | SAS-2 | As a teacher, I want to mark students present or absent for a subject and date so that records are accurate. | 5 | High |
| SAS-7 | SAS-2 | As a student, I want to view my attendance percentage per subject so that I can track it. | 3 | High |
| SAS-8 | SAS-3 | As a teacher/admin, I want a low-attendance report (below 75%) so that defaulters are identified. | 3 | Medium |
| SAS-9 | SAS-3 | As an admin, I want a daily automated report so that I do not run it manually. | 5 | Medium |
| SAS-10 | SAS-4 | As a developer, I want automated tests so that bugs are caught early. | 3 | High |
| SAS-11 | SAS-4 | As a developer, I want the app containerised with Docker so that it runs anywhere. | 3 | High |
| SAS-12 | SAS-4 | As a developer, I want a Jenkins pipeline so that every push is built and tested. | 5 | High |

## Sprint Plan

### Sprint 1 (Core application), 11 points
| Task | Linked story |
|------|--------------|
| SAS-5 Login page and session handling | SAS-5 |
| SAS-6 Mark attendance form | SAS-6 |
| SAS-7 Student attendance view | SAS-7 |
| Create GitHub repo and connect it to Jira | SAS-12 |

### Sprint 2 (Reports and DevOps), 19 points
| Task | Linked story |
|------|--------------|
| SAS-8 Low-attendance report page | SAS-8 |
| SAS-10 Write pytest tests | SAS-10 |
| SAS-11 Write Dockerfile | SAS-11 |
| SAS-12 Write Jenkinsfile and set up the pipeline | SAS-12 |
| SAS-9 Airflow DAG for daily report | SAS-9 |

## Git Branch and Commit Convention
- Branch: `SAS-6-mark-attendance`
- Commit: `SAS-6: add attendance marking form`
- Merge via pull request into `main`. Jira shows the linked branch, commits and PR on the ticket.

## Screenshots to take for the journal
1. Jira project with epics and backlog
2. Sprint 1 board (To Do / In Progress / Done), then the sprint report
3. Sprint 2 board and burndown chart
4. Jira ticket showing linked GitHub branch, commits and PR
5. GitHub repo with commit history
6. Jenkins pipeline stage view (all green)
7. `docker ps` showing the running container
8. Airflow DAG graph and the generated CSV
