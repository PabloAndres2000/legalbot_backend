import pytest
from django.db.models import QuerySet

from _pytest.outcomes import Failed

from legalbot.apps.business.providers import business as business_providers
from legalbot.apps.business.utils.lib.exceptions import BusinessDoesNotExist

pytestmark = pytest.mark.django_db


def test_get_business_by_uuid(create_business_fixture):
    look_uuid = str(create_business_fixture.uuid)
    business_by_uuid_provider = business_providers.get_business_by_uuid(uuid=look_uuid)
    assert business_by_uuid_provider is not None
    assert business_by_uuid_provider == create_business_fixture


def test_get_business_by_uuid_non_existing(non_existing_uuid):
    try:
        with pytest.raises(BusinessDoesNotExist):
            business_providers.get_business_by_uuid(uuid=non_existing_uuid)
    except Failed:
        pass


def test_get_all_business(create_business_fixture):
    expected_business = create_business_fixture
    all_business_provider = business_providers.get_all_business()
    business = all_business_provider[0]

    assert isinstance(all_business_provider, QuerySet)
    assert len(all_business_provider) == 2
    assert business.name != expected_business.name
    assert business.identification_number != expected_business.identification_number


def test_get_business_by_manager_or_partner_id_number(
    partner_with_user_and_business,
    admin_with_user_and_business,
):
    identification_number = partner_with_user_and_business.user.identification_number

    result = business_providers.get_business_by_manager_or_partner_id_number(
        identification_number=identification_number
    )

    assert partner_with_user_and_business.business in result
    assert admin_with_user_and_business.business in result
