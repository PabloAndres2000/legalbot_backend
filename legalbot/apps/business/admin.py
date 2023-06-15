from django.contrib import admin

from legalbot.apps.business.models import Business, Faculty

# Register your models here.


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    """
    Business model admin.
    """

    list_display = ("name", "identification_number", "is_active", "created_at")
    list_display_link = ("name", "identification_number")


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """
    Faculty model admin.
    """

    list_display = ("name", "is_active", "created_at")
    list_display_link = "name"
