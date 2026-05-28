from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='选填，用于密码找回')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已被注册')
        return username
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError('密码长度至少为8位')
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            raise forms.ValidationError('密码必须包含字母和数字')
        return password

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='记住我')

class CustomPasswordChangeForm(PasswordChangeForm):
    pass

class CustomPasswordResetForm(PasswordResetForm):
    pass

class CustomSetPasswordForm(SetPasswordForm):
    pass
