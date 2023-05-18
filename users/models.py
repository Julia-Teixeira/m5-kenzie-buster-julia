from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=127, unique=True, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    birthdate = models.DateField(null=True)
    is_employee = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"username: {self.username}, email: {self.email}"
