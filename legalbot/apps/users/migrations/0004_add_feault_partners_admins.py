from django.db import migrations
from legalbot.apps.users.models import Partner, User, Administrator
from legalbot.apps.business.models import Business, Faculty


def create_default_partners_admins(apps, schema_editor):
    # Get the user and business instances
    miguel_user = User.objects.get(identification_number="12432567-K")

    esteban_user = User.objects.get(identification_number="10456983-9")

    juan_user = User.objects.get(identification_number="15192932-6")
    business = Business.objects.first()

    checks_faculty = Faculty.objects.get(name="Abrir cuentas corrientes")
    contracts_faculty = Faculty.objects.get(name="Firmar contratos de compraventa")
    sign_checks = Faculty.objects.get(name="Firmar cheques")

    # Create the default partners
    Partner.objects.create(
        user=juan_user,
        business=business,
        address="Av holanda 2222",
        participation=50,
    )

    Partner.objects.create(
        user=esteban_user,
        business=business,
        address="Av siempre viva 2436",
        participation=50,
    )

    # Create the Administrator instance
    administrator_esteban = Administrator.objects.create(
        user=esteban_user,
        business=business,
    )
    # Assign the faculties to the administrator esteban
    administrator_esteban.faculties.add(checks_faculty, contracts_faculty, sign_checks)

    administrator_miguel = Administrator.objects.create(
        user=miguel_user,
        business=business,
    )

    # Assign the faculties to the administrator miguel
    administrator_miguel.faculties.add(sign_checks)


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_add_default_users"),
        ("business", "0003_create_faculties"),
    ]

    operations = [
        migrations.RunPython(create_default_partners_admins),
    ]
