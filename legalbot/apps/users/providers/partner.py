from typing import List, Optional, Union

from django.db import IntegrityError
from django.db.models.query import QuerySet

from legalbot.apps.users.models import Partner
from legalbot.apps.users.providers import user as user_providers
from legalbot.apps.users.utils.lib.exceptions import PartnerDoesNotExist


def get_partner_by_uuid(uuid: str) -> Optional[Partner]:
    """
    Retrieve an partner by UUID.

    Parameters:
        uuid (str): The UUID of the partner.

    Returns:
        Optional[Partner]: returns the partner instance if found, otherwise None.
    """
    try:
        partner = Partner.objects.get(uuid=uuid)
        return partner

    except Partner.DoesNotExist:
        raise PartnerDoesNotExist


def get_partner_by_identification_number(identification_number: str) -> List[Partner]:
    """
    Filter to find already existing partner identification number

    Parameters:
        identification_number (str): partner identification number

    Returns:
        List[Partner]: will return a list of partner model objects.
    """
    try:
        partners = Partner.objects.filter(
            user__identification_number=identification_number
        )
        return list(partners)
    except Partner.DoesNotExist:
        raise PartnerDoesNotExist


def get_active_partners() -> Union[QuerySet, List[Partner]]:
    """
    Method for get active partners

    Returns:
        will return a QuerySet or a list containing instances of the Partner model.
    """
    try:
        users = Partner.objects.filter(is_active=True).order_by(
            "user__identification_number"
        )
        return users
    except Partner.DoesNotExist:
        return None


def create_partner(
    user: "users.User",
    business: "business.Bussines",
    address: str,
    participation: int,
) -> Optional[Partner]:
    """
    Method for create partner

    Parameters:
        user (str): The UUID of the user.
        business (str): The UUID of the business.
        address: (str): address name
        participation: (int): number of shares of the partner

    Returns:
        Optional[Partner]: returns the partner instance if found, otherwise None.
    """
    try:
        partner = Partner.objects.create(
            user=user,
            business=business,
            address=address,
            participation=participation,
        )
        user_providers.add_group_to_user(user=user, group_name="partner")
        return partner
    except IntegrityError:
        raise Exception("Error creating partner: IntegrityError")


def check_if_partner_identification_number_exist(identification_number: str) -> bool:
    """
    Method to check if a partner with the given identification number exists.

    Parameters:
        identification_number (str): partner identification number

    Returns:
        bool: Returns True if a partner exists with the given identification number, False otherwise.
    """
    try:
        partner_exists = Partner.objects.filter(
            user__identification_number__iexact=identification_number
        ).exists()
        return partner_exists
    except Partner.DoesNotExist:
        return False


def check_if_partner_already_exists(
    user_uuid: str, business_uuid: str, address: str
) -> bool:
    """
    Check if an partner already exists for the given user UUID and business UUID and address.

    Parameters:
        user_uuid (str): The UUID of the user.
        business_uuid (str): The UUID of the business.
        address: (str): address name

    Returns:
        bool: True if an partner exists for the given user and business, False otherwise.
    """
    try:
        partner = Partner.objects.filter(
            user=user_uuid, business=business_uuid, address=address
        )
        return partner.exists()
    except Partner.DoesNotExist:
        return False
