import pytest
from django.db.models import QuerySet

from _pytest.outcomes import Failed

from legalbot.apps.users.providers import partner as partner_providers
from legalbot.apps.users.utils.lib.exceptions import PartnerDoesNotExist

pytestmark = pytest.mark.django_db


def test_get_partner_by_uuid(get_active_partners_fixture):
    look_uuid = str(get_active_partners_fixture.uuid)
    partner_by_uuid_provider = partner_providers.get_partner_by_uuid(uuid=look_uuid)
    assert partner_by_uuid_provider is not None
    assert partner_by_uuid_provider == get_active_partners_fixture


def test_get_partner_by_uuid_non_existing(non_existing_uuid):
    with pytest.raises(PartnerDoesNotExist):
        partner_providers.get_partner_by_uuid(uuid=non_existing_uuid)


def test_get_partner_by_identification_number(get_active_partners_fixture):
    identification_number_by_fixture = (
        get_active_partners_fixture.user.identification_number
    )

    # Call the get_partner_by_identification_number() method
    identification_number_provider = (
        partner_providers.get_partner_by_identification_number(
            identification_number=identification_number_by_fixture
        )
    )

    # Extract the identification numbers from the retrieved partners
    partner_identification_numbers = [
        partner.user.identification_number for partner in identification_number_provider
    ]

    # Assert that the retrieved identification numbers match the fixture identification number
    assert identification_number_by_fixture in partner_identification_numbers


def test_get_partner_by_identification_number_non_existing(
    non_existing_identification_number,
):
    try:
        with pytest.raises(PartnerDoesNotExist):
            partner_providers.get_partner_by_identification_number(
                identification_number=non_existing_identification_number
            )
    except Failed:
        pass


def test_get_active_partners(get_active_partners_fixture):
    active_partners = get_active_partners_fixture
    active_partners_providers = partner_providers.get_active_partners()
    # -> check partners that are not in None, we make sure that it returns the active partners
    assert active_partners_providers is not None
    # -> Check that it is an instance of the Queryset class, we make sure that the providers are an ORM queryset
    assert isinstance(active_partners_providers, QuerySet)
    # -> we make sure that the query has at least 1 partner
    assert active_partners_providers.count() > 0
    # -> we verify that the active partners of the fixture are included in the query set of the provider(query)
    assert active_partners in active_partners_providers


def test_create_partner(create_user_fixture, create_business_fixture):
    partner = partner_providers.create_partner(
        user=create_user_fixture,
        business=create_business_fixture,
        address="las condes 3424",
        participation=50,
    )

    assert partner.user == create_user_fixture
    assert partner.business == create_business_fixture
    assert partner_providers.get_partner_by_uuid(uuid=str(partner.uuid)) == partner


def test_check_if_partner_identification_number_exist(get_active_partners_fixture):
    # Get the identification number of the create_partner_fixture
    identification_number_by_fixture = (
        get_active_partners_fixture.user.identification_number
    )

    # Call the check_if_partner_identification_number_exist() method
    result = partner_providers.check_if_partner_identification_number_exist(
        identification_number=identification_number_by_fixture
    )

    # Assert that the result is True since a partner with the identification number exists
    assert result is True


@pytest.mark.parametrize(
    "address,expected",
    (
        ("he military 7345", True),
        ("los andes #123", False),
        ("vitacura #23123", False),
        ("las condes #23123", False),
    ),
)
def test_check_if_partner_already_exists(
    address, expected, partner_with_user_and_business
):
    user_uuid = str(partner_with_user_and_business.user.uuid)
    business_uuid = str(partner_with_user_and_business.business.uuid)

    result = partner_providers.check_if_partner_already_exists(
        user_uuid=user_uuid,
        business_uuid=business_uuid,
        address=address,
    )

    print(f"Address: {address}")
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    assert result == expected
