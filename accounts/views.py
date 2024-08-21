from django.shortcuts import render, redirect
from django.views import View
import random
from accounts.forms import UserRegistrationForm, UserVerifyCode, UserLoginForm
from accounts.models import OtpCode
from utils import send_otp_code
from django.contrib import messages
from .models import User
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator

def hide_from_logged_in_users(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseForbidden("You are already logged in.")
        return view_func(request, *args, **kwargs)
    return wrapper


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=code)
            request.session['user_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],

            }
            messages.success(request, 'We send a Code.', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserVerifyCode(View):
    verify_form = UserVerifyCode

    @method_decorator(hide_from_logged_in_users)
    def get(self, request):
        form = self.verify_form
        return render(request, 'accounts/verifyCode.html', {'vform': form})

    @method_decorator(hide_from_logged_in_users)
    def post(self, request):
        user_session = request.session['user_info']
        form = self.verify_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            try:
                code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'], code=cd['code'])
            except OtpCode.DoesNotExist:
                messages.error(request, 'No OTP code found for this phone number.', 'danger')
                print("gggg" * 10)
                print('Eroor')
                return redirect('accounts:verify_code')
            print('sss' * 20)
            print(timezone.now())
            print(user_session['phone_number'])
            expiration_time = code_instance.created_at + timedelta(minutes=2)
            print(expiration_time)
            if timezone.now() > expiration_time:
                messages.error(request, 'This code has expired. Please request a new one.', 'danger')
                code_instance.delete()
                return redirect('accounts:user_login')

            if cd['code'] == code_instance.code:
                user_login = authenticate(request, username=user_session['phone_number'], password=user_session['password'])
                if user_login:
                    login(request, user_login)
                    messages.success(request, 'you logged in successfully', 'successful')
                else:
                    User.objects.create_user(user_session['phone_number'], user_session['email'], user_session['full_name'],
                                         user_session['password'])
                    messages.success(request, 'you registered successfully!', 'success')
                code_instance.delete()

                return redirect('home:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logout successfully!', 'success')
        return redirect('home:home')

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # data ro begirim
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(phone_number=form.cleaned_data['phone_number'])
            except User.DoesNotExist:
                messages.error(request, 'User with this phone number does not exist.', 'warning')
                return redirect('accounts:user_register')

            user = User.objects.get(phone_number=form.cleaned_data['phone_number'])
            if not user:
                raise messages.error(request, 'something is wrong', 'warning')
            otp_code = random.randint(1000, 9999)
            # send_otp_code(user.phone_number, otp_code)
            OtpCode.objects.create(phone_number=user.phone_number, code=otp_code)
            request.session['user_info'] = {
                'phone_number': user.phone_number,
                'email': user.email,
                'full_name': user.full_name,
                'password': form.cleaned_data['password']
            }
            messages.success(request, 'sending login code')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})
