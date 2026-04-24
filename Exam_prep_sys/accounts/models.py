from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    is_learner = models.BooleanField(default=True)

    def __str__(self):
        return self.username
