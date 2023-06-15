from django.contrib import admin

from legalbot.apps.users.models import Administrator, Partner, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    User model admin.
    """

    list_display = (
        "first_name",
        "last_name",
        "identification_number",
        "is_active",
        "ip_address",
    )
    list_display_link = ("identification_number", "first_name", "last_name")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """
    Partner model admin.
    """

    list_display = (
        "get_user_identification_number",
        "get_user_first_name",
        "get_user_last_name",
        "is_active",
        "get_user_is_staff",
    )

    def get_user_identification_number(self, obj):
        return obj.user.identification_number

    get_user_identification_number.short_description = "Identification Number"

    def get_user_first_name(self, obj):
        return obj.user.first_name

    get_user_first_name.short_description = "First Name"

    def get_user_last_name(self, obj):
        return obj.user.last_name

    get_user_last_name.short_description = "Last Name"

    def get_user_is_staff(self, obj):
        return obj.user.is_staff

    get_user_is_staff.short_description = "Is Staff"


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    """
    Administrator model admin.
    """

    list_display = ("route", "first_name", "last_name", "faculty_names")

    @admin.display(description="Identification Number")
    def route(self, obj):
        return obj.user.identification_number

    @admin.display(description="First Name")
    def first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Last Name")
    def last_name(self, obj):
        return obj.user.last_name

    @admin.display(description="Faculties")
    def faculty_names(self, obj):
        return ", ".join(faculty.name for faculty in obj.faculties.all())
