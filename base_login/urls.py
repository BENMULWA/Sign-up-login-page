from django.urls import path
from .views import home, register_view, login_view, logout_view, test_email
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='root_home'),
    path('home/', home, name='home'),
    path('register/', register_view, name='register'),

    path('login/', login_view, name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('mail/', test_email, name='test_email'),
]
