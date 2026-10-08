# TaskFlow - Modern Django CRUD with SQLite

Responsive task manager with account registration, login/logout, per-user data isolation, Create/Read/Update/Delete, search, status filtering, pagination, dashboard counts, Django admin, and a Django REST Framework API.

## Run locally (Python 3.10+)

```text
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/signup/ and create an account. Sign in. In another activated terminal, optionally run `python manage.py seed_demo YOUR_USERNAME` to add fictional data. SQLite db.sqlite3 is created by migrate. The ZIP includes migrations; no separate database installation is needed.

## CRUD routes

| Operation | Web route | API route |
|---|---|---|
| Create | /tasks/new/ | POST /api/tasks/ |
| Read | / and /tasks/ID/ | GET /api/tasks/ and /api/tasks/ID/ |
| Update | /tasks/ID/edit/ | PUT or PATCH /api/tasks/ID/ |
| Delete | /tasks/ID/delete/ (POST confirms) | DELETE /api/tasks/ID/ |

Sign in through the web interface before opening /api/tasks/ in the same browser. DRF uses the session and enforces CSRF on unsafe requests. Use its browsable API forms; external clients must send the session cookie and CSRF token. API pagination uses ?page=2, search uses ?search=keyword, status uses ?status=done, sorting uses ?ordering=due_date. Dashboard metrics count all your tasks, regardless of active filters.

## Database

Task has id, owner foreign key, title, description, status, priority, optional due_date, created_at and updated_at. An owner/status index supports common filters. Django creates auth/session tables too. Owner is assigned from the session and is not editable through the API. Deleting a user cascades to their tasks. Ordinary users see only their own data; trusted superusers can manage all tasks in admin.

```text
python manage.py createsuperuser
python manage.py test
python manage.py check
```

Open /admin/ with the superuser account. Never upload your local db.sqlite3 or real credentials.

## GitHub

Create an empty repository named django-taskflow. Extract this ZIP and upload the files inside django-taskflow so manage.py and README.md are at the root. The PDF guide is under docs/.

```sh
git init
git add .
git commit -m "Add Django task manager with CRUD and REST API"
git branch -M main
git remote add origin https://github.com/praveenkumarmandula/django-taskflow.git
git push -u origin main
```

## Design / next steps

Django ORM and ModelForms handle persistence and validation. Class-based views provide CRUD. Querysets constrain every object lookup to its owner. HTML deletion requires a confirmation POST. CSRF protection is enabled. REST permissions require authentication.

Local development defaults include DEBUG enabled and a development secret. Before deployment set DJANGO_DEBUG=0, DJANGO_SECRET_KEY to a secret value, and DJANGO_ALLOWED_HOSTS to your hostnames; configure HTTPS, secure cookies, static file serving and a production WSGI server. This archive is a local portfolio project, not a production deployment. Extend it with PostgreSQL, project teams, reminders and CI. Understand and customize the code before discussing it in interviews.

References: https://docs.djangoproject.com/en/5.2/ and https://www.django-rest-framework.org/api-guide/viewsets/
