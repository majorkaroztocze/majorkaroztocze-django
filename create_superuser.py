import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # zmień na swoje, jeśli masz inną nazwę

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin2")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "rezerwacje.majorkaroztocze@gmail.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123321")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✔ Superuser created")
else:
    print("⚠ Superuser already exists")
