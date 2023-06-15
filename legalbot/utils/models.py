# Django models utilities
import uuid

from django.db import models


class BaseModel(models.Model):
    """
    BaseModel acts as an abstract base class from every other model in the project will inherit.
    this class provides every table with the following attributes
        + created_at (DateTimeField): Store the datetime the objects was created,
        + updated_at (DateTimeField): Store when the last data of a model was updated
        + is_active (BooleanField): Store show active fields by default of each action done in the project
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]
        get_latest_by = "created_at"
