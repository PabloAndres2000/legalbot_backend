from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from legalbot.apps.users.utils.user_manage import UserManager
from legalbot.utils.models import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    identification_number = models.CharField(
        max_length=12, unique=True
    )
    ip_address = models.JSONField(default=dict, null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        app_label = "users"

    objects = UserManager()
    USERNAME_FIELD = "identification_number"
    REQUIRED_FIELDS = ["first_name"]

    @property
    def user_full_name(self):
        formatted_user_name = list()
        if self.first_name:
            formatted_user_name.append(self.first_name)
        if self.last_name:
            formatted_user_name.append(self.last_name)
        return " ".join(formatted_user_name)

    @property
    def is_admin(self):
        return self.is_staff and self.groups.filter(name="admin").exists()

    def __str__(self):
        return self.user_full_name


class Partner(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="partners")
    business = models.ForeignKey(
        "business.Business", on_delete=models.CASCADE, related_name="partners"
    )
    address = models.CharField(max_length=200)
    participation = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = "users"

    def __str__(self):
        return self.user.identification_number


class Administrator(BaseModel):
    business = models.ForeignKey(
        "business.Business", on_delete=models.CASCADE, related_name="administrators"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="administrators"
    )
    faculties = models.ManyToManyField(
        "business.Faculty", related_name="administrators_faculties"
    )

    class Meta:
        app_label = "users"

    def __str__(self):
        return self.user.identification_number
