## Index
- [connect app to project (recommended)](#connect-app-to-project-recommended-)
- []()


### connect app to project (recommended) :

For example, app name is `home`:

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
