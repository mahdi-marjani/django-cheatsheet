## Index
- [customize user model (Substituting a custom User model)](#customize-user-model-substituting-a-custom-user-model-)



### customize user model (Substituting a custom User model) :
&lt;project-name&gt;/accounts/models.py:
```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):  # Custom user model
    email = models.EmailField(max_length=255, unique=True)        # Email field, must be unique
    phone_number = models.CharField(max_length=11, unique=True)   # Phone number field, must be unique
    full_name = models.CharField()                                # Full name field (required)
    is_active = models.BooleanField(default=True)                 # Check if the user is active
    is_admin = models.BooleanField(default=False)                 # Check if the user is an admin

    USERNAME_FIELD = 'phone_number'                               # The field used for logging in; this field must be unique
    REQUIRED_FIELDS = ['email', 'full_name']                      # Fields that are required along with the USERNAME_FIELD

    def __str__(self):                                            # String representation of the user object
        return self.email
    
    def has_perm(self, perm, obj=None):                           # Always returns True, allows all permissions
        return True
    
    def has_module_perms(self, app_label):                        # Always returns True, allows all app label permissions
        return True
    
    @property
    def is_staff(self):                                           # If the user is admin, they can access the admin panel
        return self.is_admin
```
#
