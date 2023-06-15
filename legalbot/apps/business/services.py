from typing import List, Optional, Union

from legalbot.apps.business.models import Business, Faculty
from legalbot.apps.business.providers import business as business_providers
from legalbot.apps.business.providers import faculty as faculty_providers


def get_all_business() -> List[Business]:
    return business_providers.get_all_business()


def get_business_by_uuid(uuid: str) -> Optional[Business]:
    return business_providers.get_business_by_uuid(uuid=uuid)


def get_all_faculties() -> List[Faculty]:
    return faculty_providers.get_all_faculties()
