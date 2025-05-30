MyBlog

A simple blog platform built with Django and Django REST Framework. Includes CRUD, comments, OAuth and normal authentication, dark mode, rate limiting, profanity filtering, and API docs. Dockerized with PostgreSQL.

-------------------------------------------------------------------------------------------------------------------------------------------------------------

Features:

Django + DRF

PostgreSQL

OAuth2 and normal auth

Create, read, update, delete posts

Comments

Dark theme toggle

Rate limiting

Profanity filter

API docs (admin access)

Docker support

-------------------------------------------------------------------------------------------------------------------------------------------------------------

Setup:

1 - Clone the repo:

bash
git clone https://github.com/juganstar/jugans.git
cd myblog


2 - Create a .env file:

ini
DEBUG=1
SECRET_KEY=your-secret-key
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypass


3 - Run the app:

css
docker-compose up --build

4 - Visit http://localhost:8000

-------------------------------------------------------------------------------------------------------------------------------------------------------------

API Docs:

Docs available at /api/docs/ (admin only)

-------------------------------------------------------------------------------------------------------------------------------------------------------------

Admin Panel:

Visit /admin/ to manage content.

-------------------------------------------------------------------------------------------------------------------------------------------------------------

Notes:

Profanity filter applies to posts.

Rate limits are configured in settings.py.

OAuth setup requires provider credentials.

-------------------------------------------------------------------------------------------------------------------------------------------------------------

Contact:
[Valdemar Santos]
[valdemardjango@hotmail.com]
[https://www.linkedin.com/in/valdemar-santos-0431a0364/]
[https://github.com/juganstar]

