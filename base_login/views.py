from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import HttpResponse
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

FASTAPI_BASE_URL = "https://sign-up-login-page-2.onrender.com"  # Your FastAPI backend URL

#  Home view
@login_required
def home(request):
    user_email = request.session.get('user_email')
    return render(request, 'home.html', {'user_email': user_email})


#  Register view
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
                "https://sign-up-login-page-3.onrender.com/register",  
                json={
                    "username": username,  #lowercase
                    "email": email,
                    "password": password
                },
                timeout=10
            )

            if response.status_code == 201:
                messages.success(request, "Registration successful. Please log in.")
                return redirect('login')
            else:
                detail = response.json().get("detail", "Registration failed.")
                messages.error(request, detail)

        except requests.exceptions.RequestException:
            messages.error(request, "Unable to reach backend API.")

    return render(request, 'registration/register.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')

        print(f"Attempting login with email: {email}")

        try:
            response = requests.post(
                f"{FASTAPI_BASE_URL}/login",
                json={"email": email, "password": password},
                timeout=15
            )

            print(f"fastAPI response code: {response.status_code}")
            print(f"FastAPI response body: {response.text}")
            if response.status_code == 200:
                user_data = response.json()

                # Check if user exists in Django, if not, create one
                user, created = User.objects.get_or_create(
                    username=user_data.get("username"),
                    defaults={"email": user_data.get("email")}
                )

                # Log them in using Django's auth system
                login(request, user)

                print(f"Logged in user: {user.username}, is_authenticated: {request.user.is_authenticated}")

                print(f"Redirecting to home for: {user.username}")




                # Save session info
                request.session['user_email'] = user_data.get("email")

                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')

            else:
                detail = response.json().get("detail", "Invalid credentials")
                messages.error(request, detail)

        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to connect to authentication server: {e}")

    return render(request, 'registration/login.html')


# Logout view
@require_GET
def logout_view(request):
    logout(request)
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('login')


# Test email functionality
from django.core.mail import send_mail

def test_email(request):
    try:
        send_mail(
            subject='Test Email',
            message='This is a test email from Django.',
            from_email='mamlakawallet1234@gmail.com',
            recipient_list=['mulwabenard9507@gmail.com'],
            fail_silently=False
        )
        return HttpResponse('Test email sent!')
    except Exception as e:
        return HttpResponse(f'Failed to send email: {str(e)}')
