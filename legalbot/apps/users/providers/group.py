from typing import Optional

from django.contrib.auth.models import Group


def get_group_by_name(name: str) -> Optional[Group]:
    """
    Get group by name

    Parameters:
        name (str): group name
    Returns:
        Optional[Group]: returns the group instance if found, otherwise None.
    """
    try:
        group = Group.objects.get(name=name)
        return group
    except Group.DoesNotExist:
        return None
