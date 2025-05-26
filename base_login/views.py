from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_GET
import requests
# renders to home page if user was succeful login 
@login_required
def home(request):
    return render(request,'home.html')

#registarion by user vif its first login for succesful registration
from django.contrib import messages

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
                timeout=5
            )

            if response.status_code == 200:
                messages.success(request, "Registration successful. Please log in.")
                return redirect('login')
            else:
                messages.error(request, response.json().get("detail", "Registration failed."))

        except requests.exceptions.RequestException:
            messages.error(request, "Unable to reach backend API.")

    return render(request, 'registration/register.html')


FASTAPI_BASE_URL = "http://localhost:8000/api/v1"

#handling user login credentials with django authentication and gets the credentials from POST request and if they valid logins redirectshe user to home , otherwise an error

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
                request.session['user_email'] = user_data.get("email")
                return render(request, 'home.html', {"user_email": email})
            else:
                messages.error(request, "Invalid credentials")

        except requests.exceptions.RequestException as e:
            messages.error(request, "Failed to connect to authentication server")

    return render(request, 'registration/login.html')

# defines logiout and redirects user back again to login page



@require_GET
def logout_view(request):
    logout(request)
    return redirect('login')

# testing for email 

from django.core.mail import send_mail
from django.http import HttpResponse

# defines fow loogin email test must look like for user registration to be valid 
from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    send_mail(
        subject='Test Email',
        message='This is a test email from Django admin.',
        from_email='mamlakawallet1234@gmail.com',  # Must match EMAIL_HOST_USER in settings.py
        recipient_list=['mulwabenard9507@gmail.com'],  # Correct recipient email
        fail_silently=False  # Will raise errors if email fails
    )
    return HttpResponse('Test email sent!')

