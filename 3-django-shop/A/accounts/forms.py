from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):                                            # for admin panel
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)       # Password field
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  # Confirm password

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password']                 # Fields to include in form
    
    def clean_password2(self):                                                      # Check if passwords match
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('Passwords dont match.')
        return cd['password2']
    
    def save(self, commit=True):                                                    # Save user with hashed password
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):                                              # for admin panel
    password = ReadOnlyPasswordHashField(                                           # Read-only password field
                    help_text='you can change password using <a href="../password/">this form</a>.'
                )  

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'last_login']  # Fields to include in form
        
class UserRegistrationForm(forms.Form):                         # for user registration
    email = forms.EmailField()
    full_name = forms.CharField(label='Full Name')
    phone = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('Email is already taken')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('Phone number is already taken')
        return phone
    
class verifyCodeForm(forms.Form):
    code = forms.IntegerField()
    
class UserLoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
