from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .forms import UserRegistrationForm, verifyCodeForm, UserLoginForm
import random
from .models import OtpCode, User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from . import tasks


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            phone = form.cleaned_data['phone']
            tasks.send_otp_code_task.delay(phone, random_code)
            OtpCode.objects.update_or_create(
                phone_number=phone,
                defaults={'code': random_code}
            )
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'We sent you a code', extra_tags='success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = verifyCodeForm
    
    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})
        
    def post(self, request):
        user_session = request.session.get('user_registration_info')
        if not user_session:
            messages.error(request, 'Session expired. Please register again.', 'danger')
            return redirect('accounts:register')
        
        try:
            code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        except OtpCode.DoesNotExist:
            messages.error(request, 'No OTP code found. Please register again.', 'danger')
            return redirect('accounts:register')
        
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                if code_instance.created < timezone.now() - timedelta(minutes=2):
                    messages.error(request, 'Code is expired. Please request a new code.', 'danger')
                    return redirect('accounts:verify_code')
                
                User.objects.create_user(
                    user_session['phone_number'], user_session['email'],
                    user_session['full_name'], user_session['password']
                )
                
                code_instance.delete()
                messages.success(request, 'You registered', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'Code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class ResendOtpView(View):
    def get(self, request):
        user_session = request.session.get('user_registration_info')
        if not user_session:
            messages.error(request, 'Session expired. Please register again.', 'danger')
            return redirect('accounts:register')
        
        try:
            code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        except OtpCode.DoesNotExist:
            messages.error(request, 'No OTP code found. Please register again.', 'danger')
            return redirect('accounts:register')
        
        if code_instance.created > timezone.now() - timedelta(seconds=60):
            messages.error(request, 'Please wait before requesting a new code.', 'danger')
            return redirect('accounts:verify_code')
        
        random_code = random.randint(1000, 9999)
        tasks.send_otp_code_task.delay(user_session['phone_number'], random_code)
        
        code_instance.code = random_code
        code_instance.save()
        
        messages.success(request, 'A new code has been sent.', 'success')
        return redirect('accounts:verify_code')

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    
    def setup(self, request, *args, **kwargs) -> None:
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['phone'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'User logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request, 'Invalid credentials', 'danger')
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})

class UserLogoutView(View):    
    def get(self, request):
        logout(request)
        messages.success(request, 'User logged out successfully!', extra_tags='success')
        return redirect('home:home')