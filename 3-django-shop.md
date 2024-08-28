## Index
- [custom user model (Substituting a custom User model)](#custom-user-model-substituting-a-custom-user-model-)
- [custom user manager](#custom-user-manager)



### custom user model (Substituting a custom User model) :
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
### custom user manager:
&lt;project-name&gt;/accounts/managers.py:
```python
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password):       # Create a regular user
        if not phone_number:
            raise ValueError('Users must have a phone number')             # Phone number is required
        if not email:
            raise ValueError('Users must have an email address')           # Email is required
        if not full_name:
            raise ValueError('Users must have a full name')                # Full name is required
        
        user = self.model(
            phone_number = phone_number,
            email = self.normalize_email(email),                           # Normalize the email
            full_name = full_name
        )

        user.set_password(password)                                        # Hash and set the password
        user.save(using=self._db)                                          # Save the user in the database
        return user

    def create_superuser(self, phone_number, email, full_name, password):  # Create a super user
        user = self.create_user(
            phone_number = phone_number,
            email = email,
            full_name = full_name,
            password = password
        )

        user.is_admin = True                                               # Make the user an admin
        user.save(using=self._db)                                          # Save the superuser in the database

        return user
```
&lt;project-name&gt;/accounts/models.py:
```python
...
from .managers import UserManager                                  # Manager 

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()                                        # Connect manager to model
    ...
```
#
