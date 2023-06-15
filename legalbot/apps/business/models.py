from django.db import models

from legalbot.utils.models import BaseModel


class Business(BaseModel):
    name = models.CharField(max_length=100)
    identification_number = models.CharField(max_length=20, unique=True)

    class Meta:
        app_label = "business"

    def __str__(self):
        return self.name


class Faculty(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "business"

    def __str__(self):
        return self.name
