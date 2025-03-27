from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=20, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

# Create your models here.
