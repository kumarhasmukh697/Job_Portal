# Job Portal - Project Structure

```
job_portal/
├── manage.py
├── requirements.txt
├── README.md
├── job_portal/                 # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/               # User registration, login, profiles
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           # Custom User / Profile
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── migrations/
│   └── jobs/                   # Job listings, applications, search
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py           # Job, Application, Category
│       ├── views.py
│       ├── urls.py
│       ├── forms.py
│       ├── api.py              # External API integration (optional)
│       └── migrations/
├── templates/
│   ├── base.html               # Base layout
│   ├── includes/
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   └── messages.html
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── dashboard.html
│   └── jobs/
│       ├── home.html           # Landing + featured jobs
│       ├── job_list.html       # Search results
│       ├── job_detail.html
│       ├── job_post.html       # Employer post form
│       ├── my_jobs.html        # Employer managed listings
│       └── applications.html   # Applications for a job
├── static/
│   ├── css/
│   │   ├── main.css            # Design system + components
│   │   └── responsive.css
│   ├── js/
│   │   └── main.js             # Light interactivity (modals, tabs, mobile menu)
│   └── images/
└── media/                      # Uploaded resumes / company logos
```

## Roles
- **Job Seeker**: Register → Search → Apply
- **Employer**: Register → Post Jobs → Manage Listings → View Applications
- **Admin**: Django admin for users & jobs

## Tech Notes
- Backend: Django
- Frontend: HTML + custom CSS (shadcn-inspired design tokens) + light vanilla JS
- DB: SQLite (dev) / PostgreSQL (prod)
- No Tailwind, no heavy client-side rendering
