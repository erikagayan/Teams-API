# Team Management API

## Overview
This project is a RESTful API built with Django and Django REST Framework (DRF) that provides functionality for user authentication, team management, and role-based permissions. The API allows for the creation of users, teams, and the assignment of users to teams with specific roles (admin, moderator, manager, regular user). It also includes JWT authentication using djangorestframework-simplejwt.

## Features
- User Authentication: Registration, login, and management of user accounts with email and password authentication.
- JWT Authentication: Secure authentication using JSON Web Tokens.
- Role-Based Permissions:
  - Admin: Full access to all resources and actions.
  - Moderator: Can manage users and teams but cannot delete superusers.
  - Manager: Can manage users and teams but cannot modify or delete moderators and admins.
  - Regular User: Can view teams and manage their own profile.
- Team Management: Create teams, add or remove users from teams, and manage team details.
- Admin Panel: Enhanced Django admin interface with custom user model and permissions.
- API Endpoints: CRUD operations for users and teams with appropriate permissions.

## Technologies Used
- Python 3.x
- Django 3.x or higher
- Django REST Framework
- Django REST Framework SimpleJWT
- PostgreSQL
- Docker 

## Installation
### Prerequisites
- Python 3.x installed on your system.
- PostgreSQL database setup (or another database of your choice).
- Virtual environment tool (venv, virtualenv, or conda).
### Steps
1. Clone the repository:
```bash
git clone https://github.com/erikagayan/Teams-API.git
cd team-api
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the database:
- Update the settings.py file with your database configuration:
```json
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Roles and Permissions
### Admin:
- Full access to all endpoints and admin panel.
- Can create, update, and delete any user or team.
### Moderator:
- Access to user and team management endpoints.
- Cannot delete or modify superusers.
### Manager:
- Access to user and team management endpoints.
- Cannot modify or delete moderators and admins.
### Authenticated User:
- Can view teams and manage their own profile.
### Anonymous User:
- Can only view the list of teams and team details.