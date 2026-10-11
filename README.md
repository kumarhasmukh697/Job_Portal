# JobPortal

Modern job board built with **Django** + pure **HTML / CSS / light JS** (shadcn-inspired design, no Tailwind).

## Features

- User registration & login (Job Seeker / Employer roles)
- Job posting, search with filters, detail pages
- Apply to jobs (with resume upload)
- Employer: manage listings & applications
- Dashboard with stats, saved jobs
- Django admin for full control

## Quick start

```bash
cd job_portal
pip install -r requirements.txt
# Optional: set database path in settings if needed
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

### Demo accounts (seeded)

| Username  | Password     | Role     |
|-----------|--------------|----------|
| admin     | admin123     | Admin    |
| employer  | employer123  | Employer |
| seeker    | seeker123    | Seeker   |

## Project layout

```
job_portal/
├── manage.py
├── job_portal/          # settings, urls, wsgi
├── apps/
│   ├── accounts/        # User model, auth views
│   └── jobs/            # Job, Application, Category models & views
├── templates/
├── static/css|js
└── media/
```

## Main URLs

- `/` – Home / featured jobs  
- `/jobs/` – Search & filter  
- `/jobs/<slug>/` – Job detail + apply  
- `/jobs/post/` – Post a job (employer)  
- `/jobs/my/` – Manage listings  
- `/accounts/register/` · `/accounts/login/`  
- `/accounts/dashboard/` · `/accounts/profile/`  
- `/admin/` – Django admin  

## Notes

- SQLite by default (see `settings.py` – currently `/tmp/job_portal.sqlite3` for this environment)
- Static files served in DEBUG mode
- Media uploads: resumes, logos under `media/`
