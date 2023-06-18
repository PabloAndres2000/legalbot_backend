from model_bakery.recipe import Recipe


class BusinessRecipes:
    def create_business_recipe():
        business_recipe = Recipe(
            "business.Business",
            name="MagallanesSpA",
            identification_number="75346753-8",
        )
        return business_recipe


class FacultyRecipes:
    def create_faculty_recipe():
        faculty_recipe = Recipe("business.Faculty", name="Abrir cuentas corrientes")
        return faculty_recipe
