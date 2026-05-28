from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    path('forget-password/', views.forget_password_view, name='forget_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_view, name='reset_password'),
]
