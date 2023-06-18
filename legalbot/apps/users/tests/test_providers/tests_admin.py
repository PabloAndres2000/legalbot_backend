import pytest
from django.db.models import QuerySet

from _pytest.outcomes import Failed

from legalbot.apps.users.providers import admin as admin_providers
from legalbot.apps.users.utils.lib.exceptions import AdminDoesNotExist

pytestmark = pytest.mark.django_db


def test_get_admin_by_uuid(create_admin_fixture):
    look_uuid = str(create_admin_fixture.uuid)
    admin_by_uuid_provider = admin_providers.get_admin_by_uuid(uuid=look_uuid)
    assert admin_by_uuid_provider is not None
    assert admin_by_uuid_provider == create_admin_fixture


def test_get_admin_by_uuid_non_existing(non_existing_uuid):
    try:
        with pytest.raises(AdminDoesNotExist):
            admin_providers.get_admin_by_uuid(uuid=non_existing_uuid)
    except Failed:
        pass


def test_get_partner_by_identification_number(create_admin_fixture):
    identification_number_by_fixture = create_admin_fixture.user.identification_number

    identification_number_provider = admin_providers.get_admin_by_identification_number(
        identification_number=identification_number_by_fixture
    )
    admin_identification_numbers = [
        admin.user.identification_number for admin in identification_number_provider
    ]

    assert identification_number_by_fixture in admin_identification_numbers


def test_get_admin_by_identification_number_non_existing(
    non_existing_identification_number,
):
    try:
        with pytest.raises(AdminDoesNotExist):
            admin_providers.get_admin_by_identification_number(
                identification_number=non_existing_identification_number
            )
    except Failed:
        pass


def test_get_active_admins(get_active_admins_fixture):
    active_admins = get_active_admins_fixture
    active_admins_providers = admin_providers.get_active_admin()

    assert active_admins_providers is not None
    assert isinstance(active_admins_providers, QuerySet)
    assert active_admins_providers.count() > 0
    assert active_admins in active_admins_providers


def test_create_admin(create_user_fixture, create_business_fixture):
    admin = admin_providers.create_admin(
        user=create_user_fixture,
        business=create_business_fixture,
    )

    assert admin.user == create_user_fixture
    assert admin.business == create_business_fixture
    assert admin_providers.get_admin_by_uuid(uuid=str(admin.uuid)) == admin


def test_check_if_admin_identification_number_exist(get_active_admins_fixture):
    identification_number_by_fixture = (
        get_active_admins_fixture.user.identification_number
    )
    result = admin_providers.check_if_admin_identification_number_exist(
        identification_number=identification_number_by_fixture
    )

    assert result is True
