from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .forms import RegistrationForm, LoginForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from documents.models import DocumentModel

def register_view(request):
    if request.user.is_authenticated:
        return redirect('my_documents')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！')
            return redirect('my_documents')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('my_documents')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if form.cleaned_data.get('remember_me'):
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)
            
            messages.success(request, '登录成功！')
            return redirect('my_documents')
        else:
            messages.error(request, '用户名或密码错误')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, '已成功登出')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, '个人信息已更新')
        return redirect('profile')
    
    document_count = request.user.documents.filter(is_deleted=False).count()
    return render(request, 'accounts/profile.html', {'document_count': document_count})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '密码已更新')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            request.user.delete()
            messages.success(request, '账号已注销')
            return redirect('home')
        else:
            messages.error(request, '密码错误')
    
    return render(request, 'accounts/delete_account.html')

def forget_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user and user.email:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                reset_url = f"http://{current_site.domain}/reset-password/{uid}/{token}/"
                
                send_mail(
                    '密码重置',
                    render_to_string('accounts/password_reset_email.txt', {
                        'user': user,
                        'reset_url': reset_url,
                    }),
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            
            messages.success(request, '如果您的邮箱已注册，将收到密码重置邮件')
            return redirect('login')
    else:
        form = CustomPasswordResetForm()
    
    return render(request, 'accounts/forget_password.html', {'form': form})

def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '密码已重置，请登录')
                return redirect('login')
        else:
            form = CustomSetPasswordForm(user)
        
        return render(request, 'accounts/reset_password.html', {'form': form})
    else:
        messages.error(request, '链接无效或已过期')
        return redirect('login')
