from typing import Optional

from rest_framework.authtoken.models import Token

from legalbot.apps.users.providers import user as user_providers
from legalbot.apps.users.utils.lib.exceptions import CantCreateToken


def remove_token_by_user_uuid(
    user_uuid: str, generate_new_token=False
) -> Optional[Token]:
    """
    Method for generate token by user uuid

    Parameters:
        user_uuid (str): The UUID of the user.
        generate_new_token (bool): token generator

    Returns:
        Optional[Token]: returns the token instance if found, otherwise None.
    """
    user = user_providers.get_user_by_uuid(uuid=user_uuid)
    if not user:
        return None
    try:
        if Token.objects.filter(user=user):
            user.auth_token.delete()
        if generate_new_token:
            token = Token.objects.create(user=user)
            return token
        return None
    except CantCreateToken:
        return None
