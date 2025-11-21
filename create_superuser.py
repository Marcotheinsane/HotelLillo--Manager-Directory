import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_Lillo.settings")
django.setup()

User = get_user_model()

username = "admin"
password = "Admin12345"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    print("▶ Creando superusuario…")
    User.objects.create_superuser(username=username, password=password, email=email)
    print("✔ Superusuario creado")
else:
    print("✔ Ya existe un superusuario")