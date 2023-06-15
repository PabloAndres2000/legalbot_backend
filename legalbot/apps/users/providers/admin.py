from typing import List, Optional, Union

from django.db import IntegrityError
from django.db.models.query import QuerySet

from legalbot.apps.users.models import Administrator
from legalbot.apps.users.providers import user as user_providers


def get_admin_by_uuid(uuid: str) -> Optional[Administrator]:
    """
    Retrieve an administrator by UUID.

    Parameters:
        uuid (str): The UUID of the administrator.

    Returns:
        Optional[Administrator]: returns the manager instance if found, otherwise None.
    """
    try:
        admin = Administrator.objects.get(uuid=uuid)
        return admin
    except Administrator.DoesNotExist:
        return None


def get_admin_by_identification_number(
    identification_number: str,
) -> List[Administrator]:
    """
    Filter to find already existing administrator identification number

    Parameters:
        identification_number (str): administrator identification number

    Returns:
        List[Administrator]: will return a list of manager model objects.
    """
    try:
        admins = Administrator.objects.filter(
            user__identification_number=identification_number
        )
        return list(admins)
    except Administrator.DoesNotExist:
        return None


def check_if_admin_identification_number_exist(identification_number: str) -> bool:
    """
    Method to check if a admin with the given identification number exists.

    Parameters:
        identification_number (str): administrator identification number

    Returns:
        bool: Returns True if a admin exists with the given identification number, False otherwise.
    """
    try:
        admin_exists = Administrator.objects.filter(
            user__identification_number__iexact=identification_number
        ).exists()
        return admin_exists
    except Administrator.DoesNotExist:
        return False


def get_active_admin() -> Union[QuerySet, List[Administrator]]:
    """
    Method for get active admin

    Returns:
        will return a QuerySet or a list containing instances of the Administrator model.
    """
    try:
        admin = Administrator.objects.filter(is_active=True).order_by(
            "user__identification_number"
        )
        return admin
    except Administrator.DoesNotExist:
        return None


def create_admin(
    user: str,
    business: str,
) -> Optional[Administrator]:
    """
    Method for create admin

    Parameters:
        user (str): The UUID of the user.
        business (str): The UUID of the business.

    Returns:
        Optional[Administrator]: returns the manager instance if found, otherwise None.
    """
    try:
        admin = Administrator.objects.create(
            user=user,
            business=business,
        )
        user_providers.add_group_to_user(user=user, group_name="admin")
        return admin
    except IntegrityError:
        raise Exception("Error creating Administrator")


def check_if_admin_already_exists(user_uuid: str, business_uuid: str) -> bool:
    """
    Check if an administrator already exists for the given user UUID and business UUID.

    Parameters:
        user_uuid (str): The UUID of the user.
        business_uuid (str): The UUID of the business.

    Returns:
        bool: True if an administrator exists for the given user and business, False otherwise.
    """
    try:
        admin = Administrator.objects.filter(user=user_uuid, business=business_uuid)
        return admin.exists()
    except Administrator.DoesNotExist:
        return False
