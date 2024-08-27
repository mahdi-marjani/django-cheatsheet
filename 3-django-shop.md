## Index
- [customize user model (Substituting a custom User model)](#customize-user-model-substituting-a-custom-user-model-)



### customize user model (Substituting a custom User model) :
&lt;project-name&gt;/accounts/models.py:
```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):  # Custom user model
    # Email field, must be unique
    email = models.EmailField(max_length=255, unique=True)
    # Phone number field, must be unique
    phone_number = models.CharField(max_length=11, unique=True)
    # Full name field (required)
    full_name = models.CharField()
    # Check if the user is active
    is_active = models.BooleanField(default=True)
    # Check if the user is an admin
    is_admin = models.BooleanField(default=False)

    # The field used for logging in (phone number in this case); this field must be unique
    USERNAME_FIELD = 'phone_number'
    # Fields that are required along with the USERNAME_FIELD
    REQUIRED_FIELDS = ['email', 'full_name']

    # String representation of the user object
    def __str__(self):
        return self.email
    
    # Always returns True, allows all permissions
    def has_perm(self, perm, obj=None):
        return True
    
    # Always returns True, allows all app label permissions
    def has_module_perms(self, app_label):
        return True
    
    # If the user is admin, they can access the admin panel
    @property
    def is_staff(self):
        return self.is_admin
```
#
