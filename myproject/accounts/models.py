from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} [{self.reputation}]"
