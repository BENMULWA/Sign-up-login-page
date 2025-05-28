# auth/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import requests
from django.conf import settings

User = get_user_model()

class FastAPIAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Call your FastAPI login endpoint
            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/login/",
                json={"email": username, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return self.get_or_create_django_user(user_data)
            return None
        except requests.ConnectionError:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_or_create_django_user(self, user_data):
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'is_active': True
            }
        )
        if created:
            user.set_unusable_password()  # We don't store passwords in Django
            user.save()
        return user