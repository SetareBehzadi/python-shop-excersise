from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Passwords don't match")
        else:
            return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can not change password <a href="../password/">this form</a>')

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'last_login']


class UserRegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=255, label='Full Name')
    phone = forms.CharField(max_length=11, label='Phone Number')
    email = forms.EmailField( label='Email')
    password = forms.CharField(max_length=11, label='Password', widget=forms.PasswordInput)

    def clean_phone(self):
        phone = User.objects.filter(phone_number=self.cleaned_data['phone']).exists()
        if phone:
            raise ValidationError('This phone is already existed!')
        return self.cleaned_data['phone']

    def clean_email(self):
        email = User.objects.filter(email=self.cleaned_data['email']).exists()
        if email:
            raise ValidationError('This email is already existed!')
        return self.cleaned_data['email']


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label='phon number', max_length=11 )
    password = forms.CharField(label='password', widget=forms.PasswordInput())


class UserVerifyCode(forms.Form):
    code = forms.IntegerField()
