from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import HttpResponse
import requests
from django.contrib.auth.models import User
# Point to your deployed FastAPI backend
FASTAPI_BASE_URL = "https://sign-up-login-page-1.onrender.com/api/v1"

# ------------------- Home View ------------------- #
@login_required
def home(request):
    return render(request, 'home.html')


# ------------------- Register View ------------------- #
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration/register.html')

        try:
            response = requests.post(
                f"{FASTAPI_BASE_URL}/register",
                json={
                    "Username": username,
                    "Email": email,
                    "Password": password
                },
                timeout=10
            )

            if response.status_code == 200:
                messages.success(request, "Registration successful. Please log in.")
                return redirect('login')

            else:
                detail = response.json().get("detail", "Registration failed.")
                messages.error(request, detail)

        except requests.exceptions.RequestException:
            messages.error(request, "Unable to reach backend API.")

    return render(request, 'registration/register.html')


# ------------------- Login View ------------------- #
FASTAPI_BASE_URL = "https://your-fastapi-url.com/api/v1"

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')

        try:
            response = requests.post(
                f"{FASTAPI_BASE_URL}/login",
                json={"email": email, "password": password},
                timeout=5
            )

            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get("username")

                # Ensure user exists in Django DB
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={"email": email}
                )

                # Optionally, update password in Django DB (not used for FastAPI login)
                user.set_unusable_password()
                user.save()

                login(request, user)  # Django login
                return redirect('home')

            else:
                error_message = response.json().get("detail", "Login failed")
                messages.error(request, error_message)

        except requests.exceptions.RequestException:
            messages.error(request, "Could not connect to authentication server.")

    return render(request, 'registration/login.html')


# ------------------- Logout View ------------------- #
@require_GET
def logout_view(request):
    logout(request)
    return redirect('login')


# ✅ Test email functionality
from django.core.mail import send_mail

def test_email(request):
    send_mail(
        subject='Test Email',
        message='This is a test email from Django.',
        from_email='mamlakawallet1234@gmail.com',  # Match your EMAIL_HOST_USER in settings.py
        recipient_list=['mulwabenard9507@gmail.com'],  # Replace with your test recipient
        fail_silently=False
    )
    return HttpResponse('Test email sent!')
