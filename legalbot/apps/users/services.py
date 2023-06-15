from typing import List, Optional

from legalbot.apps.users.models import Administrator, Partner
from legalbot.apps.users.providers import admin as admin_providers
from legalbot.apps.users.providers import partner as partner_providers


def get_partner_by_uuid(uuid: str) -> List[Partner]:
    return partner_providers.get_partner_by_uuid(uuid=uuid)


def get_partner_by_identification_number(
    identification_number: str,
) -> Optional[Partner]:
    """
    Service to be used in different applications to be able to identify if the member's identification number exists.
    """
    return partner_providers.get_partner_by_identification_number(
        identification_number=identification_number
    )


def get_admin_by_identification_number(
    identification_number: str,
) -> Optional[Administrator]:
    """
    Service to be used in different applications to be able to identify if the member's identification number exists.
    """
    return admin_providers.get_admin_by_identification_number(
        identification_number=identification_number
    )
