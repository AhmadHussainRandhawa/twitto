<div align="center">

# 🐦 Twitto

### A microblogging platform, built from scratch with Django.

Post. Edit. Delete. Attach an image. Search the feed. No algorithm deciding what you see, no ads, no data broker in the middle — just a clean Django app doing exactly what it says.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1.6-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

[**Live Demo**](https://ahmadhussain.pythonanywhere.com) · [Report a Bug](https://github.com/AhmadHussainRandhawa/twitto/issues) · [Request a Feature](https://github.com/AhmadHussainRandhawa/twitto/issues)

</div>

<br>

## 🎬 See it in action

https://github.com/user-attachments/assets/2dfd4b7f-e406-47f5-86d8-92826321775c

A live session: a user registers, logs in, and composes a tweet with an attached image. They edit it, watch the feed update, search for it by keyword, then delete it — and it's gone from the feed instantly. Every write in that flow is checked against the logged-in user before it touches the database: you can only ever edit or delete what's yours.

<br>

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

<br>

## Overview

Twitto is a server-rendered microblogging app: users register, post short text updates with an optional image, edit or delete what they've posted, and search the feed by keyword. That's the entire product surface, deliberately.

The engineering choices underneath it are what the codebase is actually about. Every mutation is scoped to the authenticated owner at the query level, not just hidden behind a UI check. Configuration — secret keys, SMTP credentials, the debug flag — lives in environment variables and is read at runtime, never hardcoded. The `text` field is database-indexed because search is a real, expected query pattern, not an afterthought. The routing layer maps one URL to one view to one template, so tracing a request from `/twitto/<id>/edit/` to the database and back takes seconds, not a debugger session.

Nothing here is exotic. It's Django used the way Django is meant to be used — and a codebase small enough that reading it end to end is a reasonable way to spend an afternoon.

<br>


## Features

- **Full tweet lifecycle** — create, edit, and delete, each action scoped to the authenticated owner
- **Image attachments** — optional image upload on any tweet
- **Search** — filter the feed by keyword in real time
- **Authentication** — registration, login, and logout on Django's battle-tested auth system
- **Contact form** — visitor messages delivered straight to your inbox via SMTP
- **Environment-driven configuration** — every secret and credential loads from `.env`, never from source
- **Indexed schema** — tweet text is database-indexed for fast search as the feed grows
- **Live reload in development** — instant browser refresh on save, via `django-browser-reload`

<br>

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | [Django](https://www.djangoproject.com/) 5.1.6 |
| Language | Python 3.10+ |
| Database | SQLite (swap the `DATABASES` config for Postgres/MySQL in production) |
| Image handling | Pillow |
| Config management | `python-dotenv` |
| Dev experience | `django-browser-reload` |
| Deployment | PythonAnywhere |

<br>

## Architecture

**Data model**

```
User (Django built-in)
  └── Tweet
        ├── text         — indexed, max 300 chars
        ├── image         — optional
        ├── created_at    — set once, on creation
        └── updated_at    — refreshed on every save
```

**Routes**

| Method | Path | View | Auth | Purpose |
|---|---|---|:---:|---|
| GET | `/twitto/` | `tweetList` | — | List and search tweets |
| GET, POST | `/twitto/create/` | `tweetCreate` | ✅ | Compose a new tweet |
| GET, POST | `/twitto/<id>/edit/` | `tweetEdit` | ✅ | Edit a tweet you own |
| GET, POST | `/twitto/<id>/delete/` | `tweetDelete` | ✅ | Delete a tweet you own |
| GET, POST | `/twitto/contact/` | `contact` | — | Send a message via email |
| GET, POST | `/twitto/register/` | `register` | — | Create an account |
| — | `/accounts/*` | Django auth | — | Login / logout |
| — | `/admin/` | Django admin | Staff | Admin dashboard |

Every view that mutates a tweet fetches it scoped to `request.user` — there's no path where one account can touch another account's data by guessing an ID.

<br>

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone git@github.com:AhmadHussainRandhawa/twitto.git
cd twitto

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# then open .env and fill in SECRET_KEY, DEBUG, and your SMTP credentials

# Apply migrations
python manage.py migrate

# (Optional) create an admin account
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** — you'll land on `/twitto/`.

### Environment Variables

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django's cryptographic secret — unique per environment, never shared |
| `DEBUG` | `True` locally, **`False`** anywhere the app is publicly reachable |
| `EMAIL_HOST` | SMTP server (e.g. `smtp.gmail.com`) |
| `EMAIL_PORT` | SMTP port — `587` for TLS |
| `EMAIL_HOST_USER` | SMTP account username |
| `EMAIL_HOST_PASSWORD` | SMTP account password or app-specific password |
| `EMAIL_USE_TLS` | `True` to require TLS on the SMTP connection |

`.env` is already listed in `.gitignore` — it will never be committed.

<br>

## Project Structure

```
twitto/
├── tweet/                  # Core app
│   ├── models.py           # Tweet model
│   ├── views.py            # CRUD, auth, contact views
│   ├── forms.py            # TweetForm, UserRegistrationForm
│   ├── urls.py             # App-level routes
│   └── templates/          # tweetList, tweetForm, tweetConfirmDelete, contact
├── templates/              # Global templates — layout, registration
├── static/                 # CSS, JS, images
├── TweetWebsite/           # Project configuration
│   ├── settings.py
│   ├── urls.py             # Root routes
│   └── wsgi.py / asgi.py
├── .env.example
├── requirements.txt
└── manage.py
```

<br>

## Roadmap

- [ ] REST API via Django REST Framework
- [ ] Likes and replies
- [ ] Follow / following
- [ ] Feed pagination
- [ ] Rate limiting on tweet creation
- [ ] Docker Compose for one-command local setup
- [ ] CI with automated test coverage

Have an idea that's not listed? [Open an issue](https://github.com/AhmadHussainRandhawa/twitto/issues) — that's exactly what it's for.

<br>

## Contributing

Contributions are welcome! Whether you're fixing a bug, improving documentation, adding tests, or proposing a new feature, your contribution can help make Twitto better.

Please read the [Contributing Guide](CONTRIBUTING.md) before getting started.

If you find Twitto useful, consider giving the repository a ⭐ — it helps more people discover the project.

<br>

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for the full text.

<br>

## Contact

**Ahmad Hussain**

- GitHub — [@AhmadHussainRandhawa](https://github.com/AhmadHussainRandhawa)
- LinkedIn — [Ahmad Hussain](https://www.linkedin.com/in/ahmad-hussain-randhawa/)
- Project — [Twitto](https://github.com/AhmadHussainRandhawa/twitto)
