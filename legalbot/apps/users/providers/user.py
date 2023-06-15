import datetime as dt
from typing import List, Optional, Tuple, Union

from django.contrib.auth import authenticate
from django.db.models.query import QuerySet

from legalbot.apps.users.models import User
from legalbot.apps.users.providers import group as group_providers
from legalbot.apps.users.providers import token as token_providers
from legalbot.apps.users.utils.lib.exceptions import (
    CantCreateUser,
    CantUpdateUser,
    GroupDoesNotExist,
)


def get_user_by_uuid(uuid: str) -> Optional[User]:
    """
    Retrieve an user by UUID.

    Parameters:
        uuid (str): The UUID of the user.

    Returns:
        Optional[User]: returns the user instance if found, otherwise None.
    """
    try:
        user = User.objects.get(uuid=uuid)
        return user
    except User.DoesNotExist:
        return None


def get_all_users() -> Union[QuerySet, List[User]]:
    """
    Retrieve all users.

    Returns:
        Union[QuerySet, List[User]]: A collection of users. It can be a QuerySet or a list of User instances.
    """
    try:
        users = User.objects.all()
        return users
    except User.DoesNotExist:
        return None


def add_group_to_user(user: User, group_name: str) -> None:
    """
    Add a group to a user.

    Parameters:
        user (User): The user instance(model).
        group_name (str): The name of the group to add.

    Returns:
        None: This function doesn't return anything.
    """
    try:
        group = group_providers.get_group_by_name(name=group_name)
        user.groups.add(group)
    except (User.DoesNotExist, GroupDoesNotExist):
        return None


def create_user(
    first_name: str,
    last_name: str,
    identification_number: str,
    ip_address: str,
    password: str,
) -> Optional[User]:
    """
    Method for create user
    Parameters:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        identification_number (str): User identification number.
        ip_address (str): The IP address of the user.
        password (str): The password for the user.

    Returns:
        Optional[User]: returns the user instance if found, otherwise None.
    """
    try:
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            identification_number=identification_number,
            is_staff=True,
        )
        user.set_password(password)
        user.save()
        add_ip_address_by_user(user=user, ip_address=ip_address)
        add_group_to_user(user=user, group_name="admin")
        return user
    except User.DoesNotExist:
        raise CantCreateUser


def add_ip_address_by_user(user: User, ip_address: str) -> None:
    """
    Add an IP address to the user's IP address field.

    Parameters:
        user (User): The user instance.
        ip_address (str): The IP address to add.

    Returns:
        None: This function doesn't return anything.
    """
    if not user.ip_address.get(ip_address):
        user.ip_address[ip_address] = str(dt.datetime.now())
        user.save(update_fields=["ip_address", "updated_at"])


def check_user_is_owner_or_staff(request_user: "users.User", user_uuid: str) -> bool:
    """
    Check if the request user is the owner of the user or is a staff member.

    Parameters:
        request_user (users.User): The user making the request.
        user_uuid (str): The UUID of the user to check.

    Returns:
        bool: True if the request user is the owner of the user or is a staff member, False otherwise.
    """
    if int(request_user.uuid) == user_uuid:
        return True
    return request_user.is_staff


def login(
    identification_number: str,
    password: str,
    ip_address: str,
) -> Tuple[Optional[User], Optional[str]]:
    """
    Perform user login by authenticating the identification number and password.

    Parameters:
        identification_number (str): The identification number of the user.
        password (str): The password of the user.
        ip_address (str): The IP address of the login request.

    Returns:
        Tuple[Optional[User], Optional[str]]: A tuple containing the user instance and the authentication token key.
            If the login is successful, the user instance and the token key are returned.
            If the login fails, None is returned for both the user instance and the token key.

    """
    user = authenticate(username=identification_number, password=password)
    if user:
        token = token_providers.remove_token_by_user_uuid(
            user_uuid=user.uuid, generate_new_token=True
        )
        add_ip_address_by_user(user=user, ip_address=ip_address)
        return user, token.key
    return None, None


def update_password_by_uuid(uuid: str, password: str) -> Optional[User]:
    """
    Update the password of a user by UUID.

    Parameters:
        uuid (str): The UUID of the user.
        password (str): The new password to set.

    Returns:
        Optional[User]: The updated user instance if successful, or None if the user doesn't exist.

    Raises:
        CantUpdateUser: If an error occurs while updating the user's password.

    """
    user = get_user_by_uuid(uuid=uuid)
    if not user:
        return None
    try:
        user.set_password(password)
        user.save()
        return user
    except User.DoesNotExist:
        raise CantUpdateUser


def check_if_user_identification_number_exist(identification_number: str) -> bool:
    """
    Method to check if a user with the given identification number exists.

    Parameters:
        identification_number (str): user identification number

    Returns:
        bool: Returns True if a user exists with the given identification number, False otherwise.
    """
    try:
        user_exists = User.objects.filter(
            identification_number__iexact=identification_number
        ).exists()
        return user_exists
    except User.DoesNotExist:
        return False


def update_user_by_uuid(user_uuid: str, **kwargs) -> Optional[User]:
    """
    Update a user by UUID with the specified fields.

    Parameters:
        user_uuid (str): The UUID of the user to update.
        **kwargs: Additional fields and values to update on the user.

    Returns:
        Optional[User]: The updated user instance if successful, or None if the user doesn't exist.

    Raises:
        CantUpdateUser: If an error occurs while updating the user.
    """
    try:
        user = get_user_by_uuid(uuid=user_uuid)
        update_fields = ["updated_at"]
        for key, value in kwargs.items():
            setattr(user, key, value if callable(value) else value)
            update_fields.append(key)
        user.save(update_fields=update_fields)
        return user
    except User.DoesNotExist:
        raise CantUpdateUser
