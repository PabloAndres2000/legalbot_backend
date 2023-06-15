from typing import List, Union

from django.db.models.query import QuerySet

from legalbot.apps.business.models import Faculty


def get_all_faculties() -> Union[QuerySet, List[Faculty]]:
    """
    Retrieve all faculties.

    Returns:
        Retrieve all users.

    Returns:
        Union[QuerySet, List[Faculty]]: A collection of faculty. It can be a QuerySet or a list of Faculty instances.

    """
    try:
        business = Faculty.objects.all()
        return business
    except Faculty.DoesNotExist:
        return None
