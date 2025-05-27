# Django Project Setup

This is a Django project with complete test coverage.

## Prerequisites
- Python 3.x
- pip (Python package installer)

## Setup Instructions

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create admin and users:
```bash
python manage.py populate_data
```

**Note:**  
When you run the `populate_data` Django command, the following user accounts are automatically created for you:

| Username             | Role        | Password          |
|----------------------|-------------|-------------------|
| ifedayo.akinsira     | Admin       | userpassword123   |
| alice.johnson        | User        | userpassword123   |
| bob.smith            | User        | userpassword123   |
| charlie.daniels      | User        | userpassword123   |
| diana.ross           | User        | userpassword123   |
| ethan.ray            | User        | userpassword123   |
| fiona.lee            | User        | userpassword123   |

- The **Admin** user (`ifedayo.akinsira`) has full access to the Django admin panel.
- All users have the same default password: `userpassword123`.

> **Important:** For security in production, please change these credentials immediately.

5. Run the development server:
```bash
python manage.py runserver
```

6. Run tests:
```bash
python manage.py test
```

## Admin Access
The system comes with a pre-configured superuser account for administrative access:

- URL: http://localhost:8000/admin/
- Username: ifedayo.akinsira
- Password: userpassword123

**Note**: For security in production, please change these credentials immediately.

## Project Structure
```
├── manage.py
├── requirements.txt
├── interview/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── projects/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── management/
│   │   └── commands/
│   │       └── populate_data.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── user_management/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── tests.py
│   └── views.py
└── tests/
    └── test_views.py
```

## Testing
- Unit tests are located in the `tests` directory
- Run tests using `python manage.py test`
- Test coverage report can be generated using `coverage run manage.py test && coverage report`