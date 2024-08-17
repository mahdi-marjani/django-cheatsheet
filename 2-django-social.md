## Index
- [connect app to project (recommended)](#connect-app-to-project-recommended-)
- [project structure with templates (recommended)](#project-structure-with-templates-recommended-)


### connect app to project (recommended) :

e.g. app name is `home`

&lt;project-name&gt;/home/apps.py:
```python
from django.apps import AppConfig

class HomeConfig(AppConfig):                                    # target
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
```

so :

&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
INSTALLED_APPS = [
    ...
    'home.apps.HomeConfig',                  # Add target here
    ...
]
```
#
### project structure with templates (recommended) :
e.g. app name is `home`
```text
<project-name>/
      ├── <project-name>/
      │     ├── __init__.py
      │     ├── asgi.py
      │     ├── settings.py
      │     ├── urls.py
      │     └── wsgi.py
      ├── home/                                # app name
      │     ├── migrations/
      │     │     └── __init__.py
      │     ├── templates/                     # templates related to this app
      │     │     └── home/                    # app name
      │     │          └── index.html          # home page
      │     ├── __init__.py
      │     ├── admin.py
      │     ├── apps.py
      │     ├── models.py
      │     ├── tests.py
      │     └── views.py
      ├── templates/                           # main templates
      │     ├── inc/                           # include templates
      │     │     └── navbar.html
      │     └── base.html
      └── manage.py
```
&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
TEMPLATES = [
    {
        ...
        'DIRS': [
            BASE_DIR / 'templates'            # main templates
        ],
        'APP_DIRS': True,                     # app templates
        ...
    },
]
#
