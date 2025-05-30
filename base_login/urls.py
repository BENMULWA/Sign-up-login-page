from django.urls import path
from . import views
from django.http import JsonResponse

urlpatterns = [
    path('', views.home, name='home'),  # Handles '/'
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('mail/', views.test_email, name='test_email'),
    path('.well-known/appspecific/com.chrome.devtools.json', lambda r: JsonResponse({}), name='chrome_devtools'),
]
