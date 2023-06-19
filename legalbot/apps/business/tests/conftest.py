import pytest

from legalbot.apps.business.tests.baker_recipe import BusinessRecipes
from legalbot.apps.users.tests.baker_recipe import AdminRecipes, PartnerRecipes
from legalbot.apps.users.tests.conftest import (
    create_admin_fixture as admin_create_fixture,
    create_user_fixture as user_create_fixture,
    get_create_partners_fixture as create_partner_fixture,
    non_existing_identification_number as global_non_existing_identification_number,
    non_existing_uuid as global_non_existing_uuid,
)


@pytest.fixture
def non_existing_identification_number(global_non_existing_identification_number):
    return global_non_existing_identification_number


@pytest.fixture
def non_existing_uuid(global_non_existing_uuid):
    return global_non_existing_uuid


@pytest.fixture
def create_business_fixture():
    create_business_recipe = BusinessRecipes.create_business_recipe()
    return create_business_recipe.make()


@pytest.fixture
def create_user_fixture(user_create_fixture):
    return user_create_fixture


@pytest.fixture
def partner_with_user_and_business(create_user_fixture, create_business_fixture):
    partner_recipe = PartnerRecipes.create_partner_recipe()
    partner = partner_recipe.make(
        user=create_user_fixture, business=create_business_fixture
    )
    return partner


@pytest.fixture
def admin_with_user_and_business(create_user_fixture, create_business_fixture):
    admin_recipe = AdminRecipes.create_admin_recipe()
    admin = admin_recipe.make(
        user=create_user_fixture, business=create_business_fixture
    )
    return admin
