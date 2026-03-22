# Hangarin: Task & To-Do Manager

A simple yet creative web application built with **Django** that helps users organize their daily tasks, manage priorities, add notes, and break down large goals into smaller subtasks.

---

## Live Demo

[alliah2026.pythonanywhere.com](https://alliah2026.pythonanywhere.com)

---

## Features

- **Dashboard** — Overview of total tasks, in progress, completed, pending, category progress bars, and upcoming deadlines
- **Task Management** — Full CRUD (Create, Read, Update, Delete) with status, priority, and category filters
- **Subtasks** — Break tasks into smaller subtasks with their own status tracking
- **Notes** — Attach notes to tasks, filterable by task and date
- **Categories** — Organize tasks by category with progress tracking
- **Priorities** — Manage priority levels (Critical, High, Medium, Low, Optional)
- **Authentication** — Login/Register with username & password or Google OAuth via django-allauth
- **Responsive Design** — Mobile-friendly with hamburger menu
- **Dark/Light Mode** — Toggle between dark and light themes

---

## Technical Requirements

| Technology | Purpose |
|---|---|
| Python 3.10 | Backend language |
| Django 5.2 | Web framework |
| django-allauth | Authentication & Google OAuth |
| django-widget-tweaks | Form field rendering |
| SQLite | Database |
| Bootstrap 5 | Frontend layout & grid |
| Custom CSS | Dark/light theme, cyan-teal gradient design |
| MDB UI Kit | Login page styling |
| Faker | Fake data generation |
| PythonAnywhere | Deployment |

---

## Project Structure
```
Hangarin-Task-To-Do-Manager/
└── hangarin/
    ├── hangarin/          # Project settings, urls, wsgi
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── tasks/             # Main app
    │   ├── models.py      # Task, SubTask, Note, Category, Priority
    │   ├── views.py       # Class-based views with LoginRequiredMixin
    │   ├── urls.py        # URL patterns
    │   ├── admin.py       # Django admin configuration
    │   └── forms.py       # ModelForms for all models
    ├── templates/
    │   ├── account/       # Allauth login template
    │   ├── socialaccount/ # Google OAuth templates
    │   ├── includes/      # Reusable templates (pagination, form)
    │   └── tasks/         # App templates
    ├── static/
    │   ├── css/           # Bootstrap + hangarin.css
    │   ├── js/            # Bootstrap bundle
    │   └── img/           # Logo and profile image
    ├── manage.py
    ├── populate.py        # Faker data population script
    └── requirements.txt
```

---

## Models

### BaseModel (Abstract)
- `created_at` — DateTimeField (auto)
- `updated_at` — DateTimeField (auto)

### Category
- `name` — CharField

### Priority
- `name` — CharField

### Task (inherits BaseModel)
- `title` — CharField
- `description` — TextField
- `deadline` — DateTimeField
- `status` — CharField (Pending / In Progress / Completed)
- `category` — ForeignKey → Category
- `priority` — ForeignKey → Priority

### Note (inherits BaseModel)
- `task` — ForeignKey → Task
- `content` — TextField

### SubTask (inherits BaseModel)
- `parent_task` — ForeignKey → Task
- `title` — CharField
- `status` — CharField (Pending / In Progress / Completed)

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/alliah2025/Hangarin-Task-To-Do-Manager.git
cd Hangarin-Task-To-Do-Manager
```

### 2. Create and activate virtual environment
```bash
python -m venv HangarinEnv
# Windows
HangarinEnv\Scripts\activate
# Mac/Linux
source HangarinEnv/bin/activate
```

### 3. Install dependencies
```bash
cd hangarin
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create superuser
```bash
python manage.py createsuperuser
```

### 6. Populate with fake data
```bash
python populate.py
```

### 7. Run the server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## Authentication Setup (Google OAuth)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create an OAuth 2.0 Client ID (Web application)
3. Add authorized redirect URIs:
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
   - `https://alliah2026.pythonanywhere.com/accounts/google/login/callback/`
4. In Django Admin → Social Applications → Add Google app with your Client ID and Secret
5. Assign the correct site to the Social Application

---

## Deployment (PythonAnywhere)
```bash
git clone https://github.com/alliah2025/Hangarin-Task-To-Do-Manager.git
source ~/.virtualenvs/hangarin/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## Author

**Alliah E. Mahilum** &nbsp; [![GitHub](https://img.shields.io/badge/GitHub-alliah2025-181717?style=flat&logo=github)](https://github.com/alliah2025)

---

## License

This project is for educational purposes.