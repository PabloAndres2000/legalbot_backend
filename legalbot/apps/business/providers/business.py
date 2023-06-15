from typing import List, Optional, Union

from django.db import IntegrityError
from django.db.models import Q, QuerySet

from legalbot.apps.business.models import Business


def get_business_by_uuid(uuid: str) -> Optional[Business]:
    """
    Retrieve an business by UUID.

    Parameters:
        uuid (str): The UUID of the business.

    Returns:
        Optional[Business]: returns the business instance if found, otherwise None.
    """
    try:
        business = Business.objects.get(uuid=uuid)
        return business
    except Business.DoesNotExist:
        return None


def get_all_business() -> Union[QuerySet, List[Business]]:
    """
    Retrieve all business.

    Returns:
        Union[QuerySet, List[Business]]: A collection of business. It can be a QuerySet or a list of Business instances.
    """
    try:
        business = Business.objects.all()
        return business
    except Business.DoesNotExist:
        return None


def create_partner(
    name: str,
    identification_number: str,
) -> Optional[Business]:
    """
    Method for create business
    Parameters:
        name (str): Name of the business.
        identification_number (str): Business identification number.

    Returns:
        Optional[Business]: returns the business instance if found, otherwise None.
    """
    try:
        business = Business.objects.create(
            name=name,
            identification_number=identification_number,
        )
        return business
    except IntegrityError:
        raise Exception("Error creating business")


def check_if_business_identification_number_exist(identification_number: str) -> bool:
    """
    Method to check if a business with the given identification number exists.

    Parameters:
        identification_number (str): Business identification number

    Returns:
        bool: Returns True if a business exists with the given identification number, False otherwise.
    """
    try:
        business_exists = Business.objects.filter(
            identification_number__iexact=identification_number
        ).exists()

        return business_exists
    except Business.DoesNotExist:
        return False


def check_if_business_name_exist(name: str) -> bool:
    """
    Method to check if a business with the given name exists.

    Parameters:
        name (str): Business name

    Returns True if a partner exists with the given name, False otherwise.
    """
    try:
        business_exists = Business.objects.filter(name__iexact=name).exists()

        return business_exists
    except Business.DoesNotExist:
        return False


def get_business_by_manager_or_partner_id_number(
    identification_number: str,
) -> List[Business]:
    """
    Filter business that contain the partner or administrator with the specified identification number.

    Parameters:
        identification_number (str): The identification number of the partner or administrator.

    Returns:
        List[Business]: will return a list of business model objects.

    """
    try:
        business = Business.objects.filter(
            Q(partners__user__identification_number=identification_number)
            | Q(administrators__user__identification_number=identification_number)
        ).distinct()
        return list(business)
    except Business.DoesNotExist:
        return None


def get_business_by_identification_number(
    identification_number: str,
) -> Optional[Business]:
    """
    Retrieve a business by its identification number.

    Parameters:
        identification_number (str): identification number of the business.

    Returns:
        Optional[Business]: returns the business instance if found, otherwise None.

    """
    try:
        business = Business.objects.get(identification_number=identification_number)
        return business
    except Business.DoesNotExist:
        return None
