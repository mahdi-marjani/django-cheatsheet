start project:
```bash
django-admin startproject <project-name>
```
Project structure:
```text
<project-name>/
      ├── <project-name>/
      │         ├── __init__.py        # Marks this directory as a Python package.
      │         ├── asgi.py            # ASGI configuration for async servers.
      │         ├── settings.py        # Project settings and configuration.
      │         ├── urls.py            # URL routing for the project.
      │         └── wsgi.py            # WSGI configuration for traditional servers.
      └── manage.py                    # Command-line tool for managing the project.
```
run project:
```bash
python manage.py runserver
```
#
