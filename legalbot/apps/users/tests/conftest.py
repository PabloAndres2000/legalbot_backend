import pytest

from legalbot.apps.business.tests.baker_recipe import BusinessRecipes, FacultyRecipes
from legalbot.apps.users.tests.baker_recipe import (
    AdminRecipes,
    PartnerRecipes,
    UserRecipes,
)


@pytest.fixture
def non_existing_identification_number():
    return "1234567890"


@pytest.fixture
def non_existing_uuid():
    return "a4a70900-24e1-11df-8924-001e8cfc7c3a"


@pytest.fixture
def get_create_partners_fixture():
    create_partner_fixture = PartnerRecipes.create_partner_recipe()
    return create_partner_fixture.make()


@pytest.fixture
def get_active_partners_fixture():
    get_active_partners_recipe = PartnerRecipes.get_active_partners_recipe()
    return get_active_partners_recipe.make()


@pytest.fixture
def partner_with_user_and_business(create_user_fixture, create_business_fixture):
    partner_recipe = PartnerRecipes.create_partner_recipe()
    partner = partner_recipe.make(
        user=create_user_fixture, business=create_business_fixture
    )
    return partner


@pytest.fixture
def create_user_fixture():
    create_user_recipe = UserRecipes.create_user_recipe()
    return create_user_recipe.make()


@pytest.fixture
def create_business_fixture():
    create_business_recipe = BusinessRecipes.create_business_recipe()
    return create_business_recipe.make()


@pytest.fixture
def create_admin_fixture():
    create_admin_recipe = AdminRecipes.create_admin_recipe()
    return create_admin_recipe.make()


@pytest.fixture
def get_active_admins_fixture():
    get_active_admins_recipe = AdminRecipes.get_active_admin_recipe()
    return get_active_admins_recipe.make()
