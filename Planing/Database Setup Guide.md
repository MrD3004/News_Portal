Database Setup Guide
This document explains how to configure and initialize the MySQL database for the News Portal project. 
It ensures that the application connects using a non‑root user, as required by best practices.

1. Environment Variables
Ensure your .env file includes the following database settings:
# Database Settings
DB_NAME=news_portal
DB_USER=news_user
DB_PASSWORD=news_password
DB_HOST=db
DB_PORT=3306
DB_ROOT_PASSWORD=your_root_password

DB_ROOT_PASSWORD is required for the MySQL container to initialize.

DB_USER and DB_PASSWORD define the non‑root application user.

DB_NAME is the database schema used by Django.

2. Container Initialization
When you run:
docker-compose up --build
the db service will:

Start a MySQL 8.0 container.

Create the database specified in DB_NAME.

Create the non‑root user (DB_USER) with the password (DB_PASSWORD).

Grant privileges on the database to this user.

3. Manual Verification (Optional)
To verify the setup:

bash
docker exec -it news_portal_db mysql -u root -p
Enter the DB_ROOT_PASSWORD from your .env. Then run:

sql
SHOW DATABASES;
USE news_portal;
SHOW TABLES;

SELECT user, host FROM mysql.user;
You should see your news_user listed with privileges on the news_portal database.

4. Django Settings Alignment
The Django settings.py file is configured to use the non‑root user:

python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env.int("DB_PORT"),
    }
}
This ensures Django connects with news_user instead of root.

5. Running Migrations
Once the database container is healthy, apply migrations:

bash
docker exec -it news_portal_web python manage.py migrate
This will create the necessary tables inside the news_portal schema.

6. Common Pitfalls
Root user errors: Do not use root credentials in Django settings. Always use DB_USER.

Missing .env variables: Ensure DB_ROOT_PASSWORD is defined, or the container will fail to start.

Healthcheck failures: Confirm that DB_USER has privileges; otherwise, the db service may not report healthy.