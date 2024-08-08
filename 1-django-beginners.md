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
MVT (Model-View-Template):

![django-mvt-based-control-flow](https://github.com/user-attachments/assets/f09e8b74-7fc8-434f-97f6-59d550ae192b)

* **Model** : Defines and manages the data structure and database interaction.
* **View** : Handles request processing and business logic.
* **Template** : Renders HTML output with data provided by the View.
#
