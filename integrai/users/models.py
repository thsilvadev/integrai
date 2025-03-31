from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)  # Agora pode ser nulo e em branco
    phone_number = models.CharField(max_length=20, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)  # Agora pode ser nulo e em branco
    waiting_data = models.CharField(max_length=100, null=True, blank=True)  # Para armazenar o estado
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

# Create your models here.
