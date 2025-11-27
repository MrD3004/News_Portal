#News Portal (Django Project)

A role‑based news publishing platform built with **Django 5**, **MySQL**, and **Bootstrap**.  
It supports multiple user roles (Reader, Journalist, Editor, Publisher), subscription flows, newsletter management, and optional **Twitter/X integration** via Tweepy.

---

##Features

- **Custom User Roles**
  - **Reader**: Subscribe to publishers/journalists, view personalized feed.
  - **Journalist**: Create and manage articles, publish newsletters.
  - **Editor**: Review, approve, update, or delete articles.
  - **Publisher**: Register publishing houses.

- **Articles**
  - Journalists create articles.
  - Editors approve/reject articles.
  - Readers see only approved articles.

- **Publishers**
  - Publisher role can register publishing houses.
  - Readers can subscribe/unsubscribe to publishers.

- **Newsletters**
  - Journalists can create, update, and delete newsletters.
  - Readers can follow journalists to receive updates.

- **Subscriptions**
  - Readers can follow/unfollow publishers and journalists.
  - Personalized feed on homepage.

- **Twitter/X Integration**
  - When an editor approves an article, it can be auto‑posted to X (Twitter) using Tweepy.
  - Safe, optional, and disabled by default.

- **REST API**
  - Endpoint: `/api/subscribed-articles/` returns JSON of a reader’s subscribed articles.

---

#Tech Stack

- **Backend**: Django 5, Django REST Framework
- **Database**: MySQL (default), SQLite (optional for dev)
- **Frontend**: Bootstrap 5
- **Integration**: Tweepy (Twitter/X API)
- **Auth**: Django’s built‑in auth with custom user model

---

#Setup Instructions

1.Clone the Repository
```bash
git clone https://github.com/yourusername/news_portal.git
cd news_portal

2. Create Virtual Environment
bash
source myenv/Scripts/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the project root

5. Database Setup
python manage.py makemigrations
python manage.py migrate

6. Create Superuser
python manage.py createsuperuser

7. Run Development Server
python manage.py runserver

User Roles & Flows
Reader
Register → Subscribe to publishers/journalists → View personalized feed.

Journalist
Register → Create articles → Manage newsletters.

Editor
Register → Access editor dashboard → Approve/update/delete articles.

Publisher
Register → Register publishing house.

API Usage
Subscribed Articles
Endpoint: /api/subscribed-articles/
Auth: Session authentication
Returns JSON of approved articles from followed publishers/journalists.

Twitter/X Integration
Optional. Controlled by TWITTER_ENABLED in .env.
When enabled, approving an article posts a tweet:
New article: <title> <url>

news_portal/
├── articles/            # App with models, views, forms, serializers
├── templates/           # HTML templates (Bootstrap 5)
├── static/              # Static assets
├── news_portal/         # Project settings & URLs
├── requirements.txt
├── .env.example
└── README.md

Data Protection Notes
No personal data from X/Twitter is collected.
Only outbound posting of approved article titles/links.
All API keys stored in .env (never committed).
Readers’ subscriptions and accounts stored securely in the databas


Benefits
- README is now **complete, professional, and reviewer‑friendly**.  
- Covers **setup, roles, workflows, API, Twitter integration, and data protection**.  
- Provides a **clear onboarding path** for reviewers and new developers.  
---
Would you like me to also create a **short `README_API.md`** dedicated just to the REST API endpoints (with request/response examples) so reviewers can test them quickly?

Virtualenv setup:
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py runserver

Docker setup:
docker-compose up --build

Environment variables: Document required keys in .env:
DJANGO_SECRET_KEY=your_secret
DB_NAME=news_portal
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=3306
TWITTER_ENABLED=false
TWITTER_API_KEY=
TWITTER_API_SECRET=