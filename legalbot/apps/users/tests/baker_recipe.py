import random

from model_bakery.recipe import Recipe, foreign_key

from legalbot.apps.business.tests.baker_recipe import BusinessRecipes, FacultyRecipes


class UserRecipes:
    def create_user_recipe():
        user_recipe = Recipe(
            "users.User",
            first_name="Pablo andres",
            last_name="torres labraña",
            identification_number="20398373-3",
        )
        return user_recipe


class PartnerRecipes:
    def create_partner_recipe():
        user_foreign_key = UserRecipes.create_user_recipe()
        business_foreign_key = BusinessRecipes.create_business_recipe()
        partner_recipe = Recipe(
            "users.Partner",
            user=foreign_key(user_foreign_key),
            business=foreign_key(business_foreign_key),
            address="he military 7345",
            participation=lambda: random.randint(0, 100),
        )

        return partner_recipe

    def get_active_partners_recipe():
        partner_recipe = PartnerRecipes.create_partner_recipe()
        partner_recipe.is_active = True
        return partner_recipe


class AdminRecipes:
    def create_admin_recipe():
        user_foreign_key = UserRecipes.create_user_recipe()
        business_foreign_key = BusinessRecipes.create_business_recipe()

        admin_recipe = Recipe(
            "users.Administrator",
            user=foreign_key(user_foreign_key),
            business=foreign_key(business_foreign_key),
        )
        return admin_recipe

    def get_active_admin_recipe():
        admin_recipe = AdminRecipes.create_admin_recipe()
        admin_recipe.is_active = True
        return admin_recipe
