import os
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from django.core.asgi import get_asgi_application

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_login.settings')

# Import your FastAPI app (change this path if different)
from fastapi_app.main import app as fastapi_app  # <-- Replace with your actual FastAPI app path

# Create the root FastAPI app
main_app = FastAPI()

origins = ["http://localhost:8000", "https://sign-up-login-page-10.onrender.com"]

# Enable CORS for API
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://sign-up-login-page-10.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount FastAPI at /api and Django at /
main_app.mount("/api", fastapi_app)
main_app.mount("/", WSGIMiddleware(get_asgi_application()))
