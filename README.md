# ResearchDoc

A SaaS research management platform built with Django 5.1.

## Live Deployment

**Deployed URL:** https://web-production-ea24f.up.railway.app

**Admin account:**
- Username: admin1
- Password: Tfr20020528

**Test user account:**
- Username: Frank_Teng
- Password: Tfr20020528!

---

## Features

- **Project Management** — Create and manage research projects with CRUD operations
- **Resource Library** — Upload PDFs or save URL links per project
- **Rich Text Summaries** — Tiptap-powered editor with inline citation support
- **Comparison Tables** — Visual inline-editable comparison tables
- **Full-Text Search** — Search across projects, resources, and summaries
- **AI Generation** — Claude-powered summary and comparison generation (Anthropic API)
- **Role-Based Access** — Users see only their own data; admin manages all via Django Admin

---

## Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
# 1. Navigate into the project
cd researchdoc

# 2. Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY (optional — AI features disabled without it)

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser (for admin panel)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

**Default admin credentials** (if created via setup script):
- Username: `admin`  Password: `admin123`

---

## Environment Variables (`.env`)

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | `True` for development | Yes |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | Yes |
| `ANTHROPIC_API_KEY` | Anthropic API key for AI features | No |

---

## Project Structure

```
researchdoc/
├── config/          Django project config (settings, urls, wsgi)
├── accounts/        User registration, login, logout, subscriptions
├── projects/        ResearchProject CRUD
├── resources/       Resource CRUD (PDF upload + URL)
├── summaries/       Summary editor (Tiptap) + AI generation
├── comparisons/     Comparison table editor + AI generation
├── search_app/      Full-text search
├── templates/       All HTML templates
├── static/          CSS, JS, images
├── media/           Uploaded files (PDF)
├── requirements.txt
├── .env.example
└── manage.py
```

---

## Deployment (Linux Server)

### 1. System packages

```bash
sudo apt update && sudo apt install python3.11 python3.11-venv python3-pip nginx -y
```

### 2. Clone and set up

```bash
git clone <repo-url> /var/www/researchdoc
cd /var/www/researchdoc
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Set SECRET_KEY, DEBUG=False, ALLOWED_HOSTS=yourdomain.com, ANTHROPIC_API_KEY
nano .env
```

### 4. Prepare static files and database

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 5. Gunicorn service (`/etc/systemd/system/researchdoc.service`)

```ini
[Unit]
Description=ResearchDoc Gunicorn
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/researchdoc
ExecStart=/var/www/researchdoc/.venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable researchdoc && sudo systemctl start researchdoc
```

### 6. Nginx config (`/etc/nginx/sites-available/researchdoc`)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /var/www/researchdoc/staticfiles/;
    }

    location /media/ {
        alias /var/www/researchdoc/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/researchdoc /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Django 5.1.4 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | Bootstrap 5.3 |
| Rich Text | Tiptap 2 |
| Static Files | Whitenoise |
| AI | OpenAI (gpt-5.4-mini) |
| Server | Gunicorn + Nginx |

---

## GenAI Declaration

This project was developed with the assistance of Generative AI tools:
- **Claude Code** (Anthropic) — Used throughout development for code generation, debugging, and deployment assistance.
- All code has been reviewed and tested by the developer.
