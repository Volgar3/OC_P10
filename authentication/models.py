from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    MINIMUM_AGE = 15

    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.age is not None and self.age < self.MINIMUM_AGE:
            raise ValidationError(
                f"L'utilisateur doit avoir au moins {self.MINIMUM_AGE} ans (RGPD)."
            )
