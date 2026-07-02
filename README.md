# AI Solutions Django Website

AI Solutions is a Django web application for a technology services company. The
project includes a public marketing website, contact enquiry form, AI chatbot
widget, Django admin area, and a custom staff CRM for managing website content
and customer queries.

## Main Features

- Public website pages for services, highlights, feedback, articles, events,
  gallery photos and contact enquiries.
- Contact Us form for visitors to submit project or support queries.
- Gemini-powered AI assistant widget for answering visitor questions.
- Custom staff CRM for managing public website content.
- Staff query management for reading, marking and deleting contact enquiries.
- Django admin fallback for database management.
- SQLite database for local development and assignment demonstration.

## Technology Stack

| Area       | Technology                              |
| ---------- | --------------------------------------- |
| Backend    | Python, Django 5.2                      |
| Database   | SQLite                                  |
| Frontend   | Django templates, HTML, CSS, JavaScript |
| Images     | Pillow                                  |
| AI chatbot | Google Gemini API                       |
| Charts     | Chart.js CDN                            |

## Project Structure

```text
ai_solution/
  settings.py
  urls.py
  wsgi.py
core/
  admin.py
  chatbot.py
  forms.py
  models.py
  urls.py
  views.py
  management/commands/seed_demo_data.py
  static/core/css/main.css
  static/core/js/main.js
  templates/core/
media/
db.sqlite3
manage.py
README.md
requirements.txt
Procfile
runtime.txt
```

## Setup

These commands assume you are in the project root, the folder that contains
`manage.py`.

### 1. Create a virtual environment

Windows:

```cmd
python -m venv .venv
```

### 2. Install dependencies

```cmd
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Apply migrations

```cmd
.\.venv\Scripts\python.exe manage.py migrate
```

### 4. Create a staff/admin user

```cmd
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Use this account for the staff CRM and Django admin.

### 5. Add demo content

```cmd
.\.venv\Scripts\python.exe manage.py seed_demo_data
```

This command creates sample solutions, highlights, feedback, articles and
events.

## Gemini Chatbot Setup

The chatbot works best when a Gemini API key is provided through an environment
variable. Do not paste the key into the code before submitting the assignment.

Command Prompt:

```cmd
set GEMINI_API_KEY=your-api-key-here
set GEMINI_MODEL=gemini-2.5-flash-lite
.\.venv\Scripts\python.exe manage.py runserver
```

PowerShell:

```powershell
$env:GEMINI_API_KEY="your-api-key-here"
$env:GEMINI_MODEL="gemini-2.5-flash-lite"
.\.venv\Scripts\python.exe manage.py runserver
```

If `GEMINI_API_KEY` is not set, the chatbot will show a simple fallback message
instead of using Gemini.

## Run the Project

```cmd
.\.venv\Scripts\python.exe manage.py runserver
```

Open the public site:

```text
http://127.0.0.1:8000/
```

Staff CRM:

```text
http://127.0.0.1:8000/staff/login/
```

Django admin:

```text
http://127.0.0.1:8000/django-admin/
```

## Useful Development Commands

Check the Django project:

```cmd
.\.venv\Scripts\python.exe manage.py check
```

Create migrations after model changes:

```cmd
.\.venv\Scripts\python.exe manage.py makemigrations
```

Apply migrations:

```cmd
.\.venv\Scripts\python.exe manage.py migrate
```

Reset a user password:

```cmd
.\.venv\Scripts\python.exe manage.py changepassword username
```

## URL Map

### Public Pages

| URL                      | Page                        |
| ------------------------ | --------------------------- |
| `/`                      | Homepage                    |
| `/solutions/`            | Services and solutions      |
| `/case-studies/`         | Highlights and case studies |
| `/feedback/`             | Customer feedback           |
| `/knowledge-hub/`        | Articles                    |
| `/knowledge-hub/<slug>/` | Article detail              |
| `/gallery/`              | Events and gallery          |
| `/contact/`              | Contact form                |
| `/api/chat/`             | Chatbot API endpoint        |

### Staff CRM

| URL                  | Purpose                  |
| -------------------- | ------------------------ |
| `/staff/login/`      | Staff login              |
| `/staff/logout/`     | Staff logout             |
| `/staff/dashboard/`  | Staff dashboard          |
| `/staff/queries/`    | Manage contact enquiries |
| `/staff/solutions/`  | Manage services          |
| `/staff/highlights/` | Manage highlights        |
| `/staff/feedback/`   | Manage feedback          |
| `/staff/articles/`   | Manage articles          |
| `/staff/photos/`     | Manage gallery photos    |
| `/staff/events/`     | Manage events            |
| `/django-admin/`     | Django admin             |

## Chatbot Behaviour

The chatbot is implemented in `core/chatbot.py` and is called by the
`/api/chat/` endpoint in `core/views.py`. Visitor messages and bot replies are
stored in the `ChatMessage` model so recent session history can be sent back to
Gemini for conversational context.

The assistant is designed to answer questions about:

- AI Solutions services.
- Website AI assistants for small businesses.
- Business websites and chatbot enquiry handoff.
- Staff help desks, HR and IT support tools.
- Request workflows, reporting dashboards and integrations.

The assistant should not claim it can directly access a visitor's website,
systems, files, orders or private data.

## Preparing a Zip Submission

Do not include generated or environment-specific folders in the zip.

Exclude:

```text
.venv/
__pycache__/
*.pyc
staticfiles/
.env
```

Usually include:

```text
ai_solution/
core/
media/
db.sqlite3
manage.py
Procfile
requirements.txt
README.md
runtime.txt
```

Keep `db.sqlite3` if the marker should see the existing demo data and any
created staff account. Remove it only if the marker is expected to run
migrations and seed data from scratch.

## Notes

- This project is configured for local development with `DEBUG = True`.
- SQLite is used for convenience.
- The Gemini API key should be supplied from the terminal and should not be
  committed into project files.
- Public visitors do not need accounts; staff users manage content after login.
