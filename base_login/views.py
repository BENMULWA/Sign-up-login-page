from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import HttpResponse
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse

FASTAPI_BASE_URL = "https://sign-up-login-page-10.onrender.com"  # Your FastAPI backend URL

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
                "https://sign-up-login-page-10.onrender.com/register",  
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

        try:
            # First verify with FastAPI
            response = requests.post(
                f"{FASTAPI_BASE_URL}/login",
                json={"email": email, "password": password},
                timeout=10
            )

            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get("username")
                
                # Get or create user with unusable password
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': email,
                        'password': '!',  # Set unusable password
                        'is_active': True
                    }
                )
                
                if created:
                    user.set_unusable_password()
                    user.save()

                # Authenticate using a custom backend or just login
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)


                request.session['user_email'] = email 
                
                next_url = request.GET.get('next') or request.POST.get('next') or 'home'
                return redirect(next_url)

            else:
                messages.error(request, response.json().get("detail", "Invalid credentials"))
                
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Service unavailable: {str(e)}")

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
